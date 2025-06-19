import pytest
from src.model.product import Product


class TestProduct:
    def test_init(self):
        # Arrange & Act
        product = Product(
            name="Test Product",
            category="Test Category",
            price=10.99,
            stock_quantity=100,
        )

        # Assert
        assert product.name == "Test Product"
        assert product.category == "Test Category"
        assert product.price == 10.99
        assert product.stock_quantity == 100
        assert product.id is None  # ID is assigned by the database

    def test_repr(self):
        # Arrange
        product = Product(
            name="Test Product",
            category="Test Category",
            price=10.99,
            stock_quantity=100,
        )

        # Act
        result = repr(product)

        # Assert
        assert "Test Product" in result
        assert "Test Category" in result
        assert "10.99" in result
        assert "100" in result
