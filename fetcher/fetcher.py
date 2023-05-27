import os.path
from typing import List, Protocol

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from n2tconfig import GOOGLE_API_CREDENTIALS, GOOGLE_API_TOKENS_PATH


class IHomeworkFetcher(Protocol):
    def get_assignment_submissions(self, course_code: str, coursework_id: str) -> None:
        pass


class ClassroomFetcher:
    def get_assignment_submissions(
        self, course_code: str, coursework_code: str
    ) -> None:
        creds = self._auth()
        service = build("classroom", "v1", credentials=creds)
        course = self._get_course_by_code(service, course_code)
        course_student_ids = self._get_course_student_ids(service, course)
        coursework = self._get_coursework_by_course_and_code(
            service, course, coursework_code
        )
        # self._download_student_submissions(
        #     service, course_student_ids, course, coursework
        # )
        self._second_try_submissions(service, course, coursework)

    def _get_coursework_by_course_and_code(self, service, course, coursework_code):
        courseworks = (
            service.courses()
            .courseWork()
            .list(courseId=course["id"])
            .execute()["courseWork"]
        )
        for cw in courseworks:
            if coursework_code in cw["alternateLink"]:
                return cw
        print("CourseWork not Found")

    def _download_student_submissions(
        self, service, course_student_ids, course, coursework
    ):
        counter = 0
        # bekas_id = "109915369104227089235"
        for student_id in course_student_ids:
            # if student_id != bekas_id:
            #     continue
            print(counter)
            counter += 1
            response = (
                service.courses()
                .courseWork()
                .studentSubmissions()
                .list(
                    courseId=course["id"],
                    courseWorkId=coursework["id"],
                    userId=student_id,
                )
                .execute()
            )
            submissions = response.get("studentSubmissions", [])
            latest_submission = submissions[0]
            if len(latest_submission["assignmentSubmission"]) == 0:
                print("not submitted")
            if len(submissions) != 1:
                print(submissions)

    def _get_course_student_ids(self, service, course) -> List[str]:
        course_id = course["id"]
        all_students = []
        page_token = None
        while True:
            students = (
                service.courses()
                .students()
                .list(courseId=course_id, pageToken=page_token)
                .execute()
            )
            all_students.extend(students["students"])
            if "nextPageToken" not in students or students["nextPageToken"] is None:
                break
            page_token = students["nextPageToken"]
        student_ids = [student["userId"] for student in all_students]
        return student_ids

    def _get_course_by_code(self, service, course_code: str) -> str:
        try:
            # Call the Classroom API
            results = service.courses().list().execute()
            courses = results.get("courses", [])

            if not courses:
                print("Course by code can't be found")
            for course in courses:
                alternate_link = course["alternateLink"]
                code_substring_start_index = alternate_link.rfind("/") + 1
                if alternate_link[code_substring_start_index:] == course_code:
                    return course

        except HttpError as error:
            print("An error occurred: %s" % error)

    def _auth(self) -> Credentials:
        credentials_path = GOOGLE_API_CREDENTIALS
        tokens_path = GOOGLE_API_TOKENS_PATH
        SCOPES = [
            "https://www.googleapis.com/auth/classroom.courses.readonly",
            "https://www.googleapis.com/auth/classroom.coursework.students",
            "https://www.googleapis.com/auth/classroom.rosters",
        ]
        creds = None
        if os.path.exists(tokens_path):
            creds = Credentials.from_authorized_user_file(tokens_path, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(tokens_path, "w") as token:
                token.write(creds.to_json())
        return creds

    def _second_try_submissions(self, service, course, coursework):
        submissions = (
            service.courses()
            .courseWork()
            .studentSubmissions()
            .list(courseId=course["id"], courseWorkId=coursework["id"])
            .execute()
            .get("studentSubmissions", [])
        )

        # Create a folder to store the downloaded files
        # download_folder = "submissions"
        # os.makedirs(download_folder, exist_ok=True)

        # Download the files for each submitted student
        for submission in submissions:
            if (
                submission["state"] == "TURNED_IN"
                and len(submission["assignmentSubmission"]) > 0
            ):
                user_id = submission["userId"]
                print(user_id)
                # attachments = submission["assignmentSubmission"].get("attachments", [])
                # for attachment in attachments:
                #     file_link = attachment["link"]["url"]
                #     file_name = attachment["driveFile"]["title"]
                #     file_path = os.path.join(download_folder, file_name)
                #
                #     Download the file
                # file_data = service._http.request(file_link, method="GET")[1]
                # with open(file_path, "wb") as file:
                #     file.write(file_data)
                # print(f"Downloaded file: {file_name}")
            else:
                print("not submitted")
