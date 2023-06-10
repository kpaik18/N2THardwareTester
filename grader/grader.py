from typing import Protocol

from googleapiclient.discovery import build

from authutil.auth_util import auth_on_google_classroom


class IGrader(Protocol):
    def grade_homework(
        self, course_id, coursework_id, student_id, submission_id, test_result
    ):
        pass


class ClassroomGrader:
    def grade_homework(
        self, course_id, coursework_id, student_id, submission_id, test_result
    ):
        creds = auth_on_google_classroom()
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
