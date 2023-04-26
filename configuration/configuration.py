from dataclasses import dataclass
from typing import List


@dataclass
class Configuration:
    archive_type: str
    working_files: List[str]
    test_files: List[str]


class IConfigurationParser:
    def parse_configuration_file(self, configuration_file_path: str) -> Configuration:
        pass


class ConfigurationParser:
    def parse_configuration_file(self, configuration_file_path: str) -> Configuration:
        pass
