import typer
import git
from .commands import status, save, commit, history, undo, sync, ignore, unignore, rename, changes, review

app = typer.Typer()

app.command()(status)
app.command()(save)
app.command()(commit)
app.command()(history)
app.command()(undo)
app.command()(sync)
app.command()(ignore)
app.command()(unignore)
app.command()(rename)
app.command()(changes)
app.command()(review)

if __name__ == "__main__":
  app()
