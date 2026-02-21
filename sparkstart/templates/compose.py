import textwrap

COMPOSE_PYTHON = textwrap.dedent("""
    version: '3.8'

    services:
      app:
        build: .
        container_name: ${PROJECT_NAME:-app}
        volumes:
          - .:/workspace
          - /workspace/.venv
        working_dir: /workspace
        environment:
          - PYTHONUNBUFFERED=1
        command: /bin/bash
        stdin_open: true
        tty: true
""").strip()

COMPOSE_RUST = textwrap.dedent("""
    version: '3.8'

    services:
      app:
        build: .
        container_name: ${PROJECT_NAME:-app}
        volumes:
          - .:/workspace
          - cargo-cache:/usr/local/cargo
        working_dir: /workspace
        command: /bin/bash
        stdin_open: true
        tty: true

    volumes:
      cargo-cache:
""").strip()

COMPOSE_JAVASCRIPT = textwrap.dedent("""
    version: '3.8'

    services:
      app:
        build: .
        container_name: ${PROJECT_NAME:-app}
        volumes:
          - .:/workspace
          - node_modules:/workspace/node_modules
        working_dir: /workspace
        command: /bin/bash
        stdin_open: true
        tty: true

    volumes:
      node_modules:
""").strip()

COMPOSE_CPP = textwrap.dedent("""
    version: '3.8'

    services:
      app:
        build: .
        container_name: ${PROJECT_NAME:-app}
        volumes:
          - .:/workspace
          - build-cache:/workspace/build
        working_dir: /workspace
        command: /bin/bash
        stdin_open: true
        tty: true

    volumes:
      build-cache:
""").strip()
