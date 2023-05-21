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
        self._download_student_submissions(
            service, course_student_ids, course, coursework
        )

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
        for student_id in course_student_ids:
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
            sorted_submissions = sorted(
                submissions, key=lambda x: x["updateTime"], reverse=True
            )
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
