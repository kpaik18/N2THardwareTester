from main import PROJECT_PATH

from configuration.configuration import ConfigurationParser, IConfigurationParser


def test_configuration_files_validity() -> None:
    configuration_parser: IConfigurationParser = ConfigurationParser()
    context_path = "test/configuration/test_config_files"
    test_files_dict = {'test_empty_archive.yml': False,
                       'test_rar_archive.yml': False,
                       'test_valid_zip_archive.yml': True,
                       'test_empty_working_files.yml': False,
                       "test_not_valid_txt_working_files.yml": False,
                       "test_valid_hdl_and_asm_working_files.yml": True,
                       "test_invalid_test_files.yml": False,
                       "test_valid_test_files.yml": True}
    for test_file, valid_result in test_files_dict.items():
        result = configuration_parser.is_valid_configuration_file(PROJECT_PATH + "/"
                                                                  + context_path
                                                                  + "/" + test_file)
        if result != valid_result:
            print("Failed configuration file test {}".format(test_file))
        assert result == valid_result
