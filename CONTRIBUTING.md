# Contributing to sparkstart

First off, thanks for considering contributing to sparkstart! It's people like you that make sparkstart such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps which reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include screenshots and animated GIFs if possible**
- **Include your environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and the expected behavior**
- **Explain why this enhancement would be useful**

### Pull Requests

- Follow the Python style guide (PEP 8)
- Include appropriate test cases
- Update documentation as needed
- Add an entry to CHANGELOG.md
- End all files with a newline

## Development Setup

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR-USERNAME/sparkstart.git
cd sparkstart
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -e ".[test]"
```

### 4. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

## Development Workflow

### Running Tests

```bash
pytest tests/ -v
```

With coverage:

```bash
pytest tests/ --cov=sparkstart --cov-report=html
```

### Code Style

We use PEP 8 with a line length of 88 characters (Black's default).

```bash
# Format code
black sparkstart/

# Check style
flake8 sparkstart/

# Type checking
mypy sparkstart/
```

### Building the Project

```bash
# Build distribution
python -m build

# Test installation
pip install dist/sparkstart-*.whl
```

## Project Structure

```
sparkstart/
├── cli.py           # Command-line interface
├── core.py          # Core project creation logic
├── validation.py    # Input validation
├── wizard.py        # Interactive wizard
├── checks.py        # Environment checks
├── scaffolding/     # Project templates for each language
│   ├── python.py
│   ├── rust.py
│   ├── javascript.py
│   └── cpp.py
├── github_utils.py  # GitHub integration
└── utils/           # Utility functions
    ├── output.py    # Pretty output formatting
    ├── progress.py  # Progress indicators
    ├── suggestions.py # Error suggestions
    ├── completion.py # Shell completion
    └── help.py      # Help system
```

## Key Files

- `sparkstart/cli.py` — Main CLI entry point
- `sparkstart/core.py` — Project creation logic
- `sparkstart/scaffolding/` — Language-specific templates
- `tests/` — Test suite
- `CHANGELOG.md` — Version history
- `README.md` — User documentation

## Making Changes

### 1. Create a Branch

```bash
git checkout -b feature/my-feature
```

### 2. Make Your Changes

- Write clean, well-documented code
- Add tests for new functionality
- Follow PEP 8 style guide
- Update docstrings

### 3. Test Your Changes

```bash
# Run tests
pytest tests/

# Test the CLI manually
python -c "from sparkstart.cli import app; app(['new', 'test-project'])"
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "Add: description of changes

- Bullet point 1
- Bullet point 2

Fixes #123"
```

Commit messages should:
- Start with present tense ("Add" not "Added")
- Reference related issues when applicable
- Be clear and descriptive

### 5. Push to Your Fork

```bash
git push origin feature/my-feature
```

### 6. Create Pull Request

- Use a clear and descriptive title
- Reference any related issues
- Describe the changes in detail
- Include before/after screenshots if applicable
- Ensure all tests pass

## Pull Request Process

1. Ensure all tests pass: `pytest tests/ -v`
2. Update documentation if needed
3. Add CHANGELOG entry
4. Wait for review
5. Make requested changes
6. Get approval and merge

## Commit Message Format

```
[Type]: Brief description

Longer description explaining what and why.

- Bullet point for important detail
- Another detail if needed

Fixes #123
Related to #456
```

**Types:**
- `Add` — New feature
- `Fix` — Bug fix
- `Update` — Enhancement to existing feature
- `Docs` — Documentation changes
- `Refactor` — Code refactoring
- `Test` — Test additions/changes
- `Style` — Code style changes

## Testing Guidelines

### Writing Tests

```python
def test_feature_name():
    """Test that feature does X when given Y."""
    # Setup
    input_value = "test"

    # Execute
    result = function_under_test(input_value)

    # Assert
    assert result == "expected_output"
```

### Test Organization

- Place tests in `tests/` directory
- Use descriptive test names
- One test file per module
- Group related tests in classes

## Documentation

### Code Comments

- Use for WHY, not WHAT (code shows what)
- Keep comments up-to-date
- Use for complex logic or non-obvious decisions

```python
# Good
# Use binary search for O(log n) lookup
def find_item(items, target):
    ...

# Avoid
# Set x to 5
x = 5
```

### Docstrings

- Use Google-style docstrings
- Document parameters, returns, and exceptions
- Include usage examples for complex functions

```python
def create_project(name: str, language: str) -> Path:
    """Create a new project with the given name and language.

    Args:
        name: Project name (alphanumeric + hyphens)
        language: Programming language (python, rust, javascript, cpp)

    Returns:
        Path to created project directory

    Raises:
        ValidationError: If name or language is invalid
        FileExistsError: If project directory already exists
    """
```

## Performance Guidelines

- Profile before optimizing
- Prefer readability over micro-optimizations
- Cache expensive operations when appropriate
- Consider memory usage for large operations

## Security Guidelines

- Never log sensitive information (tokens, passwords)
- Validate all user input
- Sanitize file paths to prevent directory traversal
- Keep dependencies up-to-date
- Review GitHub token handling carefully

## Roadmap

See our GitHub issues and projects for:
- Planned features
- Known bugs
- Enhancement requests
- Community feedback

## Questions?

Feel free to:
- Open a GitHub issue with [QUESTION] tag
- Check existing issues and discussions
- Look at the documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- CHANGELOG.md
- GitHub contributors page
- Release notes

---

Thank you for contributing to sparkstart! 🎉
