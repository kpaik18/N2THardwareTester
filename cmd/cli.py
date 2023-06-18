import os
from enum import Enum

import typer

from configuration.configuration import ConfigurationParser, IConfigurationParser
from fetcher.fetcher import ClassroomFetcher, IHomeworkFetcher
from grader.grader import ClassroomGrader, IGrader
from homeworktester.homework_tester import HomeworkTester, IHomeworkTester
from n2tconfig import PROJECT_PATH

app = typer.Typer()


class Homework(Enum):
    h1 = "h1"
    h2 = "h2"
    h3 = "h3"
    h4 = "h4"
    h5 = "h5"


@app.command()
def dummy_command():
    print("dummy")


def get_config_file_path(h: Homework):
    return os.path.join(PROJECT_PATH, "cmd/config_files/" + h.value + ".yml")


@app.command()
def test_homework(h: Homework, zip_file_path: str):
    homework_tester: IHomeworkTester = HomeworkTester()
    config_parser: IConfigurationParser = ConfigurationParser()
    result = homework_tester.test_homework(
        zip_file_path,
        config_parser.parse_configuration_file(get_config_file_path(h)),
    )
    print(result)


@app.command()
def grade_homework(
    h: Homework, course_code: str, coursework_code: str, drive_folder_url_code: str
):
    fetcher: IHomeworkFetcher = ClassroomFetcher()
    (
        homework_folder,
        student_submissions,
        course_id,
        coursework_id,
        course_students,
        coursework_due_date,
        coursework_due_time,
    ) = fetcher.get_assignment_submissions(course_code, coursework_code)
    print(student_submissions)
    config_parser: IConfigurationParser = ConfigurationParser()
    config = config_parser.parse_configuration_file(get_config_file_path(h))
    tester: IHomeworkTester = HomeworkTester()
    test_results = tester.test_homework_folder(homework_folder, config)
    grader: IGrader = ClassroomGrader()
    grader.grade_homework(
        h.value,
        course_students,
        student_submissions,
        test_results,
        drive_folder_url_code,
        coursework_due_date,
        coursework_due_time,
    )
