import os

PROJECT_PATH: str = os.getenv("n2t_hardware_tester_project_path")  # type: ignore


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f"Hi, {name}")  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    print_hi("N2T Hardware Tester")
