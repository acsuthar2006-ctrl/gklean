import typer
import git

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

def ignore(filename: str):
  """Add a file to .gitignore."""
  # to run this command write :
  #     gklean ignore secret.env
  from pathlib import Path
  try:
    repo = git.Repo(search_parent_directories=True)
    root = Path(repo.working_dir)
    gitignore = root / ".gitignore"
    
    if not gitignore.exists():
      gitignore.touch()
      
    content = gitignore.read_text()
    if filename in content:
      print(f"{filename} is already likely ignored.")
      return
      
    with gitignore.open("a") as f:
      f.write(f"\n{filename}")
      
    print(f"Added {filename} to .gitignore")
  except git.InvalidGitRepositoryError:
    print("Error: Not a git repository.")
  except Exception as e:
    print(f"Error: {e}")

def rename(new_name: str):
  """Rename the CLI command (modifies pyproject.toml). requires reinstall."""
  import re
  import sys
  import subprocess
  from pathlib import Path

  try:
    # Search for pyproject.toml in current and parent directories
    current_path = Path.cwd()
    pyproject_path = None
    
    for parent in [current_path] + list(current_path.parents):
      temp_path = parent / "pyproject.toml"
      if temp_path.exists():
        pyproject_path = temp_path
        break
        
    if not pyproject_path:
      print("Error: pyproject.toml not found in current or parent directories.")
      return

    content = pyproject_path.read_text()
    
    # Regex to find the entry point line: e.g. gklean = "gklean.main:app"
    # We look for ANY_KEY = "gklean.main:app"
    pattern = r'^(\s*).*?(\s*=\s*"gklean\.main:app")'
    
    if not re.search(pattern, content, re.MULTILINE):
       print("Error: Could not find strict entry point definition in pyproject.toml")
       return

    # Replace the whole line with "new_name = ..." preserving indentation
    new_content = re.sub(
      pattern, 
      fr'\1{new_name}\2', 
      content, 
      flags=re.MULTILINE
    )

    pyproject_path.write_text(new_content)
    
    print(f" Renamed command to '{new_name}' in pyproject.toml")
    print(" Installing changes... (running pip install -e .)")
    
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", str(pyproject_path.parent)])
    
    print(f"✅ Success! You can now use '{new_name}' command.")
    
  except Exception as e:
    print(f"Error: {e}")
