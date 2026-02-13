import textwrap

DEVCONTAINER_JSON = textwrap.dedent("""
    {
      "name": "C++",
      "image": "mcr.microsoft.com/devcontainers/cpp:1-debian-12",
      "features": {
        "ghcr.io/devcontainers/features/common-utils:2": {
          "installZsh": true,
          "configureZshAsDefaultShell": true,
          "installOhMyZsh": true,
          "upgradePackages": true
        }
      },
      "postCreateCommand": "sudo apt-get update && sudo apt-get install -y neovim",
      "customizations": {
        "vscode": {
          "extensions": [
            "ms-vscode.cpptools",
            "ms-vscode.cmake-tools",
            "waderyan.gitblame",
            "asvetliakov.vscode-neovim"
          ]
        }
      }
    }
""").strip()

DEVCONTAINER_PYTHON = textwrap.dedent("""
    {
      "name": "Python 3",
      "image": "mcr.microsoft.com/devcontainers/python:1-3.12-bullseye",
      "features": {
        "ghcr.io/devcontainers/features/common-utils:2": {
          "installZsh": true,
          "configureZshAsDefaultShell": true,
          "installOhMyZsh": true,
          "upgradePackages": true
        }
      },
      "postCreateCommand": "pip install -r requirements.txt",
      "customizations": {
        "vscode": {
          "extensions": [
            "ms-python.python",
            "ms-python.vscode-pylance",
            "njpwerner.autodocstring",
            "charliermarsh.ruff"
          ]
        }
      }
    }
""").strip()

DEVCONTAINER_RUST = textwrap.dedent("""
    {
      "name": "Rust",
      "image": "mcr.microsoft.com/devcontainers/rust:1-bullseye",
      "features": {
        "ghcr.io/devcontainers/features/common-utils:2": {
          "installZsh": true,
          "configureZshAsDefaultShell": true,
          "installOhMyZsh": true,
          "upgradePackages": true
        }
      },
      "postCreateCommand": "rustup component add rust-analyzer",
      "customizations": {
        "vscode": {
          "extensions": [
            "rust-lang.rust-analyzer",
            "serayuzgur.crates",
            "tamasfe.even-better-toml"
          ]
        }
      }
    }
""").strip()

DEVCONTAINER_JAVASCRIPT = textwrap.dedent("""
    {
      "name": "Node.js",
      "image": "mcr.microsoft.com/devcontainers/javascript-node:1-20-bullseye",
      "features": {
        "ghcr.io/devcontainers/features/common-utils:2": {
          "installZsh": true,
          "configureZshAsDefaultShell": true,
          "installOhMyZsh": true,
          "upgradePackages": true
        }
      },
      "postCreateCommand": "npm install",
      "customizations": {
        "vscode": {
          "extensions": [
            "dbaeumer.vscode-eslint",
            "esbenp.prettier-vscode",
            "vue.volar"
          ]
        }
      }
    }
""").strip()
