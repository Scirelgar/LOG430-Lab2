import os
import sys


def ensure_empty_init_files():
    """Creates empty __init__.py files in all necessary directories."""
    dirs = ["src", "src/model", "src/repository", "src/controller"]

    for directory in dirs:
        init_path = os.path.join(directory, "__init__.py")
        if not os.path.exists(init_path):
            print(f"Creating {init_path}")
            with open(init_path, "w") as f:
                f.write(
                    "# This file intentionally left empty to mark this directory as a Python package\n"
                )
        else:
            print(f"{init_path} already exists")


def add_path_to_test_files():
    """Adds path fixing code to all test files."""
    test_files = [
        f for f in os.listdir("tests") if f.startswith("test_") and f.endswith(".py")
    ]

    for test_file in test_files:
        file_path = os.path.join("tests", test_file)
        print(f"Checking {file_path}")

        with open(file_path, "r") as f:
            content = f.read()

        # Add import path code if not present
        if "import sys" not in content or "sys.path.insert" not in content:
            print(f"  Adding path import code to {test_file}")
            new_content = (
                """import os
import sys
# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

"""
                + content
            )
            with open(file_path, "w") as f:
                f.write(new_content)
        else:
            print(f"  Path import code already exists in {test_file}")


if __name__ == "__main__":
    # Execute from project root
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print("Working in:", os.getcwd())

    ensure_empty_init_files()
    add_path_to_test_files()

    print("\nDone! Now try running the tests with:")
    print("python -m pytest tests -v")
