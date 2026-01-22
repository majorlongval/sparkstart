#!/usr/bin/env python3
import subprocess
import sys
import shutil
import pathlib
import textwrap

# Ensure we are running from project root
PROJECT_ROOT = pathlib.Path(__file__).parent.parent.resolve()
DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build"
BINARY_NAME = "sparkstart"

def check_pyinstaller():
    """Check if pyinstaller is available."""
    try:
        import PyInstaller
    except ImportError:
        print("❌ PyInstaller not found.")
        print("   Please run: pip install -e .[test]")
        sys.exit(1)

def clean():
    """Clean build artifacts."""
    print(f"🧹 Cleaning {DIST_DIR} and {BUILD_DIR}...")
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    
    # Also clean .spec file if it exists in root
    spec_file = PROJECT_ROOT / f"{BINARY_NAME}.spec"
    if spec_file.exists():
        spec_file.unlink()

def build():
    """Run PyInstaller."""
    print("🔨 Building standalone binary...")
    
    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name", BINARY_NAME,
        "--clean",
        # Point to the entry point. 
        # Since we use typer, pointing to cli.py is usually best, 
        # or we can treat the package as a module. 
        # Let's try pointing to the package execution method.
        # Actually, for Typer/Click apps often a small entry script is easiest if the module approach fails,
        # but "sparkstart/cli.py" should work if we verify imports.
        # Better: create a tiny entrypoint script dynamically or use the installed module.
        # Let's try pointing directly at the file sparkstart/cli.py but we need strict import handling.
        # Safest for installed package: Use a generated entry script.
    ]
    
    # Let's use a temporary entrypoint script to ensure relative imports work correctly
    # when pyinstaller analyzes it.
    entry_script = PROJECT_ROOT / "entry_point.py"
    entry_script.write_text("from sparkstart.cli import app; app()")
    
    try:
        cmd.append(str(entry_script))
        subprocess.run(cmd, check=True, cwd=PROJECT_ROOT)
    finally:
        if entry_script.exists():
            entry_script.unlink()

def verify():
    """Verify the binary works."""
    binary_path = DIST_DIR / BINARY_NAME
    if not binary_path.exists():
        print(f"❌ Binary not found at {binary_path}")
        sys.exit(1)
        
    print(f"✅ Binary created at {binary_path}")
    print("   Running smoke test (help command)...")
    
    try:
        result = subprocess.run([str(binary_path), "--help"], capture_output=True, text=True, check=True)
        print("   Smoke test passed! stdout snippet:")
        print(textwrap.indent(result.stdout[:200] + "...", "      "))
    except subprocess.CalledProcessError as e:
        print("❌ Smoke test failed!")
        print(e.stderr)
        sys.exit(1)

def main():
    check_pyinstaller()
    clean()
    build()
    verify()
    print("\n🎉 Build successful!")

if __name__ == "__main__":
    main()
