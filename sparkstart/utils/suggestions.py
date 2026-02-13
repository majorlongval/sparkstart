"""Helpful suggestions and error messages with typo detection."""

import difflib
from typing import Optional, List


class SuggestionEngine:
    """Suggest corrections for invalid inputs."""

    @staticmethod
    def suggest_language(invalid: str, available: List[str]) -> Optional[str]:
        """Suggest closest matching language."""
        matches = difflib.get_close_matches(invalid, available, n=1, cutoff=0.6)
        return matches[0] if matches else None

    @staticmethod
    def suggest_template(invalid: str, available: List[str]) -> Optional[str]:
        """Suggest closest matching template."""
        matches = difflib.get_close_matches(invalid, available, n=1, cutoff=0.6)
        return matches[0] if matches else None

    @staticmethod
    def suggest_command(invalid: str, available: List[str]) -> Optional[str]:
        """Suggest closest matching command."""
        matches = difflib.get_close_matches(invalid, available, n=1, cutoff=0.6)
        return matches[0] if matches else None


def format_error_message(
    error: str,
    suggestion: Optional[str] = None,
    available_options: Optional[List[str]] = None,
) -> str:
    """Format error message with suggestions."""
    message = f"❌ Error: {error}"

    if suggestion:
        message += f"\n💡 Did you mean: {suggestion}?"

    if available_options:
        message += f"\n   Available options: {', '.join(available_options)}"

    return message


def suggest_invalid_language(lang: str) -> str:
    """Suggest correction for invalid language."""
    available = ["python", "rust", "javascript", "cpp"]
    suggestion = SuggestionEngine.suggest_language(lang, available)
    return format_error_message(
        f"Language '{lang}' not supported",
        suggestion,
        available,
    )


def suggest_invalid_template(template: str, lang: str = "python") -> str:
    """Suggest correction for invalid template."""
    available = ["pygame"] if lang == "python" else []
    if not available:
        return format_error_message(f"Templates not available for {lang}")

    suggestion = SuggestionEngine.suggest_template(template, available)
    return format_error_message(
        f"Template '{template}' not found for {lang}",
        suggestion,
        available,
    )


def suggest_invalid_project_name(name: str, reason: str) -> str:
    """Suggest fixes for invalid project name."""
    hints = []

    if any(c in name for c in " \t"):
        hints.append("• Remove spaces (use hyphens or underscores instead)")

    if any(c in name for c in "!@#$%^&*()+=[]{}|;:,.<>?"):
        hints.append("• Remove special characters")

    if name[0].isdigit():
        hints.append("• Project name cannot start with a number")

    if name.lower() in ["test", "demo", "example"]:
        hints.append(f"• '{name}' is a reserved word, try adding a prefix or suffix")

    message = f"❌ Error: Invalid project name '{name}'\n   Reason: {reason}"

    if hints:
        message += "\n   Suggestions:\n   " + "\n   ".join(hints)

    return message


def suggest_project_exists(name: str) -> str:
    """Message when project already exists."""
    return (
        f"❌ Project '{name}' already exists\n"
        f"   Use a different name or remove the existing directory"
    )


def suggest_docker_not_found() -> str:
    """Message when Docker is not installed."""
    return (
        "❌ Docker not found\n"
        "   To use dev containers, install Docker:\n"
        "   • macOS/Windows: https://www.docker.com/products/docker-desktop\n"
        "   • Linux: sudo apt install docker.io (Ubuntu/Debian)"
    )


def suggest_git_not_found() -> str:
    """Message when git is not installed."""
    return (
        "❌ Git not found\n"
        "   To use sparkstart, install Git:\n"
        "   • macOS: brew install git\n"
        "   • Linux: sudo apt install git (Ubuntu/Debian)\n"
        "   • Windows: https://git-scm.com/"
    )
