# Typer Concepts: Arguments vs Options

For my friend who wants to master CLI building with Python's **Typer**.

## The "Default Value" Gotcha

In Typer, how you define your function parameters determines if they become **CLI Arguments** (positional) or **CLI Options** (flags like `--name`).

### 1. The Trap ❌

If you give a parameter a simple Python default value, Typer guesses you want an **Option**.

```python
# CODE
def save(name: str = "."):
    ...

# CLI BEHAVIOR
# $ gklean save            <-- Works (name=".")
# $ gklean save temp.txt   <-- FAILS! "Got unexpected extra argument"
# $ gklean save --name temp.txt  <-- Typer expects this instead
```

Because `name` had a default, Typer assumed it was an _optional flag_ (`--name`), not a positional input.

### 2. The Fix ✅

If you want an argument to be **Positional** _and_ have a **Default Value**, you must explicitly tell Typer using `typer.Argument`.

```python
import typer

# CODE
def save(name: str = typer.Argument(default=".")):
    ...

# CLI BEHAVIOR
# $ gklean save            <-- Works (name=".")
# $ gklean save temp.txt   <-- Works! (name="temp.txt")
```

## Summary Table

| Code                              | CLI Type                | Usage Example      |
| :-------------------------------- | :---------------------- | :----------------- |
| `name: str`                       | **Argument** (Required) | `cmd value`        |
| `name: str = "default"`           | **Option** (Optional)   | `cmd --name value` |
| `name: str = typer.Argument(...)` | **Argument** (Optional) | `cmd [value]`      |
