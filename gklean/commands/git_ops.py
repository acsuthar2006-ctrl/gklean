import typer
import git
from git import Repo

def status():
  """Show the git status of the current repository."""
  # to run this command write :
  #     gklean status
  try:
    repo = git.Repo(search_parent_directories=True)
    print(repo.git.status())
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

def commit(message: str):
  """Commit the staged files."""
  # to run this command write :
  #     gklean commit "message"
  try:
    repo = git.Repo(search_parent_directories=True)
    repo.git.commit("-m", message)
    print(f"Committed: {message}")
  except git.InvalidGitRepositoryError:
    print("Error: Not a git repository.")
  except Exception as e:
    print(f"Error: {e}")

def history(n: int = typer.Argument(default=10), file: str = typer.Option(None, "--file", "-f"), oneline: bool = typer.Option(False, "--oneline", "-o")):
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
  """Sync changes with remote (Pull then Push)."""
  # to run this command write :
  #     gklean sync
  try:
    repo = git.Repo(search_parent_directories=True)
    print("Pulling changes...")
    print(repo.git.pull("--rebase"))
    print("Pushing changes...")
    print(repo.git.push())
    print("✅ Synced with remote!")
  except git.InvalidGitRepositoryError:
    print("Error: Not a git repository.")
  except Exception as e:
    print(f"Error: {e}")
