"""
Test simple pour valider la solution multi-caisses
"""

import unittest
from unittest.mock import MagicMock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.session_manager import SessionManager, CashierSession
from src.controller.controller import Controller
from src.model.sale_model import Sale


class TestMultiCashier(unittest.TestCase):

    def setUp(self):
        self.session_manager = SessionManager()

    def test_session_creation(self):
        """Test de création de session caisse"""
        session = self.session_manager.create_session(1, "Caissier-1")

        self.assertEqual(session.cashier_id, 1)
        self.assertEqual(session.cashier_name, "Caissier-1")
        self.assertIsNotNone(session.session_id)
        self.assertIn(1, self.session_manager.active_sessions)

    def test_multiple_sessions(self):
        """Test de création de multiples sessions"""
        # Créer 3 sessions
        for i in range(1, 4):
            self.session_manager.create_session(i, f"Caissier-{i}")

        # Vérifier qu'elles existent toutes
        active_sessions = self.session_manager.list_active_sessions()
        self.assertEqual(len(active_sessions), 3)

        # Vérifier les IDs
        for i in range(1, 4):
            self.assertIn(i, active_sessions)

    def test_controller_with_cashier_id(self):
        """Test du contrôleur avec ID de caisse"""
        mock_product_repo = MagicMock()
        mock_sale_repo = MagicMock()

        # Créer un contrôleur avec ID de caisse
        controller = Controller(
            product_repository=mock_product_repo,
            sale_repository=mock_sale_repo,
            cashier_id=1,
        )

        self.assertEqual(controller.cashier_id, 1)

    def test_sale_with_cashier_id(self):
        """Test de vente avec ID de caisse"""
        # Créer une vente avec ID de caisse
        sale = Sale(total_amount=50.0, cashier_id=2)

        self.assertEqual(sale.cashier_id, 2)
        self.assertEqual(sale.total_amount, 50.0)

    def test_session_cleanup(self):
        """Test de nettoyage des sessions"""
        # Créer des sessions
        for i in range(1, 4):
            self.session_manager.create_session(i, f"Caissier-{i}")

        # Fermer une session
        closed = self.session_manager.close_session(2)
        self.assertTrue(closed)

        # Vérifier qu'elle n'existe plus
        active_sessions = self.session_manager.list_active_sessions()
        self.assertEqual(len(active_sessions), 2)
        self.assertNotIn(2, active_sessions)


if __name__ == "__main__":
    print("🧪 Test de la solution multi-caisses...")
    unittest.main(verbosity=2)
