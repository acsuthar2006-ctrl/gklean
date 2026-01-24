import typer
import git

app = typer.Typer()

# This is a simple CLI tool , which does not make any sense
@app.command()
def hello(name: str = ""):
  if name == "":
    print("To Kaise Ho Aap Log!!")
    return
  print(f"Hello Topper!! ---> {name}")

@app.command()
def goodbye(name: str, formal: bool = False):
  if formal:
    print(f"Goodbye Mr. {name}. Have a good day.")
  else:
    print(f"Bye {name}!")

from .commands import status, save, rename

app.command()(status)
app.command()(save)
app.command()(rename)

if __name__ == "__main__":
  app()
