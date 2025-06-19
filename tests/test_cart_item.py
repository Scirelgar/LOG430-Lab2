import pytest
from src.model.cart_item import CartItem


class TestCartItem:
    def test_init(self):
        # Arrange & Act
        cart_item = CartItem(
            product_id=1, product_name="Test Product", quantity=2, unit_price=9.99
        )

        # Assert
        assert cart_item.product_id == 1
        assert cart_item.product_name == "Test Product"
        assert cart_item.quantity == 2
        assert cart_item.unit_price == 9.99

    def test_get_total_price(self):
        # Arrange
        cart_item = CartItem(
            product_id=1, product_name="Test Product", quantity=2, unit_price=9.99
        )

        # Act
        total_price = cart_item.get_total_price()

        # Assert
        assert total_price == 19.98  # 2 * 9.99 = 19.98

    def test_repr(self):
        # Arrange
        cart_item = CartItem(
            product_id=1, product_name="Test Product", quantity=2, unit_price=9.99
        )

        # Act
        result = repr(cart_item)

        # Assert
        assert "CartItem" in result
        assert "1" in result
        assert "Test Product" in result
        assert "2" in result
        assert "9.99" in result
