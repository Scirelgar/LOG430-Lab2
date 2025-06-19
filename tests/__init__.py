import os
import sys

# Add parent directory to path to make imports work correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Print Python path when tests are loaded (for debugging)
if __name__ != "__main__":
    print("Python path in test package:", sys.path)
