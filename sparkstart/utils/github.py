import os
import requests

def get_github_user(token: str) -> str:
    """Get the authenticated GitHub username."""
    r = requests.get(
        "https://api.github.com/user",
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
        },
        timeout=10,
    )
    if r.status_code >= 300:
        raise RuntimeError(f"GitHub API error {r.status_code}: {r.text.strip()}")
    return r.json()["login"]

def create_github_repo(repo_name: str, token: str | None = None) -> str:
    """
    Create repo under authenticated user; return clone URL.
    *token* optional – falls back to $GITHUB_TOKEN.
    """
    token = token or os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError(
            "GitHub token not provided.\n"
            "Save one in .sparkstart.env, set $GITHUB_TOKEN, or pass --github without a token to be prompted."
        )

    r = requests.post(
        "https://api.github.com/user/repos",
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
        },
        json={"name": repo_name, "private": False},
        timeout=10,
    )
    if r.status_code >= 300:
        raise RuntimeError(f"GitHub API error {r.status_code}: {r.text.strip()}")
    return r.json()["clone_url"]  # e.g. https://github.com/user/repo.git

def delete_github_repo(owner: str, repo_name: str, token: str) -> None:
    """Delete a GitHub repository."""
    r = requests.delete(
        f"https://api.github.com/repos/{owner}/{repo_name}",
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
        },
        timeout=10,
    )
    if r.status_code >= 300:
        raise RuntimeError(f"GitHub API error {r.status_code}: {r.text.strip()}")
