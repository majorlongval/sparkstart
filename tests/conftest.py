import pytest
import os
import shutil
import pathlib
import subprocess

@pytest.fixture
def tmp_cwd(tmp_path):
    """
    Fixture to run tests in a temporary directory.
    Disables git signing to avoid test environment issues.
    Yields the temporary directory path.
    """
    original_cwd = os.getcwd()

    # Disable git signing in tests to avoid environment issues
    subprocess.run(["git", "config", "--global", "commit.gpgsign", "false"], check=False)
    subprocess.run(["git", "config", "--global", "user.email", "test@sparkstart.local"], check=False)
    subprocess.run(["git", "config", "--global", "user.name", "Test User"], check=False)

    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(original_cwd)
