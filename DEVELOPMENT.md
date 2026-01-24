# Development Setup Guide

Welcome to the **gklean** development team! Follow these steps to set up your environment and start coding.

## 1. Prerequisites

Ensure you have the following installed on your system:

- **Python 3.8+**: [Download Here](https://www.python.org/downloads/)
- **Git**: [Download Here](https://git-scm.com/downloads)

## 2. Setting Up the Project

### Clone the Repository

First, get the code on your local machine:

```bash
git clone https://github.com/acsuthar2006-ctrl/gklean.git
cd gklean
```

### Create a Virtual Environment

It's best practice to keep dependencies isolated:

```bash
# Create the virtual environment name '.venv'
python3 -m venv .venv

# Activate it (macOS/Linux)
source .venv/bin/activate

# Activate it (Windows)
# .venv\Scripts\activate
```

### Install Dependencies

Install the project in "editable" mode so changes happen properly:

```bash
pip install -e .
```

This will install `typer`, `gitpython`, and other requirements defined in `pyproject.toml`.

## 3. Running the Tool

You can run the CLI tool directly through Python:

```bash
# Run help command
python gklean/main.py --help

# Run status command
python gklean/main.py status
```

Or, since you installed it with `pip install -e .`, you can use the command directly:

```bash
gklean --help
```

## 4. Contributing

1.  Make your changes in `gklean/main.py`.
2.  Test your changes manually.
3.  Commit and push!

Happy Coding! 🚀
