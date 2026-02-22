import textwrap

GITIGNORE_PYTHON = textwrap.dedent("""
    __pycache__/
    .venv/
    *.pyc
    .DS_Store
    .sparkstart.env
""").strip()
