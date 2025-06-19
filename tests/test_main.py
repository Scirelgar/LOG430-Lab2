import pytest
from unittest.mock import MagicMock, patch
from src.main import Menu


class TestMenu:
    def test_init(self):
        # Arrange
        mock_controller = MagicMock()

        # Act
        menu = Menu(mock_controller)

        # Assert
        assert menu.controller == mock_controller
        assert menu.current_menu == "main"
        assert menu.running is True
        assert menu.current_sale_id is None

    def test_change_menu(self):
        # Arrange
        mock_controller = MagicMock()
        menu = Menu(mock_controller)

        # Act
        menu.change_menu("products")

        # Assert
        assert menu.current_menu == "products"

    def test_exit(self):
        # Arrange
        mock_controller = MagicMock()
        menu = Menu(mock_controller)

        # Act
        menu.exit()

        # Assert
        assert menu.running is False


@patch("src.main.create_engine")
@patch("src.main.sessionmaker")
@patch("src.main.Menu")
def test_main_function(mock_menu_class, mock_sessionmaker, mock_create_engine):
    # Arrange
    mock_engine = MagicMock()
    mock_session_factory = MagicMock()
    mock_session = MagicMock()
    mock_menu = MagicMock()

    mock_create_engine.return_value = mock_engine
    mock_sessionmaker.return_value = mock_session_factory
    mock_session_factory.return_value = mock_session
    mock_menu_class.return_value = mock_menu

    # We need to import main here to avoid circular imports
    from src.main import main

    with patch("src.main.Base"):
        with patch("src.main.ProductRepository"):
            with patch("src.main.SaleRepository"):
                with patch("src.main.ReturnRepository"):
                    with patch("src.main.Controller"):
                        # Act
                        main()

    # Assert
    mock_create_engine.assert_called_once()
    mock_session_factory.assert_called_once()
    mock_menu_class.assert_called_once()
    mock_menu.run.assert_called_once()
