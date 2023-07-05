from dataclasses import dataclass
from enum import Enum

import pkg_resources
import typer

from configuration.configuration import ConfigurationParser, IConfigurationParser
from fetcher.fetcher import ClassroomFetcher, IHomeworkFetcher
from grader.grader import ClassroomGrader, IGrader
from homeworktester.homework_tester import HomeworkTester, IHomeworkTester
from n2tconfig import env_variables_for_student, env_variable_description, env_variables_for_lecturer, \
    env_variable_names

app = typer.Typer()


class Homework(Enum):
    h1 = "h1"
    h2 = "h2"
    h3 = "h3"
    h4 = "h4"
    h5 = "h5"


@dataclass
class LateDay:
    day_count: int
    percentage_loss: int


def get_config_file_path(h: Homework):
    data_path = pkg_resources.resource_filename(__name__, "data/" + h.value + ".yml")
    return data_path


@app.command()
def test_homework(h: Homework, zip_file_path: str):
    student_variable_vars = env_variables_for_student
    counter = 0
    for var in student_variable_vars:
        if var is None:
            var_name = env_variable_names[counter]
            print("INFO: [" + var_name + "] must be set in environment variables")
            print("INFO: [" + var_name + "] --> " + env_variable_description[var_name])
            return
        counter += 1

    homework_tester: IHomeworkTester = HomeworkTester()
    config_parser: IConfigurationParser = ConfigurationParser()
    result = homework_tester.test_homework(
        zip_file_path,
        config_parser.parse_configuration_file(get_config_file_path(h)),
    )
    print(result)


def get_late_days(late_day_percentages):
    if len(late_day_percentages) % 2 != 0:
        print("Not valid late days format")
        print(
            "format must be: {late_day_count} {percentageLoss} {late_day_count} {percentageLoss} ..."
        )
        print("example: ... 1 20 2 50 -> -20% for 1 late day, -50% for 2 late day")
        return None
    counter = 0
    late_days = []
    while counter < len(late_day_percentages):
        day_count = late_day_percentages[counter]
        counter += 1
        percentage = late_day_percentages[counter]
        if percentage < 0 and percentage > 100:
            print("percentage loss can't be more than 100 percent")
            return None
        late_days.append(LateDay(day_count, percentage))
        counter += 1
    return late_days


@app.command()
def grade_homework(
        h: Homework,
        course_code: str,
        coursework_code: str,
        drive_folder_url_code: str,
        late_day_percentages: list[int],
):
    lecture_variable_vars = env_variables_for_lecturer
    counter = 0
    for var in lecture_variable_vars:
        if var is None:
            var_name = env_variable_names[counter]
            print("INFO: [" + var_name + "] must be set in environment variables")
            print("INFO: [" + var_name + "] --> " + env_variable_description[var_name])
            return
        counter += 1
    late_days = get_late_days(late_day_percentages)
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
        late_days,
    )


@app.callback()
def main_callback(ctx: typer.Context):
    """
    Command Line Application to test nand2tetris hardware homeworks

    Commands for students who want to check their archived homework

    1. n2t-test test-homework[command] homework[argument] zip_file_address[argument]

    - homework [values from list -> (h1, h2, h3, h4, h5)]
    - zip_file_address [path of your zipped homework on your machine]

    env variables for students

    - n2t_work_area_path - path of nand2tetris folder which contains tools and project directories



    Commands for lecturers or assistants to grade student assignments

    1. n2t-test grage-homework[command] homework[argument]
                                        course_code[argument]
                                        coursework_code[argument]
                                        drive_folder_id[argument]
                                        late_days_percentages[argument]

    - homework [values from list -> (h1, h2, h3, h4, h5)]
    - course_code - can be found in url of classroom
    - coursework_code - can be found in url of classroom assignment
    - drive_folder_id - can be found in url of drive folder
    - late_days_percentages - [late_day_count] [percentage_loss] [late_day_count] [percentage_loss] ...
                              for example: 1 20 2 50 - means that for one late day student loses 20%,
                                                       for 2 late days student loses 50%,
                                                       any more late days than 2 - student loses 100%,
                              if late days is not allowed just give - "1 100" as an argument

    env variables for lecturers or assistants

    - n2t_work_area_path - path of nand2tetris folder which contains tools and project directories
    - n2t_google_api_credentials - api credentials path for google cloud console project
    - n2t_google_api_tokens_path - path for api tokens path, no need to add token file,
                                   it will be generated automatically after login
    - n2t_homework_files_download_folder - path of folder, where student assignments will be downloaded

    """
