import os
from typing import Protocol

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from n2tconfig import GOOGLE_API_CREDENTIALS, GOOGLE_API_TOKENS_PATH


class IGrader(Protocol):
    def grade_homework(
        self, course_id, coursework_id, student_id, submission_id, test_result
    ):
        pass


class ClassroomGrader:
    def grade_homework(
        self, course_id, coursework_id, student_id, submission_id, test_result
    ):
        creds = self._auth()
        service = build("classroom", "v1", credentials=creds)
        submission = (
            service.courses()
            .courseWork()
            .studentSubmissions()
            .get(courseId=course_id, courseWorkId=coursework_id, id=submission_id)
            .execute()
        )

        # Grade the submission
        submission["assignedGrade"] = 90  # Set the grade value as per your requirements

        # Update the student's submission
        updated_submission = (
            service.courses()
            .courseWork()
            .studentSubmissions()
            .patch(
                courseId=course_id,
                courseWorkId=coursework_id,
                id=submission_id,
                updateMask="assignedGrade",
                body=submission,
            )
            .execute()
        )

        # Retrieve the updated grade
        updated_grade = updated_submission["assignedGrade"]
        print(f"Updated grade: {updated_grade}")

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
