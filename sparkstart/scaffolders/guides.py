import pathlib
from sparkstart.templates.guides import get_getting_started


def scaffold_getting_started(path: pathlib.Path, name: str, lang: str, has_devcontainer: bool) -> None:
    """Create GETTING_STARTED.md with educational content."""
    content = get_getting_started(name, lang, has_devcontainer)
    (path / "GETTING_STARTED.md").write_text(content + "\n")
