import os
from enum import Enum

import typer

from configuration.configuration import ConfigurationParser, IConfigurationParser
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


@app.command()
def test_homework(h: Homework, zip_file_path: str):
    homework_tester: IHomeworkTester = HomeworkTester()
    config_parser: IConfigurationParser = ConfigurationParser()
    result = homework_tester.test_homework(
        zip_file_path,
        config_parser.parse_configuration_file(
            os.path.join(PROJECT_PATH, "cmd/config_files/" + h.value + ".yml")
        ),
    )
    print(result)


@app.command()
def test_homework_folder(h: Homework, homework_folder_path: str):
    homework_tester: IHomeworkTester = HomeworkTester()
    config_parser: IConfigurationParser = ConfigurationParser()
    result = homework_tester.test_homework_folder(
        homework_folder_path,
        config_parser.parse_configuration_file(
            os.path.join(PROJECT_PATH, "cmd/config_files/" + h.value + ".yml")
        ),
    )
    print(result)
