"""Enhanced help system and tutorials."""

import typer


def show_help_tutorial() -> None:
    """Show comprehensive help and tutorial."""
    typer.secho("\n" + "=" * 60, fg=typer.colors.CYAN)
    typer.secho("🧙 SPARKSTART – Quick Project Setup", fg=typer.colors.CYAN, bold=True)
    typer.secho("=" * 60 + "\n", fg=typer.colors.CYAN)

    # Getting Started
    typer.secho("🚀 GETTING STARTED", fg=typer.colors.GREEN, bold=True)
    typer.secho("─" * 60, fg=typer.colors.GREEN)
    typer.echo(
        """
The easiest way to get started is with the interactive wizard:

  $ sparkstart new

This will ask you:
  1. Project name
  2. Programming language (python, rust, javascript, cpp)
  3. Whether to create an educational project
  4. Template choice (if applicable)
  5. Dev container setup (Docker)
  6. Code quality tools (formatters, linters)
  7. GitHub push (optional)

Or use direct mode with flags:

  $ sparkstart new my-project --lang python --devcontainer --tools
"""
    )

    # Commands
    typer.secho("\n📋 COMMANDS", fg=typer.colors.CYAN, bold=True)
    typer.secho("─" * 60, fg=typer.colors.CYAN)
    typer.echo(
        """
  sparkstart new [NAME]     Create a new project
  sparkstart help           Show this help
  sparkstart version        Show version
"""
    )

    # Options
    typer.secho("\n⚙️  OPTIONS FOR 'sparkstart new'", fg=typer.colors.YELLOW, bold=True)
    typer.secho("─" * 60, fg=typer.colors.YELLOW)
    typer.echo(
        """
  --lang, -l LANG           Language: python, rust, javascript, cpp
  --template TEMPLATE       Template: pygame (python only)
  --tutorial, -t            Create educational project with tests
  --devcontainer, -d        Setup Docker dev container with direnv
  --tools                   Add formatters, linters, pre-commit hooks
  --github                  Create and push to GitHub
  --help, -h                Show help
"""
    )

    # Features
    typer.secho("\n✨ WHAT YOU GET", fg=typer.colors.MAGENTA, bold=True)
    typer.secho("─" * 60, fg=typer.colors.MAGENTA)
    typer.echo(
        """
Every project includes:
  ✓ Language-specific structure and examples
  ✓ .gitignore and comprehensive README
  ✓ Test setup and sample tests
  ✓ GETTING_STARTED.md guide

With --devcontainer:
  ✓ .devcontainer/ for reproducible development
  ✓ .envrc for automatic environment setup
  ✓ docker-compose.yaml for orchestration
  ✓ Pre-installed tools and dependencies

With --tools:
  ✓ Code formatters (black, prettier, rustfmt, clang-format)
  ✓ Linters (ruff, eslint, clippy)
  ✓ Pre-commit hooks to check code before commits
  ✓ .editorconfig for editor consistency

With --tutorial:
  ✓ Educational game project with tests
  ✓ Learning resources and exercises

With --github:
  ✓ Local Git repository
  ✓ Remote GitHub repository (created and pushed)
"""
    )

    # Examples
    typer.secho("\n💡 EXAMPLES", fg=typer.colors.BLUE, bold=True)
    typer.secho("─" * 60, fg=typer.colors.BLUE)
    typer.echo(
        """
# Interactive wizard
$ sparkstart new

# Python project with all features
$ sparkstart new my-app --lang python --devcontainer --tools --github

# Rust project for learning
$ sparkstart new learning-rust --lang rust --tutorial

# Quick JavaScript project
$ sparkstart new web-app --lang javascript --tools

# C++ with Docker dev environment
$ sparkstart new cpp-project --lang cpp --devcontainer
"""
    )

    # Tips
    typer.secho("\n💭 PRO TIPS", fg=typer.colors.YELLOW, bold=True)
    typer.secho("─" * 60, fg=typer.colors.YELLOW)
    typer.echo(
        """
• Use --devcontainer for consistent development across machines
• Use --tools to enforce code quality from the start
• Use --tutorial to learn a new language with guided exercises
• GitHub token is saved to .sparkstart.env (never committed)
• Each project includes GETTING_STARTED.md with language-specific setup
• Run 'sparkstart new' without arguments for interactive wizard
"""
    )

    # Troubleshooting
    typer.secho("\n🔧 TROUBLESHOOTING", fg=typer.colors.RED, bold=True)
    typer.secho("─" * 60, fg=typer.colors.RED)
    typer.echo(
        """
Missing Docker?
  Install: https://www.docker.com/get-started

Missing Git?
  macOS: brew install git
  Linux: sudo apt install git
  Windows: https://git-scm.com/

Missing language runtime?
  Python: https://www.python.org/
  Rust: https://rustup.rs/
  Node.js: https://nodejs.org/
  C++: Install gcc/clang (or use --devcontainer)

Project already exists?
  Use a different name or remove the existing directory
"""
    )

    typer.secho("\n" + "=" * 60, fg=typer.colors.CYAN)
    typer.secho("Happy coding! 🎉\n", fg=typer.colors.GREEN, bold=True)


def show_quick_help() -> None:
    """Show quick help (for --help flag)."""
    typer.secho("\nsparkstart – Create a new project repository quickly\n", bold=True)

    typer.secho("USAGE:", bold=True)
    typer.echo("  sparkstart new [NAME] [OPTIONS]")
    typer.echo("  sparkstart help")
    typer.echo("  sparkstart version")

    typer.secho("\nOPTIONS:", bold=True)
    typer.echo("  --lang, -l LANG              Language (python, rust, javascript, cpp)")
    typer.echo("  --template TEMPLATE          Template (pygame for Python)")
    typer.echo("  --tutorial, -t               Educational project with tests")
    typer.echo("  --devcontainer, -d           Docker dev container setup")
    typer.echo("  --tools                      Formatters, linters, pre-commit hooks")
    typer.echo("  --github                     Create GitHub repository")
    typer.echo("  --help, -h                   Show this message")
    typer.echo("  --version, -v                Show version")

    typer.secho("\nEXAMPLES:", bold=True)
    typer.echo("  sparkstart new my-project")
    typer.echo("  sparkstart new my-app --lang python --devcontainer --tools")
    typer.echo("  sparkstart new my-rust --lang rust --tutorial")

    typer.secho("\nFor more help, run: sparkstart help\n")
