import pytest
from datetime import datetime
from src.model.sale_model import Sale, SaleLine


class TestSale:
    def test_init(self):
        # Arrange & Act
        sale_date = datetime.now()
        sale = Sale(sale_date=sale_date, total_amount=99.99)

        # Assert
        assert sale.sale_date == sale_date
        assert sale.total_amount == 99.99
        assert sale.id is None  # ID is assigned by the database
        assert sale.sale_lines == []

    def test_repr(self):
        # Arrange
        sale_date = datetime.now()
        sale = Sale(sale_date=sale_date, total_amount=99.99)

        # Act
        result = repr(sale)

        # Assert
        assert "Sale" in result
        assert str(sale_date) in result
        assert "99.99" in result


class TestSaleLine:
    def test_init(self):
        # Arrange & Act
        sale_line = SaleLine(sale_id=1, product_id=2, quantity=5, unit_price=19.99)

        # Assert
        assert sale_line.sale_id == 1
        assert sale_line.product_id == 2
        assert sale_line.quantity == 5
        assert sale_line.unit_price == 19.99
        assert sale_line.id is None  # ID is assigned by the database

    def test_repr(self):
        # Arrange
        sale_line = SaleLine(product_id=2, quantity=5, unit_price=19.99)

        # Act
        result = repr(sale_line)

        # Assert
        assert "SaleLine" in result
        assert "2" in result
        assert "5" in result
        assert "19.99" in result
