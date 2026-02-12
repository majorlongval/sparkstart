"""Tutorial project scaffolders for all supported languages."""

import pathlib
import textwrap


def scaffold_tutorial_python(path: pathlib.Path) -> None:
    """Create a Python tutorial project with number guessing game and tests."""
    # Create directories
    (path / "src").mkdir()
    (path / "tests").mkdir()
    
    # Import templates
    from sparkstart.templates.tutorial.python import (
        PYTHON_MAIN_GAME,
        PYTHON_TESTS_GAME,
        README_PYTHON_TUTORIAL,
        PYPROJECT_TOML_TUTORIAL,
        GITIGNORE_PYTHON_TUTORIAL,
    )
    
    # Write files
    (path / "src" / "main.py").write_text(PYTHON_MAIN_GAME + "\n")
    (path / "tests" / "__init__.py").write_text("")
    (path / "tests" / "test_main.py").write_text(PYTHON_TESTS_GAME + "\n")
    (path / "README.md").write_text(README_PYTHON_TUTORIAL.replace("{name}", path.name) + "\n")
    (path / "pyproject.toml").write_text(PYPROJECT_TOML_TUTORIAL.replace("{name}", path.name) + "\n")
    (path / ".gitignore").write_text(GITIGNORE_PYTHON_TUTORIAL + "\n")


def scaffold_tutorial_rust(path: pathlib.Path) -> None:
    """Create a Rust tutorial project with number guessing game and tests."""
    # Create directories
    (path / "src").mkdir()
    (path / "tests").mkdir()
    
    # Import templates
    from sparkstart.templates.tutorial.rust import (
        RUST_MAIN_GAME,
        RUST_TESTS_GAME,
        README_RUST_TUTORIAL,
        CARGO_TOML_TUTORIAL,
        GITIGNORE_RUST_TUTORIAL,
    )
    
    # Write files
    (path / "src" / "main.rs").write_text(RUST_MAIN_GAME + "\n")
    (path / "tests" / "integration_test.rs").write_text(RUST_TESTS_GAME + "\n")
    (path / "README.md").write_text(README_RUST_TUTORIAL.replace("{name}", path.name) + "\n")
    (path / "Cargo.toml").write_text(CARGO_TOML_TUTORIAL.replace("{name}", path.name) + "\n")
    (path / ".gitignore").write_text(GITIGNORE_RUST_TUTORIAL + "\n")


def scaffold_tutorial_javascript(path: pathlib.Path) -> None:
    """Create a JavaScript tutorial project with number guessing game and tests."""
    # Create directories
    (path / "src").mkdir()
    (path / "tests").mkdir()
    
    # Import templates
    from sparkstart.templates.tutorial.javascript import (
        JAVASCRIPT_MAIN_GAME,
        JAVASCRIPT_TESTS_GAME,
        README_JAVASCRIPT_TUTORIAL,
        PACKAGE_JSON_TUTORIAL,
        GITIGNORE_JAVASCRIPT_TUTORIAL,
    )
    
    # Write files
    (path / "src" / "main.js").write_text(JAVASCRIPT_MAIN_GAME + "\n")
    (path / "tests" / "main.test.js").write_text(JAVASCRIPT_TESTS_GAME + "\n")
    (path / "README.md").write_text(README_JAVASCRIPT_TUTORIAL.replace("{name}", path.name) + "\n")
    (path / "package.json").write_text(PACKAGE_JSON_TUTORIAL.replace("{name}", path.name) + "\n")
    (path / ".gitignore").write_text(GITIGNORE_JAVASCRIPT_TUTORIAL + "\n")


def scaffold_tutorial_cpp(path: pathlib.Path) -> None:
    """Create a C++ tutorial project with number guessing game and tests."""
    # Create directories
    (path / "src").mkdir()
    (path / "tests").mkdir()
    (path / "build").mkdir()
    
    # Import templates
    from sparkstart.templates.tutorial.cpp import (
        CPP_MAIN_GAME,
        CPP_TESTS_GAME,
        README_CPP_TUTORIAL,
        CMAKE_TUTORIAL,
        CONANFILE_TUTORIAL,
        GITIGNORE_CPP_TUTORIAL,
    )
    
    # Write files
    (path / "src" / "main.cpp").write_text(CPP_MAIN_GAME + "\n")
    (path / "tests" / "test_main.cpp").write_text(CPP_TESTS_GAME + "\n")
    (path / "README.md").write_text(README_CPP_TUTORIAL.replace("{name}", path.name) + "\n")
    (path / "CMakeLists.txt").write_text(CMAKE_TUTORIAL.replace("{name}", path.name) + "\n")
    (path / "conanfile.txt").write_text(CONANFILE_TUTORIAL + "\n")
    (path / ".gitignore").write_text(GITIGNORE_CPP_TUTORIAL + "\n")
