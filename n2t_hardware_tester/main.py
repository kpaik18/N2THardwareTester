import typer

from n2t_hardware_tester.test_pack.test import test_function

tester_app = typer.Typer()


@tester_app.command()
def dummy_command():
    print("dummy")


@tester_app.command()
def other_command():
    print("other")
    test_function()


if __name__ == "__main__":
    tester_app()
    # print("Startuppp")
    # app()
    # print("start up ")
    # grade_homework(
    #     Homework.h5,
    #     "NTk1MzUxNTE3MjE4",
    #     "NTUyNTg2NjM4NTI1",
    #     "15jXXLvv4yTthiHvqEwJM3hcex--iEvOu",
    # )
