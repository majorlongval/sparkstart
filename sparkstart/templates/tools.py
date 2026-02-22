"""Templates for code quality tools (formatters, linters, pre-commit hooks)."""

import textwrap

# Pre-commit configuration for different languages
PRECOMMIT_PYTHON = textwrap.dedent("""
    # .pre-commit-config.yaml
    #
    # Runs code-quality checks automatically before every `git commit`.
    # Catches formatting issues and lint errors early, before they ever hit your history.
    #
    # First-time setup (once per machine):
    #   pip install pre-commit
    #   pre-commit install        # registers these hooks with this git repo
    #
    # Run manually on all files:
    #   pre-commit run --all-files
    #
    # Skip in an emergency (use sparingly):
    #   git commit --no-verify
    #
    # Learn more: https://pre-commit.com

    repos:
      - repo: https://github.com/psf/black
        rev: 23.12.1
        hooks:
          - id: black
            language_version: python3.12

      - repo: https://github.com/charliermarsh/ruff-pre-commit
        rev: v0.1.11
        hooks:
          - id: ruff
            args: [--fix]

      - repo: https://github.com/pre-commit/pre-commit-hooks
        rev: v4.5.0
        hooks:
          - id: trailing-whitespace
          - id: end-of-file-fixer
          - id: check-yaml
          - id: check-added-large-files
""").strip()

PRECOMMIT_RUST = textwrap.dedent("""
    # .pre-commit-config.yaml
    #
    # Runs code-quality checks automatically before every `git commit`.
    # Catches formatting and clippy warnings early, before they hit your history.
    #
    # First-time setup (once per machine):
    #   pip install pre-commit
    #   pre-commit install        # registers these hooks with this git repo
    #
    # Run manually on all files:
    #   pre-commit run --all-files
    #
    # Learn more: https://pre-commit.com

    repos:
      - repo: local
        hooks:
          - id: rustfmt
            name: rustfmt
            entry: rustfmt
            language: system
            types: [rust]
            pass_filenames: true

          - id: clippy
            name: clippy
            entry: cargo clippy -- -D warnings
            language: system
            types: [rust]
            pass_filenames: false

      - repo: https://github.com/pre-commit/pre-commit-hooks
        rev: v4.5.0
        hooks:
          - id: trailing-whitespace
          - id: end-of-file-fixer
          - id: check-yaml
""").strip()

PRECOMMIT_JAVASCRIPT = textwrap.dedent("""
    # .pre-commit-config.yaml
    #
    # Runs code-quality checks automatically before every `git commit`.
    # Catches formatting and lint issues early, before they hit your history.
    #
    # First-time setup (once per machine):
    #   pip install pre-commit
    #   pre-commit install        # registers these hooks with this git repo
    #
    # Run manually on all files:
    #   pre-commit run --all-files
    #
    # Note: requires Node.js for prettier and eslint hooks.
    # Learn more: https://pre-commit.com

    repos:
      - repo: local
        hooks:
          - id: prettier
            name: prettier
            entry: npx prettier --write
            language: system
            types: [javascript, jsx, typescript, tsx, json, yaml, markdown]

          - id: eslint
            name: eslint
            entry: npx eslint --fix
            language: system
            types: [javascript, jsx, typescript, tsx]

      - repo: https://github.com/pre-commit/pre-commit-hooks
        rev: v4.5.0
        hooks:
          - id: trailing-whitespace
          - id: end-of-file-fixer
          - id: check-yaml
          - id: check-json
""").strip()

PRECOMMIT_CPP = textwrap.dedent("""
    # .pre-commit-config.yaml
    #
    # Runs code-quality checks automatically before every `git commit`.
    # Catches formatting issues early, before they hit your history.
    #
    # First-time setup (once per machine):
    #   pip install pre-commit
    #   pre-commit install        # registers these hooks with this git repo
    #
    # Run manually on all files:
    #   pre-commit run --all-files
    #
    # Note: requires clang-format to be installed on your system.
    # Learn more: https://pre-commit.com

    repos:
      - repo: local
        hooks:
          - id: clang-format
            name: clang-format
            entry: clang-format -i
            language: system
            types: [c++, c]
            pass_filenames: true

      - repo: https://github.com/pre-commit/pre-commit-hooks
        rev: v4.5.0
        hooks:
          - id: trailing-whitespace
          - id: end-of-file-fixer
          - id: check-yaml
          - id: check-added-large-files
""").strip()

# Requirements files for Python tools
REQUIREMENTS_PYTHON_TOOLS = textwrap.dedent("""
    # requirements-dev.txt — development-only tools
    #
    # These are NOT needed to run your project — they help you write better code.
    # Install with:  pip install -r requirements-dev.txt
    #
    #   Formatters:    auto-fix code style so you never have to think about it
    #   Linters:       catch bugs and bad patterns before they become real problems
    #   Type checker:  find type errors before they become runtime surprises
    #   Coverage:      shows which lines your tests actually exercise

    # Code Quality Tools
    black==23.12.1          # Formatter: rewrites your code to a consistent style
    ruff==0.1.11           # Linter: fast, catches common bugs and style issues
    pylint==3.0.3          # Linter: more comprehensive, slower, but very thorough
    mypy==1.7.1            # Type checker: catches type errors statically
    pytest-cov==4.1.0      # Coverage: adds --cov flag to pytest
""").strip()

# npm scripts configuration (to be added to package.json)
NPM_SCRIPTS_JAVASCRIPT = {
    "lint": "eslint src/ --ext .js,.jsx,.ts,.tsx",
    "lint:fix": "eslint src/ --ext .js,.jsx,.ts,.tsx --fix",
    "format": "prettier --write src/",
    "format:check": "prettier --check src/",
    "type-check": "tsc --noEmit"
}

# EditorConfig for consistent formatting
EDITORCONFIG = textwrap.dedent("""
    # .editorconfig
    #
    # Tells editors (VS Code, PyCharm, Vim, Neovim, Emacs, ...) how to format code:
    # indentation, line endings, charset, and more. When everyone on a team uses it,
    # you stop seeing noisy diffs caused by tab/space or line-ending differences.
    #
    # Most editors support it out of the box or via a free plugin.
    # Learn more: https://editorconfig.org

    root = true

    [*]
    charset = utf-8
    end_of_line = lf
    insert_final_newline = true
    trim_trailing_whitespace = true

    [*.py]
    indent_style = space
    indent_size = 4
    max_line_length = 100

    [*.{js,jsx,ts,tsx,json}]
    indent_style = space
    indent_size = 2

    [*.{yml,yaml}]
    indent_style = space
    indent_size = 2

    [Makefile]
    indent_style = tab

    [*.md]
    trim_trailing_whitespace = false
    max_line_length = 120
""").strip()
