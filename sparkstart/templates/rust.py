import textwrap

GITIGNORE_RUST = textwrap.dedent("""
    /target
    .DS_Store
    .sparkstart.env
""").strip()
