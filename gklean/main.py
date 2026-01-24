import typer
import git
from .commands import status, save, commit , rename

app = typer.Typer()

app.command()(status)
app.command()(save)
app.command()(commit)
app.command()(rename)

if __name__ == "__main__":
  app()
