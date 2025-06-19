import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from src.controller.controller import Controller
from src.model.product import Product
from src.model.sale_model import Sale, SaleLine
from src.model.return_model import Return, ReturnLine
from src.model.cart_item import CartItem
from src.repository.product_repository import ProductRepository
from src.repository.sale_repository import SaleRepository
from src.repository.return_repository import ReturnRepository


class TestController:
    def test_init(self):
        # Arrange
        mock_product_repo = MagicMock(spec=ProductRepository)
        mock_sale_repo = MagicMock(spec=SaleRepository)
        mock_return_repo = MagicMock(spec=ReturnRepository)

        # Act
        controller = Controller(mock_product_repo, mock_sale_repo, mock_return_repo)

        # Assert
        assert controller.product_repository == mock_product_repo
        assert controller.sale_repository == mock_sale_repo
        assert controller.return_repository == mock_return_repo
        assert controller._cart_items == []

    def test_add_product(self):
        # Arrange
        mock_product_repo = MagicMock(spec=ProductRepository)
        controller = Controller(mock_product_repo)

        # Act
        product = controller.add_product("Test Product", "Test Category", 10.99, 100)

        # Assert
        assert product.name == "Test Product"
        assert product.category == "Test Category"
        assert product.price == 10.99
        assert product.stock_quantity == 100
        mock_product_repo.add.assert_called_once()

    def test_get_product_by_id(self):
        # Arrange
        mock_product_repo = MagicMock(spec=ProductRepository)
        mock_product = Product(
            name="Test Product",
            category="Test Category",
            price=10.99,
            stock_quantity=100,
        )
        mock_product_repo.get_by_id.return_value = mock_product
        controller = Controller(mock_product_repo)

        # Act
        product = controller.get_product_by_id(1)

        # Assert
        assert product == mock_product
        mock_product_repo.get_by_id.assert_called_once_with(1)

    def test_get_all_products(self):
        # Arrange
        mock_product_repo = MagicMock(spec=ProductRepository)
        mock_products = [
            Product(
                name="Product 1", category="Category 1", price=10.99, stock_quantity=100
            ),
            Product(
                name="Product 2", category="Category 2", price=20.99, stock_quantity=200
            ),
        ]
        mock_product_repo.get_all.return_value = mock_products
        controller = Controller(mock_product_repo)

        # Act
        products = controller.get_all_products()

        # Assert
        assert products == mock_products
        mock_product_repo.get_all.assert_called_once()

    def test_add_to_cart_product_exists(self):
        # Arrange
        mock_product_repo = MagicMock(spec=ProductRepository)
        mock_product = Product(
            name="Test Product",
            category="Test Category",
            price=10.99,
            stock_quantity=100,
        )
        mock_product_repo.get_by_id.return_value = mock_product
        controller = Controller(mock_product_repo)

        # Act
        result = controller.add_to_cart(1, 2)

        # Assert
        assert result is True
        assert len(controller._cart_items) == 1
        assert controller._cart_items[0].product_id == 1
        assert controller._cart_items[0].product_name == "Test Product"
        assert controller._cart_items[0].quantity == 2
        assert controller._cart_items[0].unit_price == 10.99
        mock_product_repo.get_by_id.assert_called_once_with(1)

    def test_add_to_cart_product_not_exists(self):
        # Arrange
        mock_product_repo = MagicMock(spec=ProductRepository)
        mock_product_repo.get_by_id.return_value = None
        controller = Controller(mock_product_repo)

        # Act
        result = controller.add_to_cart(1, 2)

        # Assert
        assert result is False
        assert len(controller._cart_items) == 0
        mock_product_repo.get_by_id.assert_called_once_with(1)

    def test_get_cart_items(self):
        # Arrange
        mock_product_repo = MagicMock(spec=ProductRepository)
        controller = Controller(mock_product_repo)
        cart_item = CartItem(
            product_id=1, product_name="Test Product", quantity=2, unit_price=10.99
        )
        controller._cart_items = [cart_item]

        # Act
        cart_items = controller.get_cart_items()

        # Assert
        assert cart_items == [cart_item]

    def test_process_purchase_empty_cart(self):
        # Arrange
        mock_product_repo = MagicMock(spec=ProductRepository)
        mock_sale_repo = MagicMock(spec=SaleRepository)
        controller = Controller(mock_product_repo, mock_sale_repo)
        controller._cart_items = []

        # Act
        result = controller.process_purchase()

        # Assert
        assert result is None
        mock_sale_repo.add.assert_not_called()

    def test_process_purchase_no_sale_repo(self):
        # Arrange
        mock_product_repo = MagicMock(spec=ProductRepository)
        controller = Controller(mock_product_repo)
        cart_item = CartItem(
            product_id=1, product_name="Test Product", quantity=2, unit_price=10.99
        )
        controller._cart_items = [cart_item]

        # Act
        result = controller.process_purchase()

        # Assert
        assert result is None

    @patch("src.controller.controller.datetime")
    def test_process_purchase_with_items(self, mock_datetime):
        # Arrange
        mock_now = datetime(2025, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = mock_now

        mock_product_repo = MagicMock(spec=ProductRepository)
        mock_sale_repo = MagicMock(spec=SaleRepository)
        controller = Controller(mock_product_repo, mock_sale_repo)

        # Create cart items
        cart_item = CartItem(
            product_id=1, product_name="Test Product", quantity=2, unit_price=10.99
        )
        controller._cart_items = [cart_item]

        # Mock product retrieval
        mock_product = MagicMock(spec=Product)
        mock_product_repo.get_by_id.return_value = mock_product

        # Act
        result = controller.process_purchase()

        # Assert
        assert result is not None
        assert isinstance(result, Sale)
        assert result.sale_date == mock_now
        assert result.total_amount == 21.98  # 2 * 10.99
        mock_sale_repo.add.assert_called_once()
        mock_product_repo.get_by_id.assert_called_once_with(1)
        assert controller._cart_items == []  # Cart should be cleared

    def test_process_return(self):
        # Arrange
        mock_product_repo = MagicMock(spec=ProductRepository)
        mock_sale_repo = MagicMock(spec=SaleRepository)
        mock_return_repo = MagicMock(spec=ReturnRepository)
        mock_sale = MagicMock(spec=Sale)
        mock_sale_repo.get_by_id.return_value = mock_sale

        controller = Controller(mock_product_repo, mock_sale_repo, mock_return_repo)

        product_returns = [{"product_id": 1, "quantity": 1, "reason": "Defective"}]

        mock_product = MagicMock(spec=Product)
        mock_product_repo.get_by_id.return_value = mock_product

        # Act
        result = controller.process_return(1, product_returns)

        # Assert
        assert result is not None
        assert isinstance(result, Return)
        mock_return_repo.add.assert_called()
        mock_product_repo.get_by_id.assert_called_with(1)
        mock_sale_repo.get_by_id.assert_called_with(1)

    def test_process_return_no_repo(self):
        # Arrange
        mock_product_repo = MagicMock(spec=ProductRepository)
        controller = Controller(mock_product_repo)

        product_returns = [{"product_id": 1, "quantity": 1, "reason": "Defective"}]

        # Act
        result = controller.process_return(1, product_returns)

        # Assert
        assert result is None
