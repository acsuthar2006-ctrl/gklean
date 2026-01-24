import typer
import git
from rich.console import Console

app = typer.Typer(help="gklean: Git for humans.")
console = Console()

@app.command()
def hello():
    """
    Say hello to verify gklean is working.
    """
    console.print("[bold green]Hello! gklean is ready to help.[/bold green] :broom:")

@app.command()
def save(message: str = typer.Argument(..., help="What did you change?")):
    """
    Save your work (add & commit).
    Usage: gklean save "Fixed the bug"
    """
    try:
        repo = git.Repo(".")
        
        # 1. Add all changes
        repo.git.add(".")
        
        # 2. Commit
        repo.index.commit(message)
        
        console.print(f"[bold green]Saved! :white_check_mark:[/bold green] '{message}'")
        
    except git.exc.InvalidGitRepositoryError:
        console.print("[bold red]Error:[/bold red] Not a git repository. Run `git init` or `gklean setup` first.")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")

if __name__ == "__main__":
    app()
