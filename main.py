import os
import os.path
from dataclasses import dataclass
from typing import List, Protocol

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from configuration.configuration import (ConfigurationParser,
                                         IConfigurationParser)
from fetcher.fetcher import ClassroomFetcher, IHomeworkFetcher
from grader.grader import ClassroomGrader, IGrader
from homeworktester.homework_tester import HomeworkTester, IHomeworkTester
from n2tconfig import (DOWNLOAD_FOLDER, GOOGLE_API_CREDENTIALS,
                       GOOGLE_API_TOKENS_PATH)


def auth():
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
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(tokens_path, "w") as token:
            token.write(creds.to_json())
    return creds


if __name__ == "__main__":
    fetcher: IHomeworkFetcher = ClassroomFetcher()
    (
        homework_folder,
        student_submissions,
        course_id,
        coursework_id,
    ) = fetcher.get_assignment_submissions("NjEyMDE2MDkyOTky", "NjEyOTA1NjY1MjM0")
    print(student_submissions)
    print(course_id)
    print(coursework_id)
    config_parser: IConfigurationParser = ConfigurationParser()
    config = config_parser.parse_configuration_file("h1.yml")
    tester: IHomeworkTester = HomeworkTester()
    test_results = tester.test_homework_folder(homework_folder, config)
    print(test_results)
    grader: IGrader = ClassroomGrader()
    grader.grade_homework(
        course_id,
        coursework_id,
        student_submissions[0].student_id,
        student_submissions[0].submission_id,
        test_results[0],
    )

    # creds = auth()
    # service = build("classroom", "v1", credentials=creds)
    # # Set up the course ID and assignment details
    # course_id = '612016092992'
    #
    # assignment = {
    #     'title': 'New Assignment',
    #     'description': 'This is a new assignment.',
    #     'materials': [
    #         {
    #             'link': {
    #                 'url': 'https://example.com'
    #             }
    #         }
    #     ],
    #     'workType': 'ASSIGNMENT',
    #     'state': 'PUBLISHED',
    #     'dueDate': {
    #         'year': 2023,
    #         'month': 6,
    #         'day': 5
    #     },
    #     'dueTime': {
    #         'hours': 23,
    #         'minutes': 59,
    #         'seconds': 59
    #     }
    # }
    #
    # # Create the assignment
    # created_assignment = service.courses().courseWork().create(
    #     courseId=course_id,
    #     body=assignment
    # ).execute()
    #
    # # Retrieve the created assignment ID
    # assignment_id = created_assignment['id']
    # print('Created assignment ID:', assignment_id)
