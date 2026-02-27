# gklean 🧹

**Version control without the fear.**

Git is powerful but intimidating. `gklean` is a command-line wrapper that turns complex Git workflows into simple, human-readable commands. It handles the messy details (like rebasing, stashing, and conflict detection) so you can focus on code.

## ✨ Features

### 🔍 Interactive Review (`gklean review`)
Never blindly `git add .` again.
- **Visual**: See syntax-highlighted diffs in a clear panel.
- **Interactive**: Decide file-by-file what to stage.
- **Smart**: Detects untracked files and asks if you want to add them.

### 📊 Beautiful Status (`gklean changes`)
A better `git diff`.
- **Summary Table**: See a high-level table of Modified vs Untracked files before the diff.
- **Highlighted**: Changes are color-coded using the Monokai theme.
- **Filters**: Quickly see changes for a specific file (`-f`) or just staged ones (`--staged`).

### 🔄 Smart Sync (`gklean sync`)
Stop worrying about "pull before push".
- **Auto-Stash**: Automatically stashes uncommitted changes if needed.
- **Rebase Pull**: Pulls with rebase to keep history clean.
- **Safe Pop**: Restores your work after the pull.
- **Push**: Sends your commits to the remote.

### 🌱 Branch Intelligence
Manage branches and context without losing your mind.
- **`gklean sprout <name>`**: Create a new branch.
- **`gklean prune <name>`**: Delete a branch safely.
- **`gklean jump <name>`**: Switch branches quickly.
- **`gklean branches`**: View all branches with beautiful status icons.
- **`gklean status <state>`**: Set branch status (`WIP`, `BLOCKED`, `REVIEW`, `SAFE`).
- **`gklean note <msg>`**: Attach notes/descriptions to your current branch.
- **`gklean todo <task>`**: Add todo items linked to your branch.
- **`gklean context`**: View all context, notes, and todos for your current branch.

### 🛡️ Safety Nets & Utilities
- **`gklean init`**: Initialize a new repository.
- **`gklean save`**: Stage files (defaults to all files).
- **`gklean commit "msg"`**: Safely commit your changes.
- **`gklean history`**: View recent commits with ease.
- **`gklean undo`**: Soft resets the last commit (keeps your work, just undoes the commit).
- **`gklean reword <commit_id> "new message"`**: Change the commit message for a specific commit.
- **`gklean ignore <file>`**: Easily add files to `.gitignore` without opening it.
- **`gklean unignore <file>`**: Remove files from `.gitignore`.
- **`gklean rename <name>`**: Rename the CLI command itself!

## 🚀 Usage

```bash
# Start your day
gklean sync

# Check what you did
gklean changes

# Ready to commit? Review line-by-line
gklean review

# Save valid changes
gklean commit "feat: my new cool feature"

# Fix a commit message
gklean reword <commit_id> "better message"
```

## 🛠️ Installation

```bash
pip install gklean
```

*(Requires Python 3.9+ and Git)*
