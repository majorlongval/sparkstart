import pathlib
from sparkstart.templates.devcontainer import (
    DEVCONTAINER_JSON,
    DEVCONTAINER_PYTHON,
    DEVCONTAINER_RUST,
    DEVCONTAINER_JAVASCRIPT,
)

def scaffold_devcontainer(path: pathlib.Path, lang: str) -> None:
    """Create .devcontainer configuration."""
    (path / ".devcontainer").mkdir()

    templates = {
        "cpp": DEVCONTAINER_JSON,
        "python": DEVCONTAINER_PYTHON,
        "rust": DEVCONTAINER_RUST,
        "javascript": DEVCONTAINER_JAVASCRIPT,
    }

    if lang not in templates:
        raise ValueError(f"Unsupported language for devcontainer: {lang}")

    content = templates[lang]
    (path / ".devcontainer" / "devcontainer.json").write_text(content + "\n")
