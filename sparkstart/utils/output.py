"""Pretty output and summaries for project creation."""

import typer
from pathlib import Path


def print_project_summary(path: Path, lang: str, devcontainer: bool, github: bool, tutorial: bool) -> None:
    """Print a beautiful summary of what was created."""

    project_name = path.name

    typer.secho(f"\n✨ Project '{project_name}' created successfully!\n", fg=typer.colors.GREEN, bold=True)

    # What's included section
    typer.secho("📦 What's Included:", fg=typer.colors.CYAN, bold=True)

    items = [
        f"  ✓ {lang.capitalize()} project structure",
        f"  ✓ Test files and examples",
        f"  ✓ .gitignore and README.md",
    ]

    if tutorial:
        items.append("  ✓ Educational game project with tests")

    if devcontainer:
        items.extend([
            "  ✓ .devcontainer/ - Docker dev environment",
            "  ✓ .envrc - Environment auto-setup (direnv)",
            "  ✓ compose.yaml - Docker Compose orchestration",
            "  ✓ Pre-installed formatters and linters",
        ])

    if github:
        items.append("  ✓ Git repository (pushed to GitHub)")
    else:
        items.append("  ✓ Git repository (local)")

    for item in items:
        typer.echo(item)

    # Quick start section
    typer.secho("\n🚀 Quick Start:", fg=typer.colors.CYAN, bold=True)
    typer.echo(f"  cd {project_name}")

    if devcontainer:
        typer.echo("  direnv allow              # Auto-activates environment")
        typer.echo("  docker compose up -d      # Start dev containers")
    else:
        if lang == "python":
            typer.echo("  python3 -m venv .venv")
            typer.echo("  source .venv/bin/activate")
            typer.echo("  pip install -r requirements.txt")
        elif lang == "javascript":
            typer.echo("  npm install")
        elif lang == "rust":
            typer.echo("  cargo build")
        elif lang == "cpp":
            typer.echo("  mkdir build && cd build && cmake .. && make")

    # Documentation section
    typer.secho("\n📚 Learn More:", fg=typer.colors.CYAN, bold=True)
    typer.echo("  cat GETTING_STARTED.md     # Complete setup guide")
    typer.echo("  cat README.md              # Project overview")

    if devcontainer:
        typer.echo("  cat .devcontainer/README.md  # Dev environment details")

    # Support section
    typer.secho("\n💡 Tips:", fg=typer.colors.CYAN, bold=True)

    if not devcontainer:
        typer.echo("  • Use --devcontainer flag for reproducible dev environments")

    if not tutorial:
        typer.echo("  • Use --tutorial flag for educational game projects")

    typer.echo("  • Check GETTING_STARTED.md for language-specific commands")

    typer.secho("\nHappy coding! 🎉\n", fg=typer.colors.GREEN)
