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
