"""Scaffolder for code quality tools and pre-commit hooks."""

import pathlib
import json
import textwrap
from sparkstart.templates.tools import (
    PRECOMMIT_PYTHON,
    PRECOMMIT_RUST,
    PRECOMMIT_JAVASCRIPT,
    PRECOMMIT_CPP,
    REQUIREMENTS_PYTHON_TOOLS,
    NPM_SCRIPTS_JAVASCRIPT,
    EDITORCONFIG,
)


def scaffold_tools(path: pathlib.Path, lang: str) -> None:
    """Create code quality tools configuration and pre-commit hooks."""
    # Always create EditorConfig
    _scaffold_editorconfig(path)

    # Language-specific tools
    if lang == "python":
        _scaffold_python_tools(path)
    elif lang == "rust":
        _scaffold_rust_tools(path)
    elif lang == "javascript":
        _scaffold_javascript_tools(path)
    elif lang == "cpp":
        _scaffold_cpp_tools(path)

    # Create .pre-commit-config.yaml for all languages
    _scaffold_precommit_config(path, lang)


def _scaffold_editorconfig(path: pathlib.Path) -> None:
    """Create .editorconfig file."""
    (path / ".editorconfig").write_text(EDITORCONFIG + "\n")


def _scaffold_precommit_config(path: pathlib.Path, lang: str) -> None:
    """Create .pre-commit-config.yaml based on language."""
    configs = {
        "python": PRECOMMIT_PYTHON,
        "rust": PRECOMMIT_RUST,
        "javascript": PRECOMMIT_JAVASCRIPT,
        "cpp": PRECOMMIT_CPP,
    }

    if lang in configs:
        content = configs[lang]
        (path / ".pre-commit-config.yaml").write_text(content + "\n")


def _scaffold_python_tools(path: pathlib.Path) -> None:
    """Create Python-specific tool configurations."""
    # Create requirements file for development tools
    requirements_file = path / "requirements-dev.txt"
    if requirements_file.exists():
        # Append to existing requirements
        existing = requirements_file.read_text()
        requirements_file.write_text(existing.rstrip() + "\n\n# Development Tools\n" + REQUIREMENTS_PYTHON_TOOLS + "\n")
    else:
        requirements_file.write_text(REQUIREMENTS_PYTHON_TOOLS + "\n")

    # Create pyproject.toml configuration if needed (black, ruff, mypy configs)
    pyproject_file = path / "pyproject.toml"
    if pyproject_file.exists():
        content = pyproject_file.read_text()
        # Add tool configurations if not already present
        if "[tool.black]" not in content:
            content += "\n\n[tool.black]\nline-length = 100\ntarget-version = ['py312']\n"
        if "[tool.ruff]" not in content:
            content += "\n[tool.ruff]\nline-length = 100\ntarget-version = \"py312\"\n"
        if "[tool.mypy]" not in content:
            content += "\n[tool.mypy]\npython_version = \"3.12\"\nwarn_return_any = true\nwarn_unused_configs = true\n"
        pyproject_file.write_text(content)


def _scaffold_rust_tools(path: pathlib.Path) -> None:
    """Create Rust-specific tool configurations."""
    # rustfmt.toml
    rustfmt_config = textwrap.dedent("""
        # Rust formatting configuration
        max_width = 100
        tab_spaces = 4
        edition = "2021"
    """).strip()
    (path / "rustfmt.toml").write_text(rustfmt_config + "\n")

    # clippy.toml
    clippy_config = textwrap.dedent("""
        # Clippy linting configuration
        too-many-arguments-threshold = 8
    """).strip()
    (path / "clippy.toml").write_text(clippy_config + "\n")


def _scaffold_javascript_tools(path: pathlib.Path) -> None:
    """Create JavaScript-specific tool configurations."""
    # .prettierrc
    prettier_config = {
        "semi": True,
        "trailingComma": "es5",
        "tabWidth": 2,
        "useTabs": False,
        "singleQuote": True,
        "printWidth": 100,
    }
    (path / ".prettierrc").write_text(json.dumps(prettier_config, indent=2) + "\n")

    # .prettierignore
    prettier_ignore = textwrap.dedent("""
        node_modules
        dist
        build
        .next
        out
        coverage
    """).strip()
    (path / ".prettierignore").write_text(prettier_ignore + "\n")

    # .eslintignore
    eslint_ignore = textwrap.dedent("""
        node_modules
        dist
        build
        .next
        out
        coverage
    """).strip()
    (path / ".eslintignore").write_text(eslint_ignore + "\n")

    # Update package.json with lint scripts if it exists
    package_json_path = path / "package.json"
    if package_json_path.exists():
        try:
            package_json = json.loads(package_json_path.read_text())
            if "scripts" not in package_json:
                package_json["scripts"] = {}
            # Add linting scripts
            package_json["scripts"].update(NPM_SCRIPTS_JAVASCRIPT)
            package_json_path.write_text(json.dumps(package_json, indent=2) + "\n")
        except json.JSONDecodeError:
            pass  # Silently skip if package.json is malformed


def _scaffold_cpp_tools(path: pathlib.Path) -> None:
    """Create C++-specific tool configurations."""
    # .clang-format
    clang_format_config = textwrap.dedent("""
        BasedOnStyle: LLVM
        IndentWidth: 4
        ColumnLimit: 100
        UseTab: Never
        TabWidth: 4
        BreakBeforeBraces: Attach
        AllowShortFunctionsOnASingleLine: Empty
        AllowShortIfStatementsOnASingleLine: Never
    """).strip()
    (path / ".clang-format").write_text(clang_format_config + "\n")
