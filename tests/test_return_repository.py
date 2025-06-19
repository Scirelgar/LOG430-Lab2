import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from src.repository.return_repository import ReturnRepository
from src.model.return_model import Return, ReturnLine
from datetime import datetime


class TestReturnRepository:
    def test_init(self):
        # Arrange
        mock_session = MagicMock(spec=Session)

        # Act
        repo = ReturnRepository(mock_session)

        # Assert
        assert repo.session == mock_session

    def test_add(self):
        # Arrange
        mock_session = MagicMock(spec=Session)
        return_obj = Return(
            return_date=datetime.now(), original_sale_id=1, total_amount=49.99
        )
        repo = ReturnRepository(mock_session)

        # Act
        repo.add(return_obj)

        # Assert
        mock_session.add.assert_called_once_with(return_obj)
        mock_session.commit.assert_called_once()

    def test_get_by_id(self):
        # Arrange
        mock_session = MagicMock(spec=Session)
        mock_query_result = MagicMock()
        mock_session.execute.return_value = mock_query_result
        mock_return = Return(
            return_date=datetime.now(), original_sale_id=1, total_amount=49.99
        )
        mock_query_result.scalar_one_or_none.return_value = mock_return

        repo = ReturnRepository(mock_session)

        # Act
        return_obj = repo.get_by_id(1)

        # Assert
        assert return_obj is not None
        assert return_obj.original_sale_id == 1
        assert return_obj.total_amount == 49.99
        mock_session.execute.assert_called_once()
        mock_query_result.scalar_one_or_none.assert_called_once()

    def test_get_all(self):
        # Arrange
        mock_session = MagicMock(spec=Session)
        mock_query_result = MagicMock()
        mock_session.execute.return_value = mock_query_result
        mock_returns = [
            Return(return_date=datetime.now(), original_sale_id=1, total_amount=49.99),
            Return(return_date=datetime.now(), original_sale_id=2, total_amount=29.99),
        ]
        mock_query_result.scalars.return_value.all.return_value = mock_returns

        repo = ReturnRepository(mock_session)

        # Act
        returns = repo.get_all()

        # Assert
        assert returns == mock_returns
        assert len(returns) == 2
        mock_session.execute.assert_called_once()
        mock_query_result.scalars.assert_called_once()
        mock_query_result.scalars.return_value.all.assert_called_once()

    def test_add_return_line(self):
        # Arrange
        mock_session = MagicMock(spec=Session)
        return_line = ReturnLine(
            return_id=1,
            product_id=2,
            quantity=3,
            unit_price=16.99,
            reason="Defective product",
        )
        repo = ReturnRepository(mock_session)

        # Act
        repo.add_return_line(return_line)

        # Assert
        mock_session.add.assert_called_once_with(return_line)
        mock_session.commit.assert_called_once()
