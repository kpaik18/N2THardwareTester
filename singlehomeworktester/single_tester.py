import os
import shutil
import subprocess
import zipfile
from typing import Protocol

from configuration.configuration import Configuration
from n2tconfig import N2T_WORK_AREA_PATH, TEST_SUCCESS
from singlehomeworktester.test_result import TestResult


class ISingleHomeworkTester(Protocol):
    def test_homework(
        self, archive_path: str, config: Configuration, homework_name: str
    ) -> TestResult:
        pass


class SingleHomeworkTester:
    def test_homework(
        self, archive_path: str, config: Configuration, homework_name: str
    ) -> TestResult:
        extracted_folder_path = self._unzip_archive_get_extract_folder_path(
            archive_path, config.archive_type
        )
        self._remove_working_files_from_hw_project(config.working_files, homework_name)
        self._copy_working_files_to_project(
            extracted_folder_path, config.working_files, homework_name
        )
        return self._run_tests_and_grade(config.test_files, homework_name)

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
        hw_project_path = os.path.join(N2T_WORK_AREA_PATH, "projects", homework_name)
        for w_file in working_files:
            working_file_path = os.path.join(hw_project_path, w_file)
            try:
                os.remove(working_file_path)
            except:
                pass

    def _copy_working_files_to_project(
        self, extracted_folder_path, working_files, homework_name
    ):
        hw_project_path = os.path.join(N2T_WORK_AREA_PATH, "projects", homework_name)
        for w_file in working_files:
            w_file_path = os.path.join(extracted_folder_path, w_file)
            if not os.path.exists(w_file_path):
                with open(w_file_path, "w") as f:
                    pass
            shutil.copy(w_file_path, hw_project_path)

    def _run_tests_and_grade(self, test_files, homework_name) -> TestResult:
        command = "HardwareSimulator"
        hw_project_path = os.path.join(N2T_WORK_AREA_PATH, "projects", homework_name)
        success_count = 0
        for t_file in test_files:
            full_test_command = command + " " + t_file
            result = subprocess.check_output(
                full_test_command,
                shell=True,
                cwd=hw_project_path,
                universal_newlines=True,
            )
            if result.strip() == TEST_SUCCESS:
                success_count += 1
        return TestResult(len(test_files), success_count)
