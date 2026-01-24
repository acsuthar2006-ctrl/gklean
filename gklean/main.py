import typer

app = typer.Typer()

@app.command()
def hello(name: str):
    print(f"Hello {name}")


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Mr. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


if __name__ == "__main__":
    app()

#  how to use this file
#  python main.py --help
#  python main.py hello <name>
#  python main.py goodbye <name> --formal