"""Input validation for sparkstart CLI."""

import re
import pathlib
import typer
from typing import List


VALID_LANGUAGES = ["python", "rust", "javascript", "cpp"]
VALID_TEMPLATES = {"python": ["pygame"]}


class ValidationError(Exception):
    """Raised when input validation fails."""

    pass


def validate_project_name(name: str) -> str:
    """
    Validate project name.

    Rules:
    - 1-50 characters
    - Alphanumeric, hyphens, underscores only
    - Cannot start with hyphen or number
    - Cannot be a reserved name
    """
    if not name:
        raise ValidationError("Project name cannot be empty")

    if len(name) > 50:
        raise ValidationError("Project name must be 50 characters or less")

    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_-]*$", name):
        raise ValidationError(
            "Project name must start with letter or underscore, "
            "contain only alphanumerics, hyphens, and underscores"
        )

    # Reserved names
    reserved = {"test", "build", "dist", "env", "venv"}
    if name.lower() in reserved:
        raise ValidationError(f"'{name}' is a reserved project name")

    return name


def validate_language(lang: str) -> str:
    """Validate language choice."""
    if lang not in VALID_LANGUAGES:
        raise ValidationError(
            f"Invalid language '{lang}'. "
            f"Choose from: {', '.join(VALID_LANGUAGES)}"
        )
    return lang


def validate_template(template: str, lang: str) -> str:
    """Validate template choice."""
    if template is None:
        return template

    if lang not in VALID_TEMPLATES:
        raise ValidationError(f"Templates not available for {lang}")

    valid_for_lang = VALID_TEMPLATES[lang]
    if template not in valid_for_lang:
        raise ValidationError(
            f"Invalid template '{template}' for {lang}. "
            f"Choose from: {', '.join(valid_for_lang)}"
        )
    return template


def check_project_exists(name: str, base_path: pathlib.Path = None) -> bool:
    """Check if project directory already exists."""
    if base_path is None:
        base_path = pathlib.Path.cwd()

    project_path = base_path / name
    return project_path.exists()


def print_validation_error(error: ValidationError) -> None:
    """Print validation error in user-friendly format."""
    typer.secho(f"❌ Error: {str(error)}", fg=typer.colors.RED)
