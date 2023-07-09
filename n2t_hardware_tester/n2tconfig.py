import os

PROJECT_PATH: str = os.getenv("n2t_hardware_tester_project_path")  # type: ignore
N2T_WORK_AREA_PATH: str = os.getenv("n2t_work_area_path")  # type: ignore
TEST_SUCCESS = "End of script - Comparison ended successfully"
TIMESTAMP_NOT_FOUND_VALUE_LATE_DAYS = 99999
GOOGLE_API_CREDENTIALS: str = os.getenv("n2t_google_api_credentials")  # type: ignore
GOOGLE_API_TOKENS_PATH: str = os.getenv("n2t_google_api_tokens_path")  # type: ignore
DOWNLOAD_FOLDER: str = os.getenv("n2t_homework_files_download_folder")  # type: ignore

env_variables_for_student = [N2T_WORK_AREA_PATH]
env_variables_for_lecturer = [N2T_WORK_AREA_PATH, GOOGLE_API_CREDENTIALS, GOOGLE_API_TOKENS_PATH, DOWNLOAD_FOLDER]

env_variable_names = ['n2t_work_area_path', 'n2t_google_api_credentials', 'n2t_google_api_tokens_path', 'n2t_homework_files_download_folder']

env_variable_description = {
    "n2t_work_area_path": """Path of nand2tetris directory which contains tools and project folder for the course, 
    for example -> C:/Users/StudentName/nand2tetris
    """,
    'n2t_google_api_credentials': "path of google classroom api Credentials file for google authentication, must be downloaded from google cloud console",
    'n2t_google_api_tokens_path': "path of google classroom api token path. token file is not necessary, will be downloaded automatically after login",
    'n2t_homework_files_download_folder': "path of download folder, where student assignment attachments will be downloaded",
}
