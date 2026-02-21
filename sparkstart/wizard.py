"""Interactive wizard for guided project creation."""

import typer
from typing import Optional
from sparkstart.validation import (
    validate_project_name,
    validate_language,
    validate_template,
    check_project_exists,
    ValidationError,
)


class ProjectConfig:
    """Configuration for a new project from wizard."""

    def __init__(
        self,
        name: str,
        lang: str,
        tutorial: bool,
        devcontainer: bool,
        template: Optional[str],
        github: bool,
        tools: bool = False,
    ):
        self.name = name
        self.lang = lang
        self.tutorial = tutorial
        self.devcontainer = devcontainer
        self.template = template
        self.github = github
        self.tools = tools

    def __repr__(self) -> str:
        return f"ProjectConfig(name={self.name}, lang={self.lang}, tutorial={self.tutorial}, devcontainer={self.devcontainer}, template={self.template}, github={self.github}, tools={self.tools})"


def run_wizard() -> ProjectConfig:
    """Run interactive wizard and return project configuration."""

    typer.secho("\n🧙‍♂️  Welcome to sparkstart!\n", fg=typer.colors.GREEN, bold=True)
    typer.echo("Let's set up your new project. Answer a few quick questions.\n")

    # Project name (with validation)
    while True:
        name = typer.prompt("📝 Project name", default="my-project")
        try:
            validate_project_name(name)
            if check_project_exists(name):
                typer.secho(f"⚠️  Project '{name}' already exists", fg=typer.colors.YELLOW)
                if not typer.confirm("Use different name?", default=True):
                    break
                continue
            break
        except ValidationError as e:
            typer.secho(f"❌ {str(e)}", fg=typer.colors.RED)

    # Language
    typer.secho("\n💻 What language are you using?", fg=typer.colors.CYAN)
    lang_choices = ["python", "rust", "javascript", "cpp"]
    for i, choice in enumerate(lang_choices, 1):
        typer.echo(f"  {i}. {choice}")
    lang_input = typer.prompt("Choose", default="1")

    try:
        lang = lang_choices[int(lang_input) - 1]
    except (ValueError, IndexError):
        lang = "python"
        typer.secho("Invalid choice, using Python", fg=typer.colors.YELLOW)

    # Tutorial flag
    typer.secho("\n🎮 Educational game project with tests?", fg=typer.colors.CYAN)
    typer.echo("  • Includes example game code and test structure")
    typer.echo("  • Great for learning!")
    tutorial = typer.confirm("Include tutorial?", default=False)

    # Template (only for Python)
    template: Optional[str] = None
    if lang == "python" and not tutorial:
        typer.secho("\n🎨 Project template (optional)", fg=typer.colors.CYAN)
        typer.echo("  • pygame: Snake game framework")
        use_template = typer.confirm("Use template?", default=False)
        if use_template:
            typer.echo("  1. pygame")
            template_input = typer.prompt("Choose", default="1")
            if template_input == "1":
                template = "pygame"

    # Dev container
    typer.secho("\n🐳 Development environment", fg=typer.colors.CYAN)
    typer.echo("  • Reproducible dev container (Docker)")
    typer.echo("  • Auto-setup with direnv")
    typer.echo("  • Pre-installed tools & formatters")
    devcontainer = typer.confirm("Include dev container?", default=True)

    # GitHub
    typer.secho("\n🚀 Version control", fg=typer.colors.CYAN)
    typer.echo("  • Create local git repository (always)")
    typer.echo("  • Push to GitHub (optional)")
    github = typer.confirm("Push to GitHub?", default=False)

    # Code quality tools
    typer.secho("\n🛠️  Code quality tools", fg=typer.colors.CYAN)
    typer.echo("  • Formatters: black, prettier, rustfmt, clang-format")
    typer.echo("  • Linters: ruff, eslint, clippy")
    typer.echo("  • Pre-commit hooks for automatic checks")
    tools = typer.confirm("Include code quality tools?", default=True)

    # Summary
    typer.secho("\n📋 Configuration Summary", fg=typer.colors.CYAN, bold=True)
    typer.echo(f"  Project name: {name}")
    typer.echo(f"  Language: {lang}")
    if tutorial:
        typer.echo("  Template: educational game with tests")
    elif template:
        typer.echo(f"  Template: {template}")
    if devcontainer:
        typer.echo("  Dev container: ✓ (Docker + direnv + compose)")
    if tools:
        typer.echo("  Code quality tools: ✓ (formatters, linters, pre-commit)")
    if github:
        typer.echo("  GitHub: ✓ (will push to remote)")

    # Confirm
    typer.echo()
    proceed = typer.confirm("Create project?", default=True)
    if not proceed:
        typer.secho("Cancelled. Happy coding! 👋", fg=typer.colors.YELLOW)
        raise typer.Exit(1)

    typer.echo()
    return ProjectConfig(
        name=name,
        lang=lang,
        tutorial=tutorial,
        devcontainer=devcontainer,
        template=template,
        github=github,
        tools=tools,
    )
