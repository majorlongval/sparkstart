# sparkstart Worklog

## 2026-01-21: Multi-Language Support Planning

**Goal:** Add support for Python, Rust, and JavaScript project scaffolding.

**Current state assessed:**
- CLI works with `projinit new <name>` and `projinit delete <name>`
- Python-only: creates pyproject.toml, src/, .venv, git init
- No existing tests

**Decision:** Start with multi-language basics (Option 2) before adding templates. Keep it simple — each language gets a working "Hello World" starter.

---

## 2026-01-21: Multi-Language Support Implementation

**Completed:**
1. Fixed broken `core.py` (recovered from git history, code had been truncated)
2. Added `--lang` option to CLI: `python` (default), `rust`, `javascript`
3. Each language now scaffolds with working Hello World:
   - Python: `src/main.py` with `print("Hello, world!")`
   - Rust: `src/main.rs` with `println!("Hello, world!")`
   - JavaScript: `index.js` with `console.log("Hello, world!")`
4. Updated README with new usage examples
5. Added `python-dotenv` to dependencies in pyproject.toml

**Verified:** Created test projects in all three languages, ran Hello World successfully.

---

## 2026-01-21: Published to PyPI as sparkstart

**Package name journey:** projinit → initforge → sparkstart (first two were taken)

**Published:** `pip install sparkstart` now works globally!

**Final package:** sparkstart v0.1.0

---

## 2026-01-21: C++ Scaffolding with CMake + Conan

**Added:** `--lang cpp` option that scaffolds:
- `CMakeLists.txt` with inline comments explaining CMake concepts
- `conanfile.txt` with comments on Conan dependency management
- `src/main.cpp` Hello World
- `.gitignore` for build artifacts

**Goal:** Make the CMake + Conan relationship understandable for newcomers.

---

## 2026-01-21: Testing C++ Scaffolding

**Tested:** Created test C++ project and verified scaffolding works.

**Results:**
- ✅ Project structure created correctly (CMakeLists.txt, conanfile.txt, src/main.cpp)
- ✅ g++ can compile `src/main.cpp` directly → "Hello, world!" works

**Toolchain availability on this system:**
- ✅ g++ (v13.3.0)
- ❌ cmake
- ❌ clang++
- ❌ conan

**Implemented:** Added g++ check in `_scaffold_cpp()`. Now raises helpful error with install instructions for Ubuntu/Debian/Fedora/Arch/macOS if g++ is missing.

---

## Future: Dev Containers for Zero-Friction Setup

**Marketing concept:** "Code when you have the spark" ⚡ — eliminate all friction for newcomers.

**Vision:** User runs `sparkstart new myproject --lang cpp` and gets a project that "just works" in any editor that supports dev containers.

### Milestone 1: Scaffold dev container files
- Generate `.devcontainer/devcontainer.json`
- Optional `Dockerfile` with language toolchain
- **Effort:** ~1-2 hours

### Milestone 2: Detect + guide Docker/VS Code installation
How hard is it to install these for the user?

| Tool | Linux | macOS | Windows |
|------|-------|-------|---------|
| **Docker** | `curl -fsSL get.docker.com \| sh` | Docker Desktop installer (GUI) | Docker Desktop (GUI + WSL2) |
| **VS Code** | `snap install code` or `.deb` | `brew install --cask visual-studio-code` | Installer (GUI) |

**Reality check:**
- Linux: Could script this (with sudo)
- macOS/Windows: GUI installers, harder to automate
- **Alternative:** Detect what's missing, open download page, guide user

### Milestone 3: The dream — one-click "spark"?
- User downloads sparkstart as standalone binary
- Binary checks for Docker, offers to install if missing
- Creates project + opens in VS Code with dev container ready

**This is a big vision** — maybe version 1.0 or 2.0 territory.

---

## 2026-01-21: v0.1.1 Bug Fix & Release

**Issue:** User reported `ModuleNotFoundError: No module named 'projinit'` when running `sparkstart`.
**Cause:** Published v0.1.0 contained stale import reference.
**Fix:**
- Bumped version to v0.1.1
- Rebuilt distribution (imports are correct locally)

**Status:**
- Release built.
- Upload failed (403 Forbidden). Troubleshooting auth.
- **Success:** Published v0.1.1 to PyPI. ✅

---

## 2026-01-21: v0.1.2 Features (C++ Polish)

**Features Added:**
- **Dependency Checks:** `sparkstart` now checks for `cmake` (required) and `conan` (optional).
- **Enhanced Documentation:** C++ scaffolding now includes a detailed `README.md` and "mini-tutorials" in `CMakeLists.txt`.
- **Dev Container Support:** Added `--devcontainer` flag to generate `.devcontainer/devcontainer.json`.

**Status:** Ready to release v0.1.2.


- **Success:** Published v0.1.2 to PyPI. ✅

## 2026-01-21: Standalone Binary (MVP)

**Goal:** Create a single-file executable to reduce "setup fatigue" for new users.

**Implemented:**
- Added `pyinstaller` to dev-dependencies.
- Created `scripts/build_dist.py` automation.
- **Output:** `dist/sparkstart` (Linux binary, ~18MB).

**Verified:**
- ✅ Binary runs without Python/pip on the path.
- ✅ Successfully scaffolds a C++ project (`sparkstart new test --lang cpp`).
- ✅ Dev container files are generated correctly.

## 2026-01-21: Environment Detection (Milestone 2)

**Goal:** Detect missing tools (Docker, VS Code) and guide the user to install them.

**Implemented:**
- Added `sparkstart.checks` module.
- Integrated `check_docker()` and `check_vscode()` into CLI.
- **Behavior:**
  - If `sparkstart new ... --devcontainer` is run:
  - Checks if `docker` and `code` are in PATH.
  - If missing: Prints specific warning and opens the download page in the default browser.

**Verified:**
- ✅ Positive Test: Running on valid environment passes silently.
- ✅ Negative Test: Simulated missing `docker` binary → correctly warned and attempted to open browser.

## 2026-02-21: CI — Auto-publish to PyPI on master merge

**Change:** Replaced manual tag-triggered PyPI releases with automatic publishing on every merge to master.

**Details:**
- GitHub Actions workflow now triggers on push to master
- Added `contents:write` permission to the release job so it can create tags
- No more manual `git tag` + push dance to release

---

## 2026-02-21: v1.0.1 Patch Release

**Bumped version** from 1.0.0 → 1.0.1.

No functional changes — version bump only.

---

## 2026-02-21: Fix — Wizard UX & Quickstart Accuracy

**Issues fixed:**
- Replaced gendered wizard emoji 🧙‍♂️ with neutral 🧙 in wizard prompt and help text
- Clarified git/GitHub section: local git repo is always created; GitHub push is explicitly optional
- Removed empty `requirements.txt` from Python scaffolder (deps live in `pyproject.toml`)
- Corrected quickstart install command from `pip install -r requirements.txt` to `pip install -e '.[test]'` in both quickstart output and `GETTING_STARTED.md` template

---

## 2026-02-21: Feat — Integration Test Skeleton

**Added:** `tests/integration/test_integration.py` — a skeleton of end-to-end tests that run `sparkstart new` and verify that generated projects actually install, run, and pass their own tests.

**Coverage planned (all marked TODO):**
- All four languages (Python, Rust, JavaScript, C++)
- Templates (pygame)
- Flags: `--devcontainer`, `--tools`, `--tutorial`
- Git init verification

**Status:** Skeleton only — test bodies are stubbed with `TODO` and will be fleshed out as the test suite matures.
