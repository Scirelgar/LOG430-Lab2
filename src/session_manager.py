import threading
from typing import Dict, Optional
from datetime import datetime


class CashierSession:
    """Simple session for a cashier"""

    def __init__(self, cashier_id: int, cashier_name: str):
        self.cashier_id = cashier_id
        self.cashier_name = cashier_name
        self.session_start = datetime.now()
        self.session_id = f"cash_{cashier_id}_{self.session_start.strftime('%H%M%S')}"
        self.lock = threading.Lock()  # Pour la sécurité thread

    def __str__(self):
        return f"Caisse {self.cashier_id} - {self.cashier_name}"


class SessionManager:
    """Gestionnaire simple des sessions de caisses multiples"""

    def __init__(self):
        self.active_sessions: Dict[int, CashierSession] = {}
        self.lock = threading.Lock()

    def create_session(self, cashier_id: int, cashier_name: str) -> CashierSession:
        """Créer une nouvelle session de caisse"""
        with self.lock:
            session = CashierSession(cashier_id, cashier_name)
            self.active_sessions[cashier_id] = session
            print(f"✅ Session créée pour {session}")
            return session

    def get_session(self, cashier_id: int) -> Optional[CashierSession]:
        """Récupérer une session existante"""
        with self.lock:
            return self.active_sessions.get(cashier_id)

    def close_session(self, cashier_id: int) -> bool:
        """Fermer une session"""
        with self.lock:
            if cashier_id in self.active_sessions:
                session = self.active_sessions[cashier_id]
                del self.active_sessions[cashier_id]
                print(f"🔒 Session fermée pour {session}")
                return True
            return False

    def list_active_sessions(self) -> Dict[int, CashierSession]:
        """Lister toutes les sessions actives"""
        with self.lock:
            return self.active_sessions.copy()


# Instance globale du gestionnaire de sessions
session_manager = SessionManager()
