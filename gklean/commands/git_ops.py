import typer
import git
from git import Repo
from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table
from rich.panel import Panel

console = Console()


def init(directory: str = typer.Argument(".", help="Directory to initialize (default: current)")):
  """Initialize a new git repository 🐣"""
  # to run this command write:
  #     gklean init
  try:
    # Check if already a repo
    try:
      _ = git.Repo(directory, search_parent_directories=False)
      console.print(f"[yellow]⚠️  Git repository already exists in {directory}[/yellow]")
      return
    except (git.InvalidGitRepositoryError, git.NoSuchPathError):
      pass # Good, we can create one

    # Initialize
    repo = git.Repo.init(directory)
    console.print(f"[green]✔ Initialized empty Git repository in {repo.working_dir}[/green]")
    
  except Exception as e:
    console.print(f"[bold red]Error: {e}[/bold red]")

from .branch_meta import BranchMeta, BranchStatus

def status(state: str = typer.Argument(None, help="Optional: Set branch status (WIP, BLOCKED, REVIEW, SAFE)"), 
           msg: str = typer.Argument(None, help="Optional: Description message")):
  """Show git status OR set branch status (e.g. 'gklean status BLOCKED')."""
  # to run this command write :
  #     gklean status
  #     gklean status BLOCKED "Waiting for API"
  
  if state:
    # Branch Memory Mode
    try:
      meta = BranchMeta()
      
      # Normalize input
      state_upper = state.upper()
      if state_upper in BranchStatus.__members__:
         repo = git.Repo(search_parent_directories=True)
         current = repo.active_branch.name
         
         meta.set_status(current, BranchStatus[state_upper])
         if msg:
             meta.set_description(current, msg)
             
         console.print(f"[green]✔ Status set to {state_upper} for {current}[/green]")
         if msg:
             console.print(f"[green]✔ Note saved: {msg}[/green]")
      else:
         console.print(f"[red]Invalid status. Options: {', '.join(BranchStatus.__members__.keys())}[/red]")
         
    except Exception as e:
      console.print(f"[red]Error: {e}[/red]")
    return

  # Git Status Mode (Default)
  try:
    repo = git.Repo(search_parent_directories=True)
    print(repo.git.status())
    
    # Show Context if available (Bonus)
    try:
        meta = BranchMeta()
        context_str = meta.get_context_str(repo.active_branch.name)
        if context_str:
            print("\n" + context_str)
    except:
        pass
        
  except git.InvalidGitRepositoryError:
    print("Error: Not a git repository.")
  except Exception as e:
    print(f"Error: {e}")

def save(name: str = typer.Argument(default=".")):
  """Stage files for commit. Defaults to all files ('.')."""
  # to run this command write :
  #     gklean save
  try:
    repo = git.Repo(search_parent_directories=True)
    repo.git.add(name)
    
    if name == "." : 
      name = "All files"
    print(f"Staged: {name}")
    
  except git.InvalidGitRepositoryError:
    print("Error: Not a git repository.")
  except Exception as e:
    print(f"Error: {e}")

from .safety_feature import check_branch_safety

def commit(message: str):
  """Commit the staged files."""
  # to run this command write :
  #     gklean commit "message"
  
  # Safety Check first!
  if not check_branch_safety():
    return

  try:
    repo = git.Repo(search_parent_directories=True)
    repo.git.commit("-m", message)
    console.print(f"[green]Committed: {message}[/green]")
  except git.InvalidGitRepositoryError:
    console.print("[bold red]Error: Not a git repository.[/bold red]")
  except Exception as e:
    console.print(f"[bold red]Error: {e}[/bold red]")

def history(n: int = typer.Argument(default=10), file: str = typer.Option(None, "--file", "-f"), oneline: bool = typer.Option(False, "--oneline", "-ol")):
  """Show the git history of the current repository."""
  # to run this command write :
  #     gklean history
  #     gklean history --oneline
  #     gklean history --file main.py
  try:
    repo = git.Repo(search_parent_directories=True)
    args = ["-n", str(n)]
    if oneline:
      args.append("--oneline")
    if file:
      args.append("--full-history")
      args.append(file)
    print(repo.git.log(*args))
  except git.InvalidGitRepositoryError:
    print("Error: Not a git repository.")
  except Exception as e:
    print(f"Error: {e}")

def undo():
  """Undo the last commit (keeps changes in staging area)."""
  # to run this command write :
  #     gklean undo
  try:
    repo = git.Repo(search_parent_directories=True)
    repo.git.reset("--soft", "HEAD~1")
    print("Undid last commit. Changes are now staged.")
  except git.InvalidGitRepositoryError:
    print("Error: Not a git repository.")
  except Exception as e:
    print(f"Error: {e}")

