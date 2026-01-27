import typer
import git
from rich.console import Console
from rich.panel import Panel
from .branch_meta import BranchMeta, BranchStatus

console = Console()

def create_branch(name: str):
    """Create a new branch """
    try:
        repo = git.Repo(search_parent_directories=True)
        new_branch = repo.create_head(name)
        console.print(f"[green]✔ Created branch: {name}[/green]")
        
        # Optional: Ask to checkout
        if typer.confirm(f"Switch to {name}?"):
            repo.git.checkout(name)
            console.print(f"[green]Switched to {name}[/green]")
            
    except git.InvalidGitRepositoryError:
        console.print("[bold red]Error: Not a git repository.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error creating branch: {e}[/bold red]")

def delete_branch(name: str):
    """Delete a branch """
    try:
        repo = git.Repo(search_parent_directories=True)
        
        # Check if it exists
        if name not in repo.heads:
            console.print(f"[bold red]Error: Branch '{name}' does not exist.[/bold red]")
            return

        # Check if we are currently on it
        if repo.active_branch.name == name:
             console.print(f"[bold red]Cannot delete the active branch '{name}'. Switch to another branch first.[/bold red]")
             return
             
        # Ask for confirmation
        if typer.confirm(f"Are you sure you want to delete branch '{name}'?"):
             repo.delete_head(name, force=True)
             console.print(f"[green]✔ Deleted branch: {name}[/green]")
        else:
             console.print("[yellow]Operation cancelled.[/yellow]")

    except git.InvalidGitRepositoryError:
        console.print("[bold red]Error: Not a git repository.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error deleting branch: {e}[/bold red]")

def switch_branch(name: str):
    """Jump to another branch 🦘"""
    try:
        repo = git.Repo(search_parent_directories=True)
        
        # Check if it exists
        if name not in repo.heads:
            console.print(f"[bold red]Error: Branch '{name}' does not exist.[/bold red]")
            # Optional: Ask to create it?
            if typer.confirm(f"Branch '{name}' not found. Sprout it?"):
                create_branch(name)
            return

        # Checkout
        repo.git.checkout(name)
        console.print(f"[green]✔ Jumped to branch: {name}[/green]")
        
        # Show Context
        try:
             meta = BranchMeta()
             context = meta.get_context_str(name)
             if context:
                 console.print(Panel(context, title="Branch Context", border_style="blue"))
        except:
             pass

    except git.InvalidGitRepositoryError:
        console.print("[bold red]Error: Not a git repository.[/bold red]")

def list_branches():
    """List all branches """
    try:
        repo = git.Repo(search_parent_directories=True)
        current = repo.active_branch.name
        
        console.print("[bold]Branches:[/bold]")
        
        meta = BranchMeta()
        
        for head in repo.heads:
            data = meta.get_branch_data(head.name)
            
            # determine icon
            status_val = data.get("status", "WIP")
            icon = {
                "WIP": "🚧",
                "BLOCKED": "⛔", 
                "REVIEW": "👀",
                "SAFE": "✅"
            }.get(status_val, "❓")
            
            # detailed suffix
            desc = data.get("description", "")
            if desc:
                desc = f"[dim]- {desc}[/dim]"
                
            if head.name == current:
                console.print(f"  [bold green]* {icon} {head.name}[/bold green] {desc}")
            else:
               console.print(f"    {icon} {head.name} {desc}")

    except git.InvalidGitRepositoryError:
        console.print("[bold red]Error: Not a git repository.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error listing branches: {e}[/bold red]")
