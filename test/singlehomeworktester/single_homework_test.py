import os.path

from configuration.configuration import ConfigurationParser, IConfigurationParser
from n2tconfig import PROJECT_PATH
from singlehomeworktester.single_tester import (
    ISingleHomeworkTester,
    SingleHomeworkTester,
)


def test_valid_homework() -> None:
    test_archive_folder_path = os.path.join(
        PROJECT_PATH, "test", "singlehomeworktester", "homeworkarchives"
    )
    valid_archive_path = os.path.join(test_archive_folder_path, "valid.zip")

    config_parser: IConfigurationParser = ConfigurationParser()
    config = config_parser.parse_configuration_file(
        os.path.join(test_archive_folder_path, "config", "hw1.yml")
    )

    single_tester: ISingleHomeworkTester = SingleHomeworkTester()
    res = single_tester.test_homework(valid_archive_path, config, "01")
    assert res.full_count == res.passed_count


def test_not_valid_and_homework() -> None:
    test_archive_folder_path = os.path.join(
        PROJECT_PATH, "test", "singlehomeworktester", "homeworkarchives"
    )
    valid_archive_path = os.path.join(test_archive_folder_path, "and_not_valid.zip")

    config_parser: IConfigurationParser = ConfigurationParser()
    config = config_parser.parse_configuration_file(
        os.path.join(test_archive_folder_path, "config", "hw1.yml")
    )

    single_tester: ISingleHomeworkTester = SingleHomeworkTester()
    res = single_tester.test_homework(valid_archive_path, config, "01")
    assert res.full_count != res.passed_count
    assert res.passed_count == 5


def test_not_valid_mux_homework() -> None:
    test_archive_folder_path = os.path.join(
        PROJECT_PATH, "test", "singlehomeworktester", "homeworkarchives"
    )
    valid_archive_path = os.path.join(test_archive_folder_path, "mux_not_valid.zip")

    config_parser: IConfigurationParser = ConfigurationParser()
    config = config_parser.parse_configuration_file(
        os.path.join(test_archive_folder_path, "config", "hw1.yml")
    )

    single_tester: ISingleHomeworkTester = SingleHomeworkTester()
    res = single_tester.test_homework(valid_archive_path, config, "01")
    assert res.full_count != res.passed_count
    assert res.passed_count == 8


def test_without_and_implemented() -> None:
    test_archive_folder_path = os.path.join(
        PROJECT_PATH, "test", "singlehomeworktester", "homeworkarchives"
    )
    valid_archive_path = os.path.join(
        test_archive_folder_path, "and_not_implemented.zip"
    )

    config_parser: IConfigurationParser = ConfigurationParser()
    config = config_parser.parse_configuration_file(
        os.path.join(test_archive_folder_path, "config", "hw1.yml")
    )

    single_tester: ISingleHomeworkTester = SingleHomeworkTester()
    res = single_tester.test_homework(valid_archive_path, config, "01")
    assert res.full_count != res.passed_count
    assert res.passed_count == 5
