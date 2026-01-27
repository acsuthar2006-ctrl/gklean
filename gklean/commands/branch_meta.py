import json
import time
from pathlib import Path
from typing import List, Dict, Optional
import git
from enum import Enum
import typer
from rich.console import Console

console = Console()

class BranchStatus(str, Enum):
    WIP = "WIP"
    BLOCKED = "BLOCKED"
    REVIEW = "REVIEW"
    SAFE = "SAFE"

class BranchMeta:
    """
    Manages persistent metadata for git branches.
    Storage: .gklean/branch_meta.json
    """
    
    def __init__(self):
        self.repo_root = self._get_repo_root()
        self.meta_dir = self.repo_root / ".gklean"
        self.meta_file = self.meta_dir / "branch_meta.json"
        self._ensure_storage()
        self.data = self._load()

    def _get_repo_root(self) -> Path:
        try:
            repo = git.Repo(search_parent_directories=True)
            return Path(repo.working_dir)
        except git.InvalidGitRepositoryError:
            return Path.cwd() 

    def _ensure_storage(self):
        if not self.meta_dir.exists():
            self.meta_dir.mkdir(parents=True)
        if not self.meta_file.exists():
            self.meta_file.write_text("{}")

    def _load(self) -> Dict:
        try:
            return json.loads(self.meta_file.read_text())
        except json.JSONDecodeError:
            return {}

    def _save(self):
        self.meta_file.write_text(json.dumps(self.data, indent=2))

    def _get_current_user_name(self) -> str:
        try:
            repo = git.Repo(self.repo_root)
            reader = repo.config_reader()
            return reader.get_value("user", "name", default="unknown")
        except:
            return "unknown"

    def get_branch_data(self, branch_name: str) -> Dict:
        return self.data.get(branch_name, {})

    def set_description(self, branch_name: str, description: str):
        if branch_name not in self.data:
            self._init_branch(branch_name)
        self.data[branch_name]["description"] = description
        self.touch_branch(branch_name)
        self._save()

    def set_status(self, branch_name: str, status: BranchStatus):
        if branch_name not in self.data:
            self._init_branch(branch_name)
        self.data[branch_name]["status"] = status.value
        self.touch_branch(branch_name)
        self._save()

    def add_todo(self, branch_name: str, task: str):
        if branch_name not in self.data:
            self._init_branch(branch_name)
        if "todos" not in self.data[branch_name]:
            self.data[branch_name]["todos"] = []
            
        todo_item = {
            "id": int(time.time() * 1000), 
            "text": task,
            "done": False,
            "created_at": int(time.time())
        }
        self.data[branch_name]["todos"].append(todo_item)
        self.touch_branch(branch_name)
        self._save()

    def touch_branch(self, branch_name: str):
        """Update last_touched and owner if missing"""
        if branch_name not in self.data:
            self._init_branch(branch_name)
        
        self.data[branch_name]["last_touched"] = int(time.time())
        if not self.data[branch_name].get("owner"):
            self.data[branch_name]["owner"] = self._get_current_user_name()
        self._save()

    def _init_branch(self, branch_name: str):
        if branch_name not in self.data:
            self.data[branch_name] = {
                "created_at": int(time.time()),
                "owner": self._get_current_user_name(),
                "status": BranchStatus.WIP.value,
                "todos": [],
                "description": "",
                "last_touched": int(time.time())
            }

    def get_context_str(self, branch_name: str) -> str:
        details = self.get_branch_data(branch_name)
        if not details:
            return ""
            
        status_icon = {
            "WIP": "🚧",
            "BLOCKED": "⛔",
            "REVIEW": "👀",
            "SAFE": "✅"
        }.get(details.get("status", "WIP"), "❓")
        
        owner = details.get("owner", "unknown")
        desc = details.get("description") or "(No description)"
        
        output = [f"{status_icon}  [bold]{branch_name}[/bold] (Owner: {owner})"]
        output.append(f"   📝 {desc}")
        
        todos = details.get("todos", [])
        pending = [t for t in todos if not t["done"]]
        
        if pending:
            output.append(f"   🎯 Pending Tasks: {len(pending)}")
            for t in pending[:3]: 
                output.append(f"      - {t['text']}")
            if len(pending) > 3:
                output.append("      ... and more")
                
        return "\n".join(output)

# CLI Commands
meta = BranchMeta()

def note(message: str):
    """Attach a note/description to the current branch 📝"""
    try:
        repo = git.Repo(search_parent_directories=True)
        current = repo.active_branch.name
        meta.set_description(current, message)
        console.print(f"[green]✔ Note saved for {current}[/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

def todo(task: str):
    """Add a todo item to the current branch ☑️"""
    try:
        repo = git.Repo(search_parent_directories=True)
        current = repo.active_branch.name
        meta.add_todo(current, task)
        console.print(f"[green]✔ Todo added for {current}[/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

def status_cmd(status: BranchStatus):
    """Set the status of the current branch (WIP, BLOCKED, REVIEW, SAFE) 🚦"""
    try:
        repo = git.Repo(search_parent_directories=True)
        current = repo.active_branch.name
        meta.set_status(current, status)
        console.print(f"[green]✔ Status set to {status.value} for {current}[/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

def context():
    """Show context (notes, status, todos) for the current branch 🧠"""
    try:
        repo = git.Repo(search_parent_directories=True)
        current = repo.active_branch.name
        info = meta.get_context_str(current)
        if info:
            console.print(info)
        else:
            console.print(f"[yellow]No memory found for {current}. Use 'gklean note' to add some![/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
