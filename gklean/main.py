import typer
import git
from .commands import status, save, commit , history ,rename

app = typer.Typer()

app.command()(status)
app.command()(save)
app.command()(commit)
app.command()(rename)
app.command()(history)

if __name__ == "__main__":
  app()
