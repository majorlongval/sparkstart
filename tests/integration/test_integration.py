"""
Integration tests for sparkstart.

These tests run the CLI end-to-end in a real temporary directory and verify
that the generated project is actually usable (installs, runs, passes its own tests).

TODO: implement the following test cases

Each test should:
  1. Call `sparkstart new <name> [options]` via subprocess in a tmp_path
  2. Assert the expected files/dirs exist
  3. Run the generated project's setup commands (venv, install, etc.)
  4. Run the generated project's tests and assert they pass
  5. Clean up (tmp_path fixture handles this automatically)

-------------------------------------------------------------------------------
Test cases to cover:
-------------------------------------------------------------------------------

TODO: test_python_default
  - sparkstart new test-proj --lang python
  - Expected files: src/main.py, tests/test_main.py, pyproject.toml, .gitignore, README.md
  - Setup: python -m venv .venv && .venv/bin/pip install -e '.[test]'
  - Verify: .venv/bin/pytest tests/ exits 0

TODO: test_python_pygame_template
  - sparkstart new test-pygame --lang python --template pygame
  - Expected files: src/main.py (imports pygame), pyproject.toml (pygame in deps)
  - Setup: python -m venv .venv && .venv/bin/pip install -e '.[test]'
  - Verify: pygame importable, .venv/bin/pytest tests/ exits 0

TODO: test_python_tutorial
  - sparkstart new test-tutorial --lang python --tutorial
  - Expected files: tutorial structure, tests with game logic
  - Verify: .venv/bin/pytest tests/ exits 0

TODO: test_rust_default
  - sparkstart new test-rust --lang rust
  - Expected files: src/main.rs, Cargo.toml, tests/
  - Verify: cargo test exits 0

TODO: test_javascript_default
  - sparkstart new test-js --lang javascript
  - Expected files: src/main.js, package.json, tests/
  - Verify: npm install && npm test exits 0

TODO: test_cpp_default
  - sparkstart new test-cpp --lang cpp
  - Expected files: src/main.cpp, CMakeLists.txt
  - Verify: mkdir build && cmake .. && make exits 0

TODO: test_devcontainer_files
  - sparkstart new test-dc --lang python --devcontainer
  - Verify presence of: .devcontainer/, .envrc, compose.yaml

TODO: test_tools_files
  - sparkstart new test-tools --lang python --tools
  - Verify presence of: .pre-commit-config.yaml, .editorconfig

TODO: test_git_initialized
  - Any sparkstart new ... call
  - Verify: .git/ directory exists and `git log` shows an initial commit

TODO: test_no_requirements_txt
  - sparkstart new test-proj --lang python
  - Verify: requirements.txt does NOT exist (deps are in pyproject.toml)
"""

# Skeleton — uncomment and implement when ready
#
# import subprocess
# import sys
# from pathlib import Path
# import pytest
#
#
# def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
#     return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
#
#
# def test_python_default(tmp_path):
#     result = run(["sparkstart", "new", "test-proj", "--lang", "python"], cwd=tmp_path)
#     assert result.returncode == 0
#
#     proj = tmp_path / "test-proj"
#     assert (proj / "src" / "main.py").exists()
#     assert (proj / "tests" / "test_main.py").exists()
#     assert (proj / "pyproject.toml").exists()
#     assert not (proj / "requirements.txt").exists()
#
#     run([sys.executable, "-m", "venv", ".venv"], cwd=proj)
#     run([".venv/bin/pip", "install", "-e", ".[test]"], cwd=proj)
#     result = run([".venv/bin/pytest", "tests/"], cwd=proj)
#     assert result.returncode == 0
