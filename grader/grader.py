from typing import Protocol


class IGrader(Protocol):
    def grade_homework(self, student_submissions, test_results):
        pass


class ClassroomGrader:
    def grade_homework(self, student_submissions, test_results):
        pass
