import textwrap

ENVRC_PYTHON = textwrap.dedent("""
    # direnv configuration for Python project
    # Usage: direnv allow

    export VIRTUAL_ENV=.venv
    if [ ! -d "$VIRTUAL_ENV" ]; then
      python3 -m venv "$VIRTUAL_ENV"
      "$VIRTUAL_ENV/bin/pip" install -U pip
    fi
    PATH_add "$VIRTUAL_ENV/bin"
""").strip()

ENVRC_RUST = textwrap.dedent("""
    # direnv configuration for Rust project
    # Usage: direnv allow

    export RUSTFLAGS="-D warnings"
    use_nix  # uncomment if you use nix flakes
""").strip()

ENVRC_JAVASCRIPT = textwrap.dedent("""
    # direnv configuration for Node.js project
    # Usage: direnv allow

    use node 20
""").strip()

ENVRC_CPP = textwrap.dedent("""
    # direnv configuration for C++ project
    # Usage: direnv allow

    export CFLAGS="-Wall -Wextra -pedantic"
    export CXXFLAGS="-Wall -Wextra -pedantic"
""").strip()
