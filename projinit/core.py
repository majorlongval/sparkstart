"""
core.py – all the heavy lifting for projinit
    • folder scaffold          (src/, README, .gitignore, requirements.txt)
    • local virtual-env        (.venv)
    • git repo + first commit
    • optional --github push   (per-project token in .projinit.env or $GITHUB_TOKEN)

Requires: requests, python-dotenv
    pip install requests python-dotenv
"""

from __future__ import annotations

import os
import pathlib
import shutil
import subprocess
import textwrap
import venv
import webbrowser
from typing import List

import requests
from dotenv import dotenv_values

# ----------------------------------------------------------------------------- #
# Constants                                                                     #
# ----------------------------------------------------------------------------- #

README_TEXT = "# {name}\n\nProject initialized by `projinit`."

GITIGNORE = textwrap.dedent(
    """
    __pycache__/
    .venv/
    *.pyc
    .DS_Store
    .projinit.env
    """
).strip()

NEW_TOKEN_URL = (
    "https://github.com/settings/tokens/new?description=projinit:{name}&scopes=repo,delete_repo,user"
)

# ... (omitted)

    # GitHub remote + push (optional) ------------------------------------
    token: str | None = None
    if github:
        # token preference: .projinit.env  >  $GITHUB_TOKEN  >  prompt user
        token = _project_token(path) or os.getenv("GITHUB_TOKEN", "")
        if not token:
            import typer  # lazy import to avoid hard dependency in library mode

            typer.secho("Opening GitHub to generate a token...", fg=typer.colors.YELLOW)
            webbrowser.open(NEW_TOKEN_URL.format(name=path.name))
            token = typer.prompt(
                "Paste your new GitHub token here (saved to .projinit.env, never committed)"
            )
            _save_project_token(path, token)

    _sh(["git", "init", "-b", "main"], cwd=path)
    _sh(["git", "add", "."], cwd=path)
    _sh(["git", "commit", "-m", "Initial commit"], cwd=path)

    if github:
        repo_url = _create_github_repo(path.name, token)
        # inject token into HTTPS URL for authentication: https://TOKEN@github.com/...
        auth_repo_url = repo_url.replace("https://", f"https://{token}@", 1)

        _sh(["git", "remote", "add", "origin", auth_repo_url], cwd=path)
        _sh(["git", "push", "-u", "origin", "main"], cwd=path)


def delete_project(path: pathlib.Path, github: bool = False) -> None:
    """
    Delete *path* directory; optionally delete its remote GitHub repo.

    Token resolution order:
        1.  .projinit.env inside the project
        2.  $GITHUB_TOKEN
        3.  raise RuntimeError if --github but no token found
    """
    if not path.exists():
        raise RuntimeError(f"{path} does not exist")

    # remove remote first (so local folder still has .projinit.env if needed)
    if github:
        token = _project_token(path) or os.getenv("GITHUB_TOKEN")
        if not token:
            raise RuntimeError(
                "No GitHub token found in .projinit.env or $GITHUB_TOKEN"
            )
        owner = _github_user(token)
        _delete_github_repo(owner, path.name, token)

    # finally delete local directory
    shutil.rmtree(path)
