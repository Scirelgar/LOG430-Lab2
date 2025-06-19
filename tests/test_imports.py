import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

print("Python path:", sys.path)
print("Working directory:", os.getcwd())

try:
    import src.model.product

    print("Successfully imported src.model.product")
except Exception as e:
    print(f"Error importing src.model.product: {e}")

try:
    from src.model.product import Product

    print("Successfully imported Product class")
except Exception as e:
    print(f"Error importing Product class: {e}")

print("\nAttempting to import with absolute path...")
try:
    sys.path.insert(
        0,
        os.path.abspath(
            "c:\\Users\\Samuel Richard\\OneDrive - ETS\\Session 7 E25\\LOG430\\LOG430-Laboratoires\\LOG430-Lab1"
        ),
    )
    import src.model.product

    print("Successfully imported with absolute path")
except Exception as e:
    print(f"Error with absolute path: {e}")
