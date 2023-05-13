import os.path
from typing import Protocol

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
    def get_assignment_submissions(self, course_code: str, coursework_id: str) -> None:
        creds = self._auth()
        course = self._get_course_by_code(course_code, creds)
        print(course)

    def _get_course_by_code(self, course_code: str, creds: Credentials) -> str:
        try:
            service = build("classroom", "v1", credentials=creds)

            # Call the Classroom API
            results = service.courses().list().execute()
            courses = results.get("courses", [])

            if not courses:
                print("No courses found.")
            for course in courses:
                alternate_link = course["alternateLink"]
                if alternate_link[alternate_link.rfind("/") + 1 :] == course_code:
                    return course

        except HttpError as error:
            print("An error occurred: %s" % error)

    def _auth(self) -> Credentials:
        credentials_path = GOOGLE_API_CREDENTIALS
        tokens_path = GOOGLE_API_TOKENS_PATH
        SCOPES = [
            "https://www.googleapis.com/auth/classroom.courses.readonly",
            "https://www.googleapis.com/auth/classroom.coursework.students",
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
