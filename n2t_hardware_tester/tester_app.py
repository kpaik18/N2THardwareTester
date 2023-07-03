import typer

tester_app = typer.Typer()


@tester_app.command()
def dummy_command():
    print("dummy")
