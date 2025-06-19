import pytest
import sys
import os

# Add the project root directory to Python path to ensure imports work correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Print the Python path for debugging
print("Python path:", sys.path)

if __name__ == "__main__":
    # Run pytest with verbose output
    print("Running tests from:", os.path.dirname(__file__))
    pytest.main(["-v"])
