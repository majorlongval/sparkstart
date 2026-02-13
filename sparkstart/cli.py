import pathlib
import typer
import shutil
from typing import Optional
from sparkstart.core import create_project, delete_project
from sparkstart.checks import check_docker, check_vscode
from sparkstart.wizard import run_wizard
from sparkstart.validation import (
    validate_project_name,
    validate_language,
    validate_template,
    check_project_exists,
    ValidationError,
)


app = typer.Typer(
    help="sparkstart – create a new project repository quickly",
    invoke_without_command=True,  # allows root alias
)


# --- root alias ----------------------------------------------------
@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    # name argument removed to avoid "stealing" the subcommand
):
    """
    sparkstart – Start your new project in seconds.

    Usage:
        sparkstart new <name>
        sparkstart delete <name>
    """
    if ctx.invoked_subcommand is None:
        # Show helpful welcome message
        _print_welcome()
        raise typer.Exit()


def _print_welcome() -> None:
    """Print a welcoming, informative welcome message."""
    typer.secho("\n🚀 sparkstart – Create a project in seconds\n", fg=typer.colors.GREEN, bold=True)

    typer.secho("Usage:", fg=typer.colors.CYAN, bold=True)
    typer.echo("  sparkstart new [NAME]          Create a new project (interactive wizard)")
    typer.echo("  sparkstart new NAME --lang rust --devcontainer  # Skip wizard with flags")
    typer.echo("  sparkstart delete NAME         Remove a project")

    typer.secho("\nExamples:", fg=typer.colors.CYAN, bold=True)
    typer.echo("  sparkstart new                 # Start with interactive wizard (recommended)")
    typer.echo("  sparkstart new my-app          # Create Python project with defaults")
    typer.echo("  sparkstart new my-game --lang python --template pygame --tutorial")

    typer.secho("\nOptions:", fg=typer.colors.CYAN, bold=True)
    typer.echo("  --lang LANGUAGE               python, rust, javascript, cpp (default: python)")
    typer.echo("  --devcontainer               Include Docker dev environment")
    typer.echo("  --tutorial                   Create educational game project with tests")
    typer.echo("  --template TEMPLATE          pygame (python only)")
    typer.echo("  --github                     Push to GitHub")

    typer.secho("\nQuick Start:", fg=typer.colors.CYAN, bold=True)
    typer.echo("  1. sparkstart new             # Interactive setup (recommended for first time)")
    typer.echo("  2. cd my-project")
    typer.echo("  3. cat GETTING_STARTED.md     # See what's included")

    typer.secho("\nLearn More:", fg=typer.colors.CYAN, bold=True)
    typer.echo("  Documentation: https://github.com/majorlongval/sparkstart")
    typer.echo("  Issues: https://github.com/majorlongval/sparkstart/issues")

    typer.secho("\nHappy coding! ✨\n", fg=typer.colors.GREEN)


# --- explicit sub‑command -----------------------------------------
@app.command()
def new(
    name: Optional[str] = typer.Argument(None, help="Project name (interactive wizard if omitted)"),
    github: bool = typer.Option(False, "--github", help="Push to GitHub"),
    lang: str = typer.Option(None, "--lang", "-l", help="Language: python, rust, javascript, cpp"),
    template: str = typer.Option(None, "--template", help="Template: pygame (only for python)"),
    tutorial: bool = typer.Option(False, "--tutorial", "-t", help="Create educational game project with tests"),
    devcontainer: bool = typer.Option(None, "--devcontainer", "-d", help="Generate .devcontainer config (Docker required)"),
    tools: bool = typer.Option(False, "--tools", help="Include formatters, linters, and pre-commit hooks"),
):
    """Create a new project (interactive wizard or direct mode with flags)."""

    # Launch wizard if name is not provided
    if name is None:
        config = run_wizard()
        name = config.name
        lang = config.lang
        tutorial = config.tutorial
        devcontainer = config.devcontainer
        template = config.template
        github = config.github
        tools = config.tools
    else:
        # Direct mode with flags - validate inputs
        try:
            validate_project_name(name)
            if check_project_exists(name):
                typer.secho(f"❌ Project '{name}' already exists", fg=typer.colors.RED)
                raise typer.Exit(1)

            if lang is None:
                lang = "python"
            else:
                validate_language(lang)

            if template is not None:
                validate_template(template, lang)

            if devcontainer is None:
                devcontainer = False

        except ValidationError as e:
            typer.secho(f"❌ Error: {str(e)}", fg=typer.colors.RED)
            raise typer.Exit(1)

    if devcontainer:
        check_docker()
        check_vscode()

    create_project(pathlib.Path.cwd() / name, github, lang, devcontainer, template, tutorial, tools)



@app.command()
def delete(
    name: str,
    github: bool = typer.Option(False, "--github"),
    force: bool = typer.Option(False, "--yes", "-y"),
):
    target = pathlib.Path.cwd() / name
    if not force:
        typer.confirm(f"Delete {'and remote ' if github else ''}{target} ?", abort=True)

    try:
        from sparkstart.core import delete_project

        delete_project(target, github)
        typer.secho("Project deleted !", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(f"Failed : {e}", fg=typer.colors.RED)
