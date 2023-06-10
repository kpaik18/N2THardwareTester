from dataclasses import dataclass
from typing import List, Protocol

from googleapiclient.discovery import build

from authutil.auth_util import auth_on_google_classroom
from fetcher.fetcher import StudentSubmission
from homeworktester.test_result import TestResult


class IGrader(Protocol):
    def grade_homework(
        self, students_data, student_submissions, test_results, drive_folder_id
    ):
        pass


@dataclass
class StudentGradeData:
    student_id: str
    student_name: str
    student_last_name: str
    homework_name: str
    grade: int


class ClassroomGrader:
    def grade_homework(
        self, students_data, student_submissions, test_results, drive_folder_id
    ):
        creds = auth_on_google_classroom()
        google_sheet_id = self._create_google_sheet(drive_folder_id, creds)
        student_grade_data = self._get_student_grade_data(
            students_data, student_submissions, test_results
        )

    def _create_google_sheet(self, drive_folder_id, creds):
        service = build("drive", "v3", credentials=creds)
        file_metadata = {
            "name": "My Spreadsheet",
            "mimeType": "application/vnd.google-apps.spreadsheet",
            "parents": [drive_folder_id],
        }
        file = service.files().create(body=file_metadata).execute()
        return file["id"]

    def _get_student_grade_data(
        self,
        students_data,
        student_submissions: List[StudentSubmission],
        test_results: List[TestResult],
    ):
        test_result_dict = {
            test_result.name: test_result for test_result in test_results
        }
        student_data_dict = {student["userId"]: student for student in students_data}
        student_grade_data = []
        for student_submission in student_submissions:
            test_result: TestResult = test_result_dict[
                student_submission.submission_file_name
            ]
            student_grade_data.append(
                StudentGradeData(
                    student_submission.student_id,
                    student_data_dict[student_submission.student_id]["profile"]["name"][
                        "givenName"
                    ],
                    student_data_dict[student_submission.student_id]["profile"]["name"][
                        "familyName"
                    ],
                    student_submission.submission_file_name,
                    (int)(test_result.passed_count / test_result.full_count * 100),
                )
            )
        print(student_grade_data)
