import pytest

from configuration.configuration import ConfigurationParser, IConfigurationParser
from main import PROJECT_PATH

configuration_test_path = "test/configuration/test_config_files"


def test_configuration_files_validity() -> None:
    configuration_parser: IConfigurationParser = ConfigurationParser()
    test_files_dict = {
        "test_empty_archive.yml": False,
        "test_rar_archive.yml": False,
        "test_valid_zip_archive.yml": True,
        "test_empty_working_files.yml": False,
        "test_not_valid_txt_working_files.yml": False,
        "test_valid_hdl_and_asm_working_files.yml": True,
        "test_invalid_test_files.yml": False,
        "test_valid_test_files.yml": True,
    }
    for test_file, valid_result in test_files_dict.items():
        result = configuration_parser.is_valid_configuration_file(
            PROJECT_PATH + "/" + configuration_test_path + "/" + test_file
        )
        if result != valid_result:
            print("Failed configuration file test {}".format(test_file))
        assert result == valid_result


def test_parse_valid_configuration_files() -> None:
    configuration_parser: IConfigurationParser = ConfigurationParser()
    config = configuration_parser.parse_configuration_file(
        PROJECT_PATH
        + "/"
        + configuration_test_path
        + "/"
        + "test_valid_hdl_and_asm_working_files.yml"
    )
    assert config.archive_type == "zip"
    assert len(config.working_files) == 4
    assert len(config.test_files) == 3
    assert "working1.hdl" in config.working_files
    assert "working4.asm" in config.working_files
    assert "test1.tst" in config.test_files


def test_should_not_parse_invalid_configuration_file() -> None:
    configuration_parser: IConfigurationParser = ConfigurationParser()
    with pytest.raises(Exception):
        config = configuration_parser.parse_configuration_file(
            PROJECT_PATH
            + "/"
            + configuration_test_path
            + "/"
            + "test_not_valid_txt_working_files.yml"
        )
