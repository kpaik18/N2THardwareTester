from dataclasses import dataclass
from datetime import datetime
from typing import List, Protocol

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from authutil.auth_util import auth_on_google_classroom
from fetcher.fetcher import StudentSubmission
from homeworktester.test_result import TestResult
from n2tconfig import TIMESTAMP_NOT_FOUND_VALUE_LATE_DAYS


class IGrader(Protocol):
    def grade_homework(
        self,
        homework_name,
        students_data,
        student_submissions,
        test_results,
        drive_folder_id,
        coursework_due_date,
        coursework_due_time,
        late_days,
    ):
        pass


@dataclass
class StudentGradeData:
    student_id: str
    student_name: str
    student_last_name: str
    homework_name: str
    grade: int
    late_days: int
    grade_after_late_days: int


class ClassroomGrader:
    def grade_homework(
        self,
        homework_name,
        students_data,
        student_submissions,
        test_results,
        drive_folder_id,
        coursework_due_date,
        coursework_due_time,
        late_days,
    ):
        coursework_due_timestamp = datetime(
            coursework_due_date["year"],
            coursework_due_date["month"],
            coursework_due_date["day"],
            coursework_due_time["hours"],
            coursework_due_time["minutes"] if "minutes" in coursework_due_time else 0,
        )
        creds = auth_on_google_classroom()
        google_sheet_id = self._create_google_sheet(
            drive_folder_id, homework_name, creds
        )
        student_grade_data = self._get_student_grade_data(
            students_data,
            student_submissions,
            test_results,
            coursework_due_timestamp,
            late_days,
        )
        self._write_student_grades_in_spreadsheet(google_sheet_id, student_grade_data)

    def _create_google_sheet(self, drive_folder_id, homework_name, creds):
        service = build("drive", "v3", credentials=creds)
        file_metadata = {
            "name": homework_name + "-grades",
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
        coursework_due_timestamp,
        late_days,
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
            family_name = ""
            if (
                "familyName"
                in student_data_dict[student_submission.student_id]["profile"]["name"]
            ):
                family_name = student_data_dict[student_submission.student_id][
                    "profile"
                ]["name"]["familyName"]
            grade_for_submission = (int)(
                test_result.passed_count / test_result.full_count * 100
            )
            late_days_for_submission = self._get_late_days(
                student_submission.turn_in_timestamp, coursework_due_timestamp
            )
            grade_after_late_days = self._calculate_grade_after_late_days(
                grade_for_submission, late_days_for_submission, late_days
            )
            student_grade_data.append(
                StudentGradeData(
                    student_submission.student_id,
                    student_data_dict[student_submission.student_id]["profile"]["name"][
                        "givenName"
                    ],
                    family_name,
                    student_submission.submission_file_name,
                    grade_for_submission,
                    0 if late_days_for_submission == TIMESTAMP_NOT_FOUND_VALUE_LATE_DAYS else late_days_for_submission,
                    grade_after_late_days,
                )
            )
        return student_grade_data

    def _write_student_grades_in_spreadsheet(self, google_sheet_id, student_grade_data):
        creds = auth_on_google_classroom()
        try:
            service = build("sheets", "v4", credentials=creds)
            values = []
            for student_data in student_grade_data:
                row = [
                    student_data.student_id,
                    student_data.student_name,
                    student_data.student_last_name,
                    student_data.homework_name,
                    student_data.grade,
                    student_data.late_days,
                    student_data.grade_after_late_days,
                ]
                values.append(row)
            body = {"values": values}
            result = (
                service.spreadsheets()
                .values()
                .update(
                    spreadsheetId=google_sheet_id,
                    range="Sheet1!A1:G",
                    valueInputOption="RAW",
                    body=body,
                )
                .execute()
            )
            print(f"{result.get('updatedCells')} cells updated.")
            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

    def _get_late_days(self, turn_in_timestamp_str, coursework_due_timestamp):
        if turn_in_timestamp_str is None:
            return TIMESTAMP_NOT_FOUND_VALUE_LATE_DAYS
        turn_in_timestamp_str = turn_in_timestamp_str.rstrip("Z")
        turn_in_timestamp = datetime.fromisoformat(turn_in_timestamp_str)
        is_late = turn_in_timestamp > coursework_due_timestamp
        if not is_late:
            return 0
        return (turn_in_timestamp - coursework_due_timestamp).days + 1

    def _calculate_grade_after_late_days(
        self, grade_for_submission, late_days_for_submission, late_days
    ):
        if late_days_for_submission <= 0:
            return grade_for_submission
        for late_day in late_days:
            if late_day.day_count == late_days_for_submission:
                return max(0, grade_for_submission - late_day.percentage_loss)
        return 0
