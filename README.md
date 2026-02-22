# sparkstart ⚡

**Create a new project in seconds, not hours.**

`sparkstart` handles all the boring setup so you can start coding immediately. No more copy-pasting boilerplate, no more manual configuration—just run one command and you're ready to go.

[![Tests](https://github.com/majorlongval/sparkstart/actions/workflows/tests.yml/badge.svg)](https://github.com/majorlongval/sparkstart/actions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ What It Does

1. **🚀 Instant Setup** — Creates project structure, git repo, and starter code in seconds
2. **🐳 Dev Containers** — Optional Docker environments with pre-configured tools
3. **🎓 Educational Projects** — Learn new languages with guided game tutorials
4. **🛠️ Code Quality Tools** — Pre-commit hooks, linters, and formatters built-in
5. **☁️ GitHub Integration** — Auto-create and push repositories
6. **📚 Smart Help System** — Built-in guides and tutorials for every project

## 🚀 Quick Start

```bash
# Install (recommended)
pipx install sparkstart

# Or with pip (Windows / python.org macOS only)
pip install sparkstart

# Create a project (interactive wizard)
sparkstart new

# Or use direct mode with flags
sparkstart new my-awesome-game --lang python --devcontainer --tools
```

That's it! Your project is ready to code.

## 📋 Supported Languages

| Language | Features |
|----------|----------|
| **Python** | Poetry/pip, venv, pytest, best practices |
| **Rust** | Cargo, clippy, rustfmt, testing setup |
| **JavaScript** | npm/Node.js, ESLint, Prettier, testing framework |
| **C++** | CMake, Conan, build system, googletest |

## 🎯 Usage

### Interactive Wizard (Recommended)

```bash
sparkstart new
```

Guides you through:
- Project name
- Programming language
- Dev container setup (Docker)
- Code quality tools (formatters, linters, pre-commit)
- Educational project option (learn by building games)
- GitHub push

### Direct Mode with Flags

```bash
# Python project with all features
sparkstart new my-app --lang python --devcontainer --tools --github

# Rust project for learning
sparkstart new learning-rust --lang rust --tutorial

# Quick JavaScript project
sparkstart new web-app --lang javascript --tools

# C++ with Docker environment
sparkstart new cpp-project --lang cpp --devcontainer
```

### Available Options

```
--lang, -l LANG           Language: python, rust, javascript, cpp
--template TEMPLATE       Template: pygame (python only)
--tutorial, -t            Educational project with tests and guides
--devcontainer, -d        Docker dev container with direnv + compose
--tools                   Formatters, linters, pre-commit hooks
--github                  Create and push to GitHub repository
--help, -h                Show help information
```

### Commands

```bash
sparkstart new [NAME]     Create new project
sparkstart help           Show comprehensive help
sparkstart version        Show version
```

## 🎁 What's Included

### Every Project Gets:

✅ **Project Structure**
- Language-specific folder layout
- Working starter code ("Hello World")
- README.md and .gitignore
- Git repository (pre-initialized)

✅ **Documentation**
- GETTING_STARTED.md (language-specific setup guide)
- Inline code comments
- Example code patterns

✅ **Testing Setup**
- Test files and examples
- Pre-configured test runner
- Sample test cases

### With `--devcontainer`:

🐳 **Docker Development Environment**
- `.devcontainer/` with Dockerfile
- `docker-compose.yaml` for orchestration
- `.envrc` for automatic environment setup (direnv)
- Pre-installed tools and dependencies
- Reproducible development across machines

### With `--tools`:

🛠️ **Code Quality Tools**
- **Formatters**: black (Python), prettier (JS), rustfmt (Rust), clang-format (C++)
- **Linters**: ruff (Python), eslint (JS), clippy (Rust)
- **Pre-commit hooks**: Automatic code checking before commits
- **.editorconfig**: Editor consistency across team

### With `--tutorial`:

🎓 **Educational Game Project**
- Complete working game (Pygame for Python)
- Tutorial and learning resources
- Exercises to practice concepts
- Tests to verify your progress

### With `--github`:

☁️ **GitHub Integration**
- Automatic repository creation
- Secure token handling (saved locally, never committed)
- Initial commit and push
- Ready for collaboration

## 💡 Pro Tips

- **Use `--devcontainer`** for consistent development across team and machines
- **Use `--tools`** to enforce code quality from the start
- **Use `--tutorial`** to learn a new language with guided exercises
- **Check `GETTING_STARTED.md`** in your new project for language-specific commands
- **GitHub token** is saved to `.sparkstart.env` (never committed to git)

## 🔧 Requirements

### Minimum

- **Python** 3.8+ → [Download](https://www.python.org/downloads/)
- **Git** → [Download](https://git-scm.com/downloads)

### Optional

- **Docker** (for `--devcontainer`) → [Download](https://www.docker.com/get-started)
- **Language runtime** for chosen language:
  - Python: Built-in ✅
  - Rust: [rustup.rs](https://rustup.rs/)
  - Node.js: [nodejs.org](https://nodejs.org/)
  - C++: gcc/clang (or use `--devcontainer`)

## 📦 Installation

### From PyPI (Recommended)

Install with `pipx` (works on all platforms — Linux, macOS, WSL, Windows):

```bash
pipx install sparkstart
```

`pipx` installs CLI tools in isolated environments and exposes the binary globally.
If you don't have `pipx` yet:

| Platform | Command |
|----------|---------|
| Ubuntu / WSL | `sudo apt install pipx` |
| macOS (Homebrew) | `brew install pipx` |
| Windows / macOS (python.org) | `pip install pipx` |

> **Why not `pip install` directly?** On Ubuntu 23.04+, macOS with Homebrew Python,
> and WSL, `pip install` to the system Python is blocked (PEP 668). `pipx` is the
> correct tool for installing Python CLI applications globally.

### From Source

```bash
git clone https://github.com/majorlongval/sparkstart
cd sparkstart
pip install -e .
```

### Verify Installation

```bash
sparkstart version
```

## 🎮 Examples

### Python Game Project

```bash
sparkstart new my-game --lang python --template pygame --tutorial
cd my-game
cat GETTING_STARTED.md  # See setup instructions
```

### Rust Project with DevContainer

```bash
sparkstart new learn-rust --lang rust --devcontainer --tutorial
cd learn-rust
direnv allow                    # Auto-activate environment
docker compose up -d            # Start dev container
docker compose exec dev cargo test  # Run tests in container
```

### Production JavaScript Project

```bash
sparkstart new production-app --lang javascript --tools --github --devcontainer
cd production-app
npm install
npm test
git push
```

### C++ Academic Project

```bash
sparkstart new algorithms --lang cpp --tutorial --tools
cd algorithms
mkdir build && cd build && cmake .. && make
./test_algorithms
```

## 🛠️ Shell Completion

### Bash

Add to `~/.bashrc`:

```bash
eval "$(sparkstart --bash-completion)"
```

### Zsh

Add to `~/.zshrc`:

```bash
eval "$(sparkstart --zsh-completion)"
```

Then run:

```bash
source ~/.bashrc  # or ~/.zshrc
```

Now you get autocomplete for:
- Commands (new, help, version)
- Languages (python, rust, javascript, cpp)
- Templates (pygame)
- All flags and options

## 📚 Documentation

- **[Getting Started](./docs/GETTING_STARTED.md)** — Detailed setup guide
- **[Contributing Guide](./CONTRIBUTING.md)** — How to contribute
- **[Changelog](./CHANGELOG.md)** — Version history and updates
- **[Architecture](./docs/architecture.md)** — How sparkstart works

## 🐛 Troubleshooting

### Missing Docker?

```bash
# macOS
brew install docker

# Linux (Ubuntu/Debian)
sudo apt install docker.io

# Windows
# Download Docker Desktop: https://www.docker.com/get-started
```

### Missing Git?

```bash
# macOS
brew install git

# Linux (Ubuntu/Debian)
sudo apt install git

# Windows
# Download: https://git-scm.com/
```

### Project Already Exists?

Use a different name:

```bash
sparkstart new my-project-v2
```

Or remove the existing directory:

```bash
rm -rf my-project
sparkstart new my-project
```

### GitHub Token Issues?

1. The token is saved to `.sparkstart.env` (never committed)
2. To regenerate: Remove `.sparkstart.env` and re-run with `--github`
3. Personal access token docs: [GitHub Docs](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

## 🤝 Contributing

We'd love your help! See [CONTRIBUTING.md](./CONTRIBUTING.md) for:
- How to set up development environment
- Running tests
- Submitting pull requests
- Code style guidelines

## 📝 License

MIT License — See [LICENSE](./LICENSE) for details

## 🎉 Quick Facts

- ⚡ **Fast** — Creates projects in seconds
- 🔒 **Secure** — GitHub tokens never committed
- 🎯 **Focused** — Does one thing well
- 📚 **Educational** — Learn new languages faster
- 🛠️ **Professional** — Production-ready code quality
- 🐳 **Docker-Ready** — Dev containers included

## 📞 Support

- **Questions?** Check the [help system](README.md#-documentation)
- **Found a bug?** [Open an issue](https://github.com/majorlongval/sparkstart/issues)
- **Have an idea?** [Create a discussion](https://github.com/majorlongval/sparkstart/discussions)

---

**Ready to start?** Run `sparkstart new` and create your first project! 🚀
