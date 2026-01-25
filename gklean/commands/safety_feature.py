import typer
import git
from rich.console import Console

console = Console()

def check_branch_safety():
    """
    Checks if it is safe to commit on the current branch.
    Returns True if safe, False if unsafe (and user opted not to override).
    """
    try:
        repo = git.Repo(search_parent_directories=True)
        current_branch = repo.active_branch.name

        # Protected branches
        protected = ["main", "master", "production"]

        if current_branch in protected:
            console.print(f"[bold red]⛔ SAFETY WARNING: You are on the '{current_branch}' branch![/bold red]")
            console.print("Direct commits to main are discouraged. Use a feature branch instead.")
            
            choice = typer.prompt("Are you sure you want to proceed? [y/N]", default="N")
            if choice.lower() != 'y':
                console.print("[yellow]Aborted commit for safety.[/yellow]")
                return False
        
        return True

    except Exception:
        # If we can't check, fail open (safe) or closed depending on philosophy. 
        # Here we assume it's fine if we can't determine.
        return True
