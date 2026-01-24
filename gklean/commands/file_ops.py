import git
from pathlib import Path

def ignore(filename: str):
  """Add a file to .gitignore."""
  # to run this command write :
  #     gklean ignore secret.env
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

def unignore(filename: str):
  """Remove a file from .gitignore."""
  # to run this command write :
  #     gklean unignore secret.env
  try:
    repo = git.Repo(search_parent_directories=True)
    root = Path(repo.working_dir)
    gitignore = root / ".gitignore"
    
    if not gitignore.exists():
      print("Error: .gitignore does not exist.")
      return
      
    content = gitignore.read_text().splitlines()
    if filename not in content:
      print(f"{filename} is not in .gitignore.")
      return
      
    new_content = [line for line in content if line.strip() != filename]
    gitignore.write_text("\n".join(new_content) + "\n")
      
    print(f"Removed {filename} from .gitignore")
  except git.InvalidGitRepositoryError:
    print("Error: Not a git repository.")
  except Exception as e:
    print(f"Error: {e}")
