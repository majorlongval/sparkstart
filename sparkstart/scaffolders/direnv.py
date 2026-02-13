import pathlib
from sparkstart.templates.direnv import ENVRC_PYTHON, ENVRC_RUST, ENVRC_JAVASCRIPT, ENVRC_CPP


def scaffold_direnv(path: pathlib.Path, lang: str) -> None:
    """Create .envrc configuration for direnv."""
    templates = {
        "python": ENVRC_PYTHON,
        "rust": ENVRC_RUST,
        "javascript": ENVRC_JAVASCRIPT,
        "cpp": ENVRC_CPP,
    }

    if lang not in templates:
        raise ValueError(f"Unsupported language for direnv: {lang}")

    content = templates[lang]
    (path / ".envrc").write_text(content + "\n")
