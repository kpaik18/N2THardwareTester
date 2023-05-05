import os
import zipfile
from typing import Protocol

from configuration.configuration import Configuration
from n2tconfig import N2T_WORK_AREA_PATH


class ISingleHomeworkTester(Protocol):
    def test_homework(
        self, archive_path: str, config: Configuration, homework_name: str
    ) -> None:
        pass


class SingleHomeworkTester:
    def test_homework(
        self, archive_path: str, config: Configuration, homework_name: str
    ) -> None:
        extracted_folder_path = self._unzip_archive_get_extract_folder_path(
            archive_path, config.archive_type
        )
        self._remove_working_files_from_hw_project(config.working_files, homework_name)

    def _unzip_archive_get_extract_folder_path(
        self, archive_path: str, archive_type: str
    ) -> str:
        directory_path, filename = os.path.split(archive_path)
        extract_path_folder_name = filename[: filename.rfind(".")]
        extract_path = os.path.join(directory_path, extract_path_folder_name)
        if archive_type == "zip":
            with zipfile.ZipFile(archive_path, "r") as zip_ref:
                zip_ref.extractall(extract_path)
        return extract_path

    def _remove_working_files_from_hw_project(self, working_files, homework_name):
        hw_project_path = os.path.join(N2T_WORK_AREA_PATH, 'projects', homework_name)
        pass
