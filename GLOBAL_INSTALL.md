# How to Use Your Command Globally

To use your `gklean` (or renamed) command from **any directory** on your device, you need to install it globally.

Here are the two best ways to do it:

## Method 1: Using `pipx` (Recommended) ⭐

`pipx` installs tools in isolated environments so they don't mess up your system Python packages.

1.  **Install pipx** (if you don't have it):

    ```bash
    brew install pipx
    pipx ensurepath
    ```

    _(Restart your terminal after this)_

2.  **Install your tool**:
    Run this command from inside your project folder:

    ```bash
    pipx install .
    ```

3.  **That's it!**
    Now you can run `gklean` from anywhere.
    ```bash
    cd ~/Desktop
    gklean status
    ```

## Method 2: Global Pip Install

If you don't want to use `pipx`, you can install it directly to your user's Python environment.

1.  **Deactivate your virtual environment** (if active):

    ```bash
    deactivate
    ```

2.  **Install globally**:
    ```bash
    pip install .
    ```
    _Note: If you get a permission error, try `pip install --user .`_

## Updating the Tool

If you make changes to your code, you need to reinstall it for the global command to update.

- For **pipx**: `pipx reinstall gklean` (or your custom name)
- For **pip**: `pip install .` again
