from dataclasses import dataclass
from typing import Any, Dict, List, Protocol

import yaml

VALID_WORKING_FILE_EXTENSIONS = {"hdl", "asm"}
VALID_TEST_FILE_EXTENSIONS = {"tst"}
VALID_TESTER_PROGRAMS = {"HardwareSimulator", "CPUEmulator"}


@dataclass
class Configuration:
    archive_type: str
    working_files: List[str]
    test_files: List[str]
    tester_program: str
    homework_name: str


class IConfigurationParser(Protocol):
    def parse_configuration_file(self, configuration_file_path: str) -> Configuration:
        pass

    def is_valid_configuration_file(self, configuration_file_path: str) -> bool:
        pass


class ConfigurationParser:
    def parse_configuration_file(self, configuration_file_path: str) -> Configuration:
        with open(configuration_file_path, "r") as f:
            data = yaml.safe_load(f)
        if not self._is_valid_configuration_data(data):
            raise Exception("not_valid_configuration_file")
        return Configuration(
            data["archive_type"],
            data["working_files"],
            data["test_files"],
            data["tester_program"],
            data["homework_name"],
        )

    def is_valid_configuration_file(self, configuration_file_path: str) -> bool:
        with open(configuration_file_path, "r") as f:
            data = yaml.safe_load(f)
        return self._is_valid_configuration_data(data)

    def _is_valid_configuration_data(self, data: Dict[Any, Any]) -> bool:
        if "archive_type" not in data or data["archive_type"] != "zip":
            return False
        if "homework_name" not in data:
            return False
        if (
            "tester_program" not in data
            or data["tester_program"] not in VALID_TESTER_PROGRAMS
        ):
            return False
        if "working_files" not in data:
            return False
        working_files = data["working_files"]
        for w_file in working_files:
            extension = w_file[w_file.rfind(".") + 1 :]
            if extension not in VALID_WORKING_FILE_EXTENSIONS:
                return False
        if "test_files" not in data:
            return False
        test_files = data["test_files"]
        for t_file in test_files:
            extension = t_file[t_file.rfind(".") + 1 :]
            if extension not in VALID_TEST_FILE_EXTENSIONS:
                return False
        return True
