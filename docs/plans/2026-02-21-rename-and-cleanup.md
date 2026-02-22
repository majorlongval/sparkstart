# Rename & Repo Cleanup Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace all functional `projinit` references with `sparkstart`, delete the untracked `testPython/` test artifact, and bring `WORKLOG.md` up to date with recent commits.

**Architecture:** Three independent change sets — (1) source + template rename of `.projinit.env` → `.sparkstart.env`, (2) delete untracked test folder, (3) append missing WORKLOG entries. No new modules, no test changes needed (token filename is internal behaviour tested manually).

**Tech Stack:** Python (in-place edits), Git

---

### Task 1: Rename `.projinit.env` → `.sparkstart.env` in source utilities

**Files:**
- Modify: `sparkstart/utils/common.py` (all 4 occurrences)

**Step 1: Make the edits**

In `sparkstart/utils/common.py`, replace every occurrence of `.projinit.env` with `.sparkstart.env`:
- Line 16 docstring: `".sparkstart.env"`
- Line 17 `dotenv_values(project_root / ".sparkstart.env")`
- Line 21 `(project_root / ".sparkstart.env").write_text(...)`
- Line 25 `if ".sparkstart.env" not in lines:`
- Line 26 `lines.append(".sparkstart.env")`

**Step 2: Verify**

```bash
grep -n "projinit" sparkstart/utils/common.py
```
Expected: no output.

**Step 3: Commit**

```bash
git add sparkstart/utils/common.py
git commit -m "fix: rename .projinit.env to .sparkstart.env in token utils"
```

---

### Task 2: Rename `.projinit.env` in `core.py` docstring and comments

**Files:**
- Modify: `sparkstart/core.py` (lines 6, 130, 138, 163, 170, 175)

**Step 1: Make the edits**

Replace all occurrences of `.projinit.env` with `.sparkstart.env` in `sparkstart/core.py`.

**Step 2: Verify**

```bash
grep -n "projinit" sparkstart/core.py
```
Expected: no output.

**Step 3: Commit**

```bash
git add sparkstart/core.py
git commit -m "fix: update .projinit.env references in core.py"
```

---

### Task 3: Rename `.projinit.env` in generated `.gitignore` templates

These are the template strings baked into the Python source that get written into *generated* project `.gitignore` files.

**Files:**
- Modify: `sparkstart/templates/python.py` (line 8)
- Modify: `sparkstart/templates/rust.py` (line 6)
- Modify: `sparkstart/templates/javascript.py` (line 6)
- Modify: `sparkstart/templates/cpp.py` (line 22)

**Step 1: Make the edits**

In each file, replace `.projinit.env` with `.sparkstart.env` inside the gitignore template string.

**Step 2: Verify**

```bash
grep -rn "projinit" sparkstart/templates/
```
Expected: no output.

**Step 3: Commit**

```bash
git add sparkstart/templates/
git commit -m "fix: update generated .gitignore templates to use .sparkstart.env"
```

---

### Task 4: Rename `.projinit.env` in remaining source files

**Files:**
- Modify: `sparkstart/utils/github.py` (line 27)
- Modify: `sparkstart/utils/help.py` (line 125)

**Step 1: Make the edits**

Replace `.projinit.env` with `.sparkstart.env` in both files.

**Step 2: Verify**

```bash
grep -rn "projinit" sparkstart/
```
Expected: no output.

**Step 3: Commit**

```bash
git add sparkstart/utils/github.py sparkstart/utils/help.py
git commit -m "fix: update remaining .projinit.env references in utils"
```

---

### Task 5: Fix `.projinit.env` references in README.md

**Files:**
- Modify: `README.md` (lines 155, 316, 317)

**Step 1: Make the edits**

Replace `.projinit.env` with `.sparkstart.env` in `README.md`.

**Step 2: Verify**

```bash
grep -n "projinit" README.md
```
Expected: no output (historical WORKLOG refs are in WORKLOG.md, not README).

**Step 3: Commit**

```bash
git add README.md
git commit -m "docs: update .projinit.env references in README"
```

---

### Task 6: Delete the untracked `testPython/` directory

`testPython/` is an untracked test artifact left over from manual testing. It is not part of the project and should not be committed.

**Step 1: Remove it**

```bash
rm -rf testPython/
```

**Step 2: Verify**

```bash
git status
```
Expected: `testPython/` no longer appears in untracked files.

*(No commit needed — this folder was never tracked.)*

---

### Task 7: Update WORKLOG.md with missing entries

The worklog stops at Phase 3D (commit `76f0cba`). The following work happened since then and is not recorded:

1. **CI: auto-publish to PyPI on master merge** (`e2ca146`) — replaced manual tag-triggered releases with automatic publish on master merge
2. **Chore: bump version to 1.0.1** (`0b50876`) — patch bump; also added `contents:write` CI permission for tag creation
3. **Fix: wizard UX improvements** (`bb59402`) — neutral wizard emoji, clarified git/GitHub copy, removed empty `requirements.txt`, corrected quickstart install command to `pip install -e '.[test]'`
4. **Feat: integration test skeleton** (`0e28cf1`) — added `tests/integration/test_integration.py` with TODO end-to-end tests covering all languages, templates, devcontainer, tools, and git init

**Step 1: Append to WORKLOG.md**

Add the four entries above (dated 2026-02-21) after the last existing entry (line 160).

**Step 2: Verify**

```bash
tail -50 WORKLOG.md
```
Expected: four new dated sections visible.

**Step 3: Commit**

```bash
git add WORKLOG.md
git commit -m "docs: update worklog with CI, v1.0.1, wizard fix, and integration test entries"
```

---

## Final verification

```bash
grep -rn "projinit" sparkstart/ README.md CHANGELOG.md CONTRIBUTING.md
```
Expected: no output (WORKLOG.md historical refs are intentional and left alone).

```bash
git log --oneline -8
```
Expected: all task commits visible.
