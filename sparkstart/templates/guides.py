import textwrap

def get_getting_started(name: str, lang: str, has_devcontainer: bool) -> str:
    """Generate language-specific GETTING_STARTED.md"""

    base = textwrap.dedent(f"""
        # Getting Started with {name}

        Welcome! This project includes several tools to help you code efficiently.

        ## What's Inside

        ### Project Files
        - **src/** - Your source code
        - **tests/** - Test files
        - **README.md** - Project overview
        """).strip()

    if has_devcontainer:
        base += textwrap.dedent("""

            ### Development Environment
            - **.devcontainer/** - Docker dev container configuration
            - **.envrc** - Environment setup (requires `direnv`)
            - **compose.yaml** - Docker Compose for orchestration
            """).strip()

    lang_guides = {
        "python": textwrap.dedent("""

            ## Python Setup

            ### Option 1: Using direnv (Recommended)
            ```bash
            direnv allow           # Auto-activates virtual environment
            pip install -r requirements.txt
            ```

            If you don't have direnv, install it: https://direnv.net

            ### Option 2: Manual Virtual Environment
            ```bash
            python3 -m venv .venv
            source .venv/bin/activate
            pip install -r requirements.txt
            ```

            ### Running Your Code
            ```bash
            python src/main.py
            ```

            ### Running Tests
            ```bash
            pytest tests/
            ```

            ### Code Quality
            ```bash
            black src/          # Format code
            ruff check src/     # Lint for issues
            pylint src/main.py  # Detailed analysis
            ```
            """).strip(),

        "rust": textwrap.dedent("""

            ## Rust Setup

            ### Option 1: Using direnv (Recommended)
            ```bash
            direnv allow           # Auto-sets Rust flags
            ```

            ### Option 2: Manual Setup
            ```bash
            rustup update
            cargo build
            ```

            ### Running Your Code
            ```bash
            cargo run
            ```

            ### Running Tests
            ```bash
            cargo test
            ```

            ### Code Quality
            ```bash
            cargo fmt             # Format code
            cargo clippy          # Lint for issues
            cargo clippy --fix    # Auto-fix common issues
            ```
            """).strip(),

        "javascript": textwrap.dedent("""

            ## JavaScript/Node.js Setup

            ### Option 1: Using direnv (Recommended)
            ```bash
            direnv allow           # Auto-loads Node.js
            npm install
            ```

            ### Option 2: Manual Setup
            ```bash
            node --version         # Check Node.js is installed
            npm install
            ```

            ### Running Your Code
            ```bash
            npm start
            # or
            node src/main.js
            ```

            ### Running Tests
            ```bash
            npm test
            ```

            ### Code Quality
            ```bash
            npm run lint           # ESLint
            npm run format         # Prettier
            npm run lint -- --fix  # Auto-fix issues
            ```
            """).strip(),

        "cpp": textwrap.dedent("""

            ## C++ Setup

            ### Building
            ```bash
            mkdir -p build
            cd build
            cmake ..
            make
            ```

            ### Running Your Code
            ```bash
            ./build/myapp
            ```

            ### Running Tests
            ```bash
            cd build
            ctest
            ```

            ### Code Quality
            ```bash
            clang-format -i src/*.cpp    # Format code
            clang-tidy src/main.cpp      # Lint for issues
            ```
            """).strip(),
    }

    base += "\n\n" + lang_guides.get(lang, "")

    if has_devcontainer:
        base += textwrap.dedent("""

            ## Using Dev Containers

            ### With VSCode
            1. Install the "Dev Containers" extension
            2. Open the project folder
            3. Click "Reopen in Container" when prompted
            4. All tools are pre-installed!

            ### With Docker Compose
            ```bash
            docker compose up -d      # Start containers
            docker compose exec app bash  # Access shell
            docker compose down       # Stop containers
            ```

            ### Benefits
            - Consistent environment across machines
            - No local tool installation needed
            - Automatic dependency management
            - Works on Windows, Mac, Linux
            """).strip()

    base += textwrap.dedent("""

        ## Useful Commands

        ### Git Workflow
        ```bash
        git status              # Check changes
        git add .               # Stage files
        git commit -m "message" # Create commit
        git push                # Push to remote
        ```

        ### Viewing Documentation
        ```bash
        cat README.md           # Project overview
        cat .devcontainer/README.md  # Dev environment details (if using containers)
        ```

        ## Learning Resources

        - **Direnv Guide**: https://direnv.net/docs/installation.html
        - **Docker Docs**: https://docs.docker.com/
        - **Language Docs**:
        """).strip()

    lang_docs = {
        "python": "  - https://docs.python.org/3/",
        "rust": "  - https://doc.rust-lang.org/",
        "javascript": "  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/",
        "cpp": "  - https://en.cppreference.com/",
    }

    base += "\n" + lang_docs.get(lang, "")

    base += textwrap.dedent("""

        ## Next Steps

        1. Read the README.md for project-specific info
        2. Check out src/main.* to understand the structure
        3. Run the example code: `python src/main.py` (or your language's equivalent)
        4. Try modifying the code and running tests
        5. Explore the tools mentioned above

        Happy coding! 🚀
        """).strip()

    return base
