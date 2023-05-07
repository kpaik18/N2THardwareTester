import os

PROJECT_PATH: str = os.getenv("n2t_hardware_tester_project_path")  # type: ignore
N2T_WORK_AREA_PATH: str = os.getenv("n2t_work_area_path")  # type: ignore
TEST_SUCCESS = "End of script - Comparison ended successfully"
