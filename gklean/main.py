import typer
import git
from .commands import init, status, save, commit, history, undo, sync, ignore, unignore, rename, changes, review, create_branch, delete_branch, switch_branch, list_branches, note, todo, context

app = typer.Typer()

app.command()(init)
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
app.command(name="sprout")(create_branch)
app.command(name="prune")(delete_branch)
app.command(name="jump")(switch_branch)
app.command(name="branches")(list_branches)
app.command()(note)
app.command()(todo)
app.command()(context)

if __name__ == "__main__":
  app()
