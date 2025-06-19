import os
import sys
import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

# Ensure the project root is in Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.model.product import Product
from src.model.sale_model import Sale, SaleLine
from src.model.return_model import Return, ReturnLine
from src.repository.product_repository import ProductRepository
from src.repository.sale_repository import SaleRepository
from src.repository.return_repository import ReturnRepository
from src.controller.controller import Controller


@pytest.fixture
def mock_session():
    """Creates a mock SQLAlchemy session"""
    return MagicMock(spec=Session)


@pytest.fixture
def product_repository(mock_session):
    """Creates a ProductRepository with a mock session"""
    return ProductRepository(mock_session)


@pytest.fixture
def sale_repository(mock_session):
    """Creates a SaleRepository with a mock session"""
    return SaleRepository(mock_session)


@pytest.fixture
def return_repository(mock_session):
    """Creates a ReturnRepository with a mock session"""
    return ReturnRepository(mock_session)


@pytest.fixture
def controller(product_repository, sale_repository, return_repository):
    """Creates a Controller with mock repositories"""
    return Controller(product_repository, sale_repository, return_repository)


@pytest.fixture
def sample_product():
    """Creates a sample product for testing"""
    return Product(
        name="Test Product", category="Test Category", price=10.99, stock_quantity=100
    )


@pytest.fixture
def sample_sale():
    """Creates a sample sale for testing"""
    return Sale(total_amount=99.99)


@pytest.fixture
def sample_return():
    """Creates a sample return for testing"""
    return Return(original_sale_id=1, total_amount=49.99)
