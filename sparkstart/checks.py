
import shutil
import typer
import webbrowser
import sys

def open_url(url: str):
    """Open a URL in the default browser, handling errors gracefully."""
    print(f"   Opening {url} ...")
    try:
        webbrowser.open(url)
    except Exception:
        print(f"   (Could not open browser. Please visit {url} manually)")

def check_docker():
    """Check if Docker is installed. If not, prompt user and open download page."""
    if shutil.which("docker") is None:
        typer.secho("⚠️  Docker is missing!", fg=typer.colors.YELLOW, bold=True)
        typer.secho("   Docker is required to run the Dev Containers environment.", fg=typer.colors.YELLOW)
        open_url("https://www.docker.com/get-started")
        
        # Optional: prompt to continue? For now, we just warn.
        # If we blocked, it might be annoying if they plan to install later.
        typer.echo("")

def check_vscode():
    """Check if VS Code is installed. If not, prompt user and open download page."""
    if shutil.which("code") is None:
        typer.secho("⚠️  VS Code is missing!", fg=typer.colors.YELLOW, bold=True)
        typer.secho("   We recommend VS Code for the best experience with this project.", fg=typer.colors.YELLOW)
        open_url("https://code.visualstudio.com/")
        typer.echo("")