def sync():
  """Sync changes with remote (Auto-Stash -> Pull --rebase -> Pop -> Push)."""
  # to run this command write :
  #     gklean sync
  try:
    repo = git.Repo(search_parent_directories=True)
    
    # Check if remote exists
    if not repo.remotes:
        console.print("[yellow]No remote found. Skipping sync (pull/push).[/yellow]")
        return

    # Check tracking
    active_branch = repo.active_branch
    tracking_branch = active_branch.tracking_branch()
    
    if tracking_branch:
        # Existing Logic: Full Sync
        # helper to check if dirty
        is_dirty = repo.is_dirty() or len(repo.untracked_files) > 0
        stashed = False
        
        if is_dirty:
          print(" Uncommitted changes detected. Stashing them...")
          repo.git.stash("save", "gklean-auto-stash")
          stashed = True
          
        print(" Pulling changes (rebase)...")
        repo.git.pull("--rebase")
        
        if stashed:
          print(" Popping stash...")
          try:
            repo.git.stash("pop")
          except git.GitCommandError:
            print("⚠️  Conflict during stash pop. Please resolve conflicts manually.")
            return

        print(" Pushing changes...")
        repo.git.push()
        
    else:
        # New Branch Logic
        console.print(f"[yellow]Branch '{active_branch.name}' has no upstream. Skipping pull.[/yellow]")
        console.print(f" Pushing '{active_branch.name}' to 'origin'...")
        repo.git.push("--set-upstream", "origin", active_branch.name)

    print(" Synced with remote!")
    
  except git.InvalidGitRepositoryError:
    print("Error: Not a git repository.")
  except Exception as e:
    print(f"Error: {e}")
 
def changes(
    staged: bool = typer.Option(False, "--staged", "-s", help="Show staged changes"), 
    file: str = typer.Option(None, "--file", "-f", help="Show changes for specific file"),
    name_only: bool = typer.Option(False, "--name-only", "-n", help="Show only names of changed files")
):
  """Show changes in the repository (including untracked)."""
  
  try : 
    repo = git.Repo(search_parent_directories=True)

    args = []
    if staged:
      args.append("--staged")
    if name_only:
      args.append("--name-only")
    if file:
      args.append(file)

    output = repo.git.diff(*args)
    if output:
      syntax = Syntax(output, "diff", theme="monokai", line_numbers=True)
      console.print(syntax)
    else:
      if not file:
         console.print("[dim]No modified files.[/dim]")

    # 3. Show Untracked (Bonus Feature!)
    # We only show this if we aren't asking for staged/specific files
    if not staged and not file and not name_only:
       untracked = repo.untracked_files
       if untracked:
         console.print("\n[bold yellow]Untracked files:[/bold yellow]")
         for f in untracked:
           console.print(f"[red]?? {f}[/red]")
       
  except git.InvalidGitRepositoryError:
    console.print("[bold red]Error: Not a git repository.[/bold red]")
  except Exception as e:
    console.print(f"[bold red]Error: {e}[/bold red]")

def review():
  """Interactive diff and staging (The 'Check' Solution)."""
  # to run this command write:
  #     gklean review
  try:
     repo = git.Repo(search_parent_directories=True)
     
     # Get all modified files
     diffs = repo.index.diff(None) # Unstaged changes
     untracked = repo.untracked_files
     
     if not diffs and not untracked:
       console.print("[green]Nothing to review![/green]")
       return

     # Handle Modified Files
     for diff_item in diffs:
       filename = diff_item.a_path
       console.clear() # Clear screen for focus
       
       # Prominent Header
       console.print(Panel(f"[bold blue]{filename}[/bold blue]", title="Reviewing Modified File", border_style="blue"))
       
       # Show diff for this specific file
       diff_output = repo.git.diff(filename)
       if diff_output:
          syntax = Syntax(diff_output, "diff", theme="monokai", line_numbers=True)
          console.print(syntax)
       
       console.print("\n[bold]Options:[/bold] [green](y)es[/green], [red](n)o[/red], [dim](q)uit[/dim]")
       choice = typer.prompt("Stage this file? ", default="n")
       if choice.lower() == 'y':
         repo.git.add(filename)
         console.print(f"[green]✔ Staged {filename}[/green]")
       elif choice.lower() == 'q':
         return
       else:
          console.print(f"[yellow]Skipped {filename}[/yellow]")

     # Handle Untracked Files
     for filename in untracked:
       console.clear()
       console.print(Panel(f"[bold yellow]{filename}[/bold yellow]", title="Reviewing Untracked File", border_style="yellow"))
       
       # preview content (first 10 lines)
       try:
         with open(filename, 'r') as f:
           head = "".join([next(f) for _ in range(10)])
           syntax = Syntax(head, "python", theme="monokai", line_numbers=False) 
           console.print(syntax)
           console.print("[dim]... (end of preview)[/dim]")
       except:
         console.print("[dim](Binary or unreadable content)[/dim]")

       console.print("\n[bold]Options:[/bold] [green](y)es[/green], [red](n)o[/red], [dim](q)uit[/dim]")
       choice = typer.prompt(f"Track (add) this file? ", default="n")
       if choice.lower() == 'y':
         repo.git.add(filename)
         console.print(f"[green]✔ Added {filename}[/green]")
       elif choice.lower() == 'q':
         return
       else:
          console.print(f"[yellow]Skipped {filename}[/yellow]")
         
     console.print("\n[bold green]Review complete![/bold green]")
     
  except git.InvalidGitRepositoryError:
    console.print("[bold red]Error: Not a git repository.[/bold red]")
  except Exception as e:
    console.print(f"[bold red]Error: {e}[/bold red]")

