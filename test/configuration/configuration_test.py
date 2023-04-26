from configuration.configuration import ConfigurationParser


def test_simple_configuration() -> None:
    configuration_parser = ConfigurationParser()
    config = configuration_parser.parse_configuration_file('test/configuration/test_config_files/test_env_1.yml')
    assert True
