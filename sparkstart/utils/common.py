import pathlib
import subprocess
import os
from dotenv import dotenv_values
from typing import List

def run_shell(cmd: List[str], cwd: pathlib.Path) -> None:
    """Run *cmd* in *cwd*; raise RuntimeError on non-zero exit."""
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"$ {' '.join(cmd)}\n{result.stderr.strip() or 'command failed'}"
        )

def get_project_token(project_root: pathlib.Path) -> str | None:
    """Return token from .sparkstart.env or '' if file missing/empty."""
    return dotenv_values(project_root / ".sparkstart.env").get("GITHUB_TOKEN", "")

def save_project_token(project_root: pathlib.Path, token: str | None) -> None:
    """Persist token to .sparkstart.env and ensure it's git-ignored."""
    (project_root / ".sparkstart.env").write_text(f"GITHUB_TOKEN={token}\n")

    gi = project_root / ".gitignore"
    lines: list[str] = gi.read_text().splitlines() if gi.exists() else []
    if ".sparkstart.env" not in lines:
        lines.append(".sparkstart.env")
        gi.write_text("\n".join(lines) + "\n")
