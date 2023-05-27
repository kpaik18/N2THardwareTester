import os

PROJECT_PATH: str = os.getenv("n2t_hardware_tester_project_path")  # type: ignore
N2T_WORK_AREA_PATH: str = os.getenv("n2t_work_area_path")  # type: ignore
TEST_SUCCESS = "End of script - Comparison ended successfully"
GOOGLE_API_CREDENTIALS: str = os.getenv("google_api_credentials")  # type: ignore
GOOGLE_API_TOKENS_PATH: str = os.getenv("google_api_tokens_path")  # type: ignore
DOWNLOAD_FOLDER: str = os.getenv("n2t_homework_files_download_folder")
