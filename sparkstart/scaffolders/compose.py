import pathlib
from sparkstart.templates.compose import COMPOSE_PYTHON, COMPOSE_RUST, COMPOSE_JAVASCRIPT, COMPOSE_CPP


def scaffold_compose(path: pathlib.Path, lang: str) -> None:
    """Create docker-compose.yaml configuration."""
    templates = {
        "python": COMPOSE_PYTHON,
        "rust": COMPOSE_RUST,
        "javascript": COMPOSE_JAVASCRIPT,
        "cpp": COMPOSE_CPP,
    }

    if lang not in templates:
        raise ValueError(f"Unsupported language for compose: {lang}")

    content = templates[lang]
    (path / "compose.yaml").write_text(content + "\n")
