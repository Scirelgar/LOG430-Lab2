import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from src.repository.product_repository import ProductRepository
from src.model.product import Product


class TestProductRepository:
    def test_init(self):
        # Arrange
        mock_session = MagicMock(spec=Session)

        # Act
        repo = ProductRepository(mock_session)

        # Assert
        assert repo.session == mock_session

    def test_add(self):
        # Arrange
        mock_session = MagicMock(spec=Session)
        product = Product(
            name="Test Product",
            category="Test Category",
            price=10.99,
            stock_quantity=100,
        )
        repo = ProductRepository(mock_session)

        # Act
        repo.add(product)

        # Assert
        mock_session.add.assert_called_once_with(product)
        mock_session.commit.assert_called_once()

    def test_get_by_id(self):
        # Arrange
        mock_session = MagicMock(spec=Session)
        mock_query_result = MagicMock()
        mock_session.execute.return_value = mock_query_result
        mock_query_result.scalar_one_or_none.return_value = Product(
            name="Test Product",
            category="Test Category",
            price=10.99,
            stock_quantity=100,
        )

        repo = ProductRepository(mock_session)

        # Act
        product = repo.get_by_id(1)

        # Assert
        assert product is not None
        assert product.name == "Test Product"
        assert product.category == "Test Category"
        assert product.price == 10.99
        assert product.stock_quantity == 100
        mock_session.execute.assert_called_once()
        mock_query_result.scalar_one_or_none.assert_called_once()

    def test_get_all(self):
        # Arrange
        mock_session = MagicMock(spec=Session)
        mock_query_result = MagicMock()
        mock_session.execute.return_value = mock_query_result
        mock_products = [
            Product(
                name="Product 1", category="Category 1", price=10.99, stock_quantity=100
            ),
            Product(
                name="Product 2", category="Category 2", price=20.99, stock_quantity=200
            ),
        ]
        mock_query_result.scalars.return_value.all.return_value = mock_products

        repo = ProductRepository(mock_session)

        # Act
        products = repo.get_all()

        # Assert
        assert products == mock_products
        assert len(products) == 2
        mock_session.execute.assert_called_once()
        mock_query_result.scalars.assert_called_once()
        mock_query_result.scalars.return_value.all.assert_called_once()
