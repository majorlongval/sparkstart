import textwrap

GITIGNORE_CPP = textwrap.dedent("""
    # Build output
    build/
    
    # CMake generated files
    CMakeCache.txt
    CMakeFiles/
    cmake_install.cmake
    Makefile
    
    # Conan
    conan_output/
    
    # IDE
    .vscode/
    .idea/
    
    # General
    .DS_Store
    .sparkstart.env
    
    # Testing
    test_results/
""").strip()

README_CPP = textwrap.dedent("""
    # {name}
    
    A C++ project initialized by `sparkstart`.
    
    ## 🚀 Quick Start
    
    ### Prerequisites
    - **C++ Compiler** (g++, clang++, or MSVC)
    - **CMake** (3.15+)
    - **Conan** (Optional, for dependencies)
    
    ### Build & Run
    We use an **out-of-source** build workflow to keep your source directory clean.
    
    ```bash
    # 1. Configure (Generate Build Files)
    cd build
    cmake ..
    
    # 2. Build (Compile)
    cmake --build .
    
    # 3. Run
    ./{name}
    ```
    
    ## 📂 Project Structure
    - `src/`             - Your C++ source files (Start with main.cpp)
    - `build/`           - Build artifacts (Makefiles, binaries) - keep this clean!
    - `CMakeLists.txt`   - The "Recipe" for CMake to build your project
    - `conanfile.txt`    - List of libraries you want to install
    
    ## 📚 "How-To" Mini-Guides
    
    ### How to add a new Source Folder?
    1. Create the folder (e.g. `src/utils/`)
    2. Add a `CMakeLists.txt` inside strictly identifying its library name.
    3. In the main `CMakeLists.txt`, add: `add_subdirectory(src/utils)`
    *(See comments in CMakeLists.txt for examples)*
    
    ### How to add a Dependency (Library)?
    1. Search for it on [Conan Center](https://conan.io/center) (e.g. `fmt`).
    2. Add it to `conanfile.txt` under `[requires]`.
    3. Run: `conan install . --output-folder=build --build=missing`
    4. Uncomment the Conan lines in `CMakeLists.txt` to link it.
""").strip()

BUILD_SH = textwrap.dedent("""
    #!/bin/bash
    set -e
    
    # ==============================================================================
    # Build Script - a shortcut for the CMake workflow
    # ==============================================================================
    
    echo "🚀 Building {name}..."
    
    # 1. Create build directory
    mkdir -p build
    
    # 2. Dependency Management (Optional)
    # If you use Conan, uncomment the following line:
    # conan install . --output-folder=build --build=missing
    
    # 3. Configure (CMake)
    cd build
    cmake ..
    
    # 4. Build (Compile)
    cmake --build .
    
    echo "✅ Build complete! Run with: ./build/{name}"
""").strip()
