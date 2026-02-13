"""
core.py – all the heavy lifting for sparkstart
    • folder scaffold          (src/, README, .gitignore, etc.)
    • local virtual-env        (.venv) for Python
    • git repo + first commit
    • optional --github push   (per-project token in .projinit.env or $GITHUB_TOKEN)

Requires: requests, python-dotenv
    pip install requests python-dotenv
"""

from __future__ import annotations

import os
import pathlib
import shutil
import webbrowser

from sparkstart.templates.common import README_TEXT, NEW_TOKEN_URL
from sparkstart.templates.cpp import README_CPP

from sparkstart.utils.common import run_shell, get_project_token, save_project_token
from sparkstart.utils.github import create_github_repo, delete_github_repo, get_github_user

from sparkstart.scaffolders.python import scaffold_python
from sparkstart.scaffolders.cpp import scaffold_cpp
from sparkstart.scaffolders.rust import scaffold_rust
from sparkstart.scaffolders.javascript import scaffold_javascript
from sparkstart.scaffolders.devcontainer import scaffold_devcontainer
from sparkstart.scaffolders.direnv import scaffold_direnv
from sparkstart.scaffolders.compose import scaffold_compose
from sparkstart.scaffolders.guides import scaffold_getting_started

from sparkstart.utils.output import print_project_summary


def create_project(
    path: pathlib.Path,
    github: bool = False,
    lang: str = "python",
    devcontainer: bool = False,
    template: str | None = None,
    tutorial: bool = False
) -> None:
    """
    Make a fully-initialised project directory.

    Parameters
    ----------
    path   : pathlib.Path  target directory (must not already exist)
    github : bool          if True, also create & push remote repo
    lang   : str           language: "python", "rust", "javascript", or "cpp"
    devcontainer : bool    if True, generate .devcontainer config
    template     : str     template name (e.g. "pygame") or None
    tutorial     : bool    if True, create educational game project with tests
    """
    # Create project folder
    path.mkdir(parents=False, exist_ok=False)

    # Language-specific scaffolding (tutorial or standard)
    if tutorial:
        from sparkstart.scaffolders.tutorial import (
            scaffold_tutorial_python,
            scaffold_tutorial_rust,
            scaffold_tutorial_javascript,
            scaffold_tutorial_cpp,
        )

        if lang == "python":
            scaffold_tutorial_python(path)
        elif lang == "rust":
            scaffold_tutorial_rust(path)
        elif lang == "javascript":
            scaffold_tutorial_javascript(path)
        elif lang == "cpp":
            scaffold_tutorial_cpp(path)
        else:
            raise ValueError(f"Unknown language: {lang}. Choose: python, rust, javascript, cpp")
    else:
        # Add generic README for standard projects
        if lang == "cpp":
            (path / "README.md").write_text(README_CPP.format(name=path.name))
        else:
            (path / "README.md").write_text(README_TEXT.format(name=path.name))

        # Standard scaffolding
        if lang == "python":
            scaffold_python(path, template)
        elif lang == "rust":
            scaffold_rust(path)
        elif lang == "javascript":
            scaffold_javascript(path)
        elif lang == "cpp":
            scaffold_cpp(path)
        else:
            raise ValueError(f"Unknown language: {lang}. Choose: python, rust, javascript, cpp")

    # Dev Container + supporting configs
    if devcontainer:
        if shutil.which("docker") is None:
            import typer
            typer.secho(
                "WARNING: Docker not found. You need Docker to use Dev Containers.",
                fg=typer.colors.YELLOW
            )
        scaffold_devcontainer(path, lang)
        scaffold_direnv(path, lang)
        scaffold_compose(path, lang)

    # Educational documentation
    scaffold_getting_started(path, path.name, lang, devcontainer)

    # git repository
    if shutil.which("git") is None:
        raise RuntimeError("`git` executable not found in PATH")

    # GitHub remote + push (optional)
    token: str | None = None
    if github:
        # token preference: .projinit.env  >  $GITHUB_TOKEN  >  prompt user
        token = get_project_token(path) or os.getenv("GITHUB_TOKEN", "")
        if not token:
            import typer  # lazy import to avoid hard dependency in library mode

            typer.secho("Opening GitHub to generate a token...", fg=typer.colors.YELLOW)
            webbrowser.open(NEW_TOKEN_URL.format(name=path.name))
            token = typer.prompt(
                "Paste your new GitHub token here (saved to .projinit.env, never committed)"
            )
            save_project_token(path, token)

    run_shell(["git", "init", "-b", "main"], cwd=path)
    run_shell(["git", "add", "."], cwd=path)
    run_shell(["git", "commit", "-m", "Initial commit"], cwd=path)

    if github:
        repo_url = create_github_repo(path.name, token)
        # inject token into HTTPS URL for authentication: https://TOKEN@github.com/...
        auth_repo_url = repo_url.replace("https://", f"https://{token}@", 1)

        run_shell(["git", "remote", "add", "origin", auth_repo_url], cwd=path)
        run_shell(["git", "push", "-u", "origin", "main"], cwd=path)

    # Print friendly summary
    print_project_summary(path, lang, devcontainer, github, tutorial)


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
        token = get_project_token(path) or os.getenv("GITHUB_TOKEN")
        if not token:
            raise RuntimeError(
                "No GitHub token found in .projinit.env or $GITHUB_TOKEN"
            )
        owner = get_github_user(token)
        delete_github_repo(owner, path.name, token)

    # finally delete local directory
    shutil.rmtree(path)
