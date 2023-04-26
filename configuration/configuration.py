from dataclasses import dataclass
from typing import List
import yaml


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
        with open("example.yml", "r") as f:
            data = yaml.safe_load(f)

        print(data)
