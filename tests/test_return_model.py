import pytest
from datetime import datetime
from src.model.return_model import Return, ReturnLine


class TestReturn:
    def test_init(self):
        # Arrange & Act
        return_date = datetime.now()
        return_obj = Return(
            return_date=return_date, original_sale_id=1, total_amount=49.99
        )

        # Assert
        assert return_obj.return_date == return_date
        assert return_obj.original_sale_id == 1
        assert return_obj.total_amount == 49.99
        assert return_obj.id is None  # ID is assigned by the database
        assert return_obj.return_lines == []

    def test_repr(self):
        # Arrange
        return_date = datetime.now()
        return_obj = Return(
            return_date=return_date, original_sale_id=1, total_amount=49.99
        )

        # Act
        result = repr(return_obj)

        # Assert
        assert "Return" in result
        assert str(return_date) in result
        assert "49.99" in result


class TestReturnLine:
    def test_init(self):
        # Arrange & Act
        return_line = ReturnLine(
            return_id=1,
            product_id=2,
            quantity=3,
            unit_price=16.99,
            reason="Defective product",
        )

        # Assert
        assert return_line.return_id == 1
        assert return_line.product_id == 2
        assert return_line.quantity == 3
        assert return_line.unit_price == 16.99
        assert return_line.reason == "Defective product"
        assert return_line.id is None  # ID is assigned by the database

    def test_repr(self):
        # Arrange
        return_line = ReturnLine(
            product_id=2, quantity=3, unit_price=16.99, reason="Defective product"
        )

        # Act
        result = repr(return_line)

        # Assert
        assert "ReturnLine" in result
        assert "2" in result
        assert "3" in result
        assert "16.99" in result
