import typer
import git

app = typer.Typer()

# This is a simple CLI tool , which does not make any sense
@app.command()
def hello(name: str = ""):
  if name == "":
    print("To Kaise Ho Aap Log!!")
    return
  print(f"Hello Topper!! ---> {name}")

@app.command()
def goodbye(name: str, formal: bool = False):
  if formal:
    print(f"Goodbye Mr. {name}. Have a good day.")
  else:
    print(f"Bye {name}!")

@app.command()
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

@app.command()
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


if __name__ == "__main__":
  app()
