import os.path
from typing import List, Protocol

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from n2tconfig import DOWNLOAD_FOLDER, GOOGLE_API_CREDENTIALS, GOOGLE_API_TOKENS_PATH


class IHomeworkFetcher(Protocol):
    def get_assignment_submissions(self, course_code: str, coursework_id: str) -> str:
        pass


class ClassroomFetcher:
    def get_assignment_submissions(self, course_code: str, coursework_code: str) -> str:
        creds = self._auth()
        service = build("classroom", "v1", credentials=creds)
        course = self._get_course_by_code(service, course_code)
        course_students = self._get_course_students(service, course)
        coursework = self._get_coursework_by_course_and_code(
            service, course, coursework_code
        )
        return self._download_submissions(service, course, coursework)

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

    def _get_course_students(self, service, course) -> List[str]:
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
        return all_students

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
            "https://www.googleapis.com/auth/drive.readonly",
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

    def _download_submissions(self, service, course, coursework):
        submissions = (
            service.courses()
            .courseWork()
            .studentSubmissions()
            .list(courseId=course["id"], courseWorkId=coursework["id"])
            .execute()
            .get("studentSubmissions", [])
        )
        download_folder = os.path.join(DOWNLOAD_FOLDER)
        download_folder = os.path.join(download_folder, course["id"], coursework["id"])
        _ = os.path.dirname(download_folder)
        os.makedirs(_, exist_ok=True)

        for submission in submissions:
            if (
                # submission["state"] == "TURNED_IN"
                # and
                len(submission["assignmentSubmission"])
                > 0
            ):
                user_id = submission["userId"]
                attachments = submission["assignmentSubmission"].get("attachments", [])
                attachment = attachments[0]
                file_id = attachment["driveFile"]["id"]
                file_title = attachment["driveFile"]["title"]

                creds = self._auth()
                drive_service = build("drive", "v3", credentials=creds)

                request = drive_service.files().get_media(fileId=file_id)
                filename = os.path.join(download_folder, file_title)

                with open(filename, "wb") as f:
                    downloader = MediaIoBaseDownload(f, request)
                    done = False
                    while done is False:
                        status, done = downloader.next_chunk()
        return download_folder
