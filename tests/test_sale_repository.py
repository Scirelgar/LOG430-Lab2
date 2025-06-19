import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from src.repository.sale_repository import SaleRepository
from src.model.sale_model import Sale, SaleLine
from datetime import datetime


class TestSaleRepository:
    def test_init(self):
        # Arrange
        mock_session = MagicMock(spec=Session)

        # Act
        repo = SaleRepository(mock_session)

        # Assert
        assert repo.session == mock_session

    def test_add(self):
        # Arrange
        mock_session = MagicMock(spec=Session)
        sale = Sale(sale_date=datetime.now(), total_amount=99.99)
        repo = SaleRepository(mock_session)

        # Act
        repo.add(sale)

        # Assert
        mock_session.add.assert_called_once_with(sale)
        mock_session.commit.assert_called_once()

    def test_get_by_id(self):
        # Arrange
        mock_session = MagicMock(spec=Session)
        mock_query_result = MagicMock()
        mock_session.execute.return_value = mock_query_result
        mock_sale = Sale(sale_date=datetime.now(), total_amount=99.99)
        mock_query_result.scalar_one_or_none.return_value = mock_sale

        repo = SaleRepository(mock_session)

        # Act
        sale = repo.get_by_id(1)

        # Assert
        assert sale is not None
        assert sale.total_amount == 99.99
        mock_session.execute.assert_called_once()
        mock_query_result.scalar_one_or_none.assert_called_once()

    def test_get_all(self):
        # Arrange
        mock_session = MagicMock(spec=Session)
        mock_query_result = MagicMock()
        mock_session.execute.return_value = mock_query_result
        mock_sales = [
            Sale(sale_date=datetime.now(), total_amount=99.99),
            Sale(sale_date=datetime.now(), total_amount=149.99),
        ]
        mock_query_result.scalars.return_value.all.return_value = mock_sales

        repo = SaleRepository(mock_session)

        # Act
        sales = repo.get_all()

        # Assert
        assert sales == mock_sales
        assert len(sales) == 2
        mock_session.execute.assert_called_once()
        mock_query_result.scalars.assert_called_once()
        mock_query_result.scalars.return_value.all.assert_called_once()

    def test_add_sale_line(self):
        # Arrange
        mock_session = MagicMock(spec=Session)
        sale_line = SaleLine(sale_id=1, product_id=2, quantity=5, unit_price=19.99)
        repo = SaleRepository(mock_session)

        # Act
        repo.add_sale_line(sale_line)

        # Assert
        mock_session.add.assert_called_once_with(sale_line)
        mock_session.commit.assert_called_once()
