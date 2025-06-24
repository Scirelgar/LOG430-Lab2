"""
Application console multi-caisses pour le système de point de vente.
Support de 3 caisses simultanées avec gestion des sessions.
"""

import sys
import os
import threading
import argparse

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.model.declarative_base import Base
from src.model.product import Product
from src.model.sale_model import Sale, SaleLine
from src.model.return_model import Return, ReturnLine
from src.repository.product_repository import ProductRepository
from src.repository.sale_repository import SaleRepository
from src.repository.return_repository import ReturnRepository
from src.controller.controller import Controller
from src.session_manager import session_manager


def run_cashier_terminal(cashier_id: int, db_engine):
    """Lance un terminal de caisse pour un caissier spécifique"""

    # Créer une session de caisse
    cashier_name = f"Caissier-{cashier_id}"
    session = session_manager.create_session(cashier_id, cashier_name)

    # Créer une session de base de données séparée pour ce thread
    Session = sessionmaker(bind=db_engine, future=True)
    db_session = Session()

    # Initialiser les repositories
    product_repo = ProductRepository(db_session)
    sale_repo = SaleRepository(db_session)
    return_repo = ReturnRepository(db_session)

    # Initialiser le contrôleur avec l'ID de caisse
    controller = Controller(product_repo, sale_repo, return_repo, cashier_id=cashier_id)

    print(f"\n🏪 === CAISSE {cashier_id} DÉMARRÉE ===")
    print(f"Caissier: {cashier_name}")
    print(f"Session ID: {session.session_id}")

    try:
        # Simple menu en boucle pour cette caisse
        while True:
            print(f"\n--- CAISSE {cashier_id} ---")
            print("1. Ajouter produit au panier")
            print("2. Voir panier")
            print("3. Finaliser vente")
            print("4. Lister produits")
            print("5. Traiter retour")
            print("0. Fermer caisse")

            choice = input("Choix: ").strip()

            if choice == "1":
                add_to_cart(controller)
            elif choice == "2":
                show_cart(controller)
            elif choice == "3":
                process_sale(controller, cashier_id)
            elif choice == "4":
                list_products(controller)
            elif choice == "5":
                process_return(controller)
            elif choice == "0":
                break
            else:
                print("❌ Choix invalide")

    except KeyboardInterrupt:
        print(f"\n⏹️  Interruption caisse {cashier_id}")
    finally:
        # Fermer la session
        session_manager.close_session(cashier_id)
        db_session.close()
        print(f"🔒 Caisse {cashier_id} fermée")


def add_to_cart(controller: Controller):
    """Ajouter un produit au panier"""
    try:
        product_id = int(input("ID produit: "))
        quantity = int(input("Quantité: "))

        if controller.add_to_cart(product_id, quantity):
            print(f"✅ Produit {product_id} ajouté au panier")
        else:
            print("❌ Produit non trouvé")
    except ValueError:
        print("❌ Valeurs invalides")


def show_cart(controller: Controller):
    """Afficher le contenu du panier"""
    cart_items = controller.get_cart_items()
    if not cart_items:
        print("🛒 Panier vide")
        return

    print("\n🛒 Contenu du panier:")
    total = 0
    for item in cart_items:
        line_total = item.quantity * item.unit_price
        total += line_total
        print(
            f"- {item.quantity}x {item.product_name} @ {item.unit_price}$ = {line_total}$"
        )
    print(f"💰 Total: {total}$")


def process_sale(controller: Controller, cashier_id: int):
    """Finaliser une vente"""
    cart_items = controller.get_cart_items()
    if not cart_items:
        print("❌ Panier vide")
        return

    show_cart(controller)
    confirm = input("Confirmer la vente? (o/n): ").lower()

    if confirm == "o":
        sale = controller.process_purchase()
        if sale:
            print(f"✅ Vente finalisée!")
            print(f"   ID: {sale.id}")
            print(f"   Total: {sale.total_amount}$")
            print(f"   Caisse: {cashier_id}")
        else:
            print("❌ Erreur lors de la vente")
    else:
        print("❌ Vente annulée")


def list_products(controller: Controller):
    """Lister tous les produits"""
    products = controller.get_all_products()
    if not products:
        print("📦 Aucun produit en stock")
        return

    print("\n📦 Produits disponibles:")
    for product in products:
        print(
            f"- ID:{product.id} | {product.name} | {product.price}$ | Stock:{product.stock_quantity}"
        )


def process_return(controller: Controller):
    """Traiter un retour"""
    try:
        sale_id = input("ID de la vente (optionnel): ").strip()
        sale_id = int(sale_id) if sale_id else None

        product_id = int(input("ID produit à retourner: "))
        quantity = int(input("Quantité: "))
        reason = input("Raison (optionnel): ").strip() or None

        product_returns = [
            {"product_id": product_id, "quantity": quantity, "reason": reason}
        ]

        return_obj = controller.process_return(sale_id, product_returns)
        if return_obj:
            print(f"✅ Retour traité! ID: {return_obj.id}")
        else:
            print("❌ Erreur lors du retour")

    except ValueError:
        print("❌ Valeurs invalides")


def main():
    """Point d'entrée principal - lance les 3 caisses"""

    # Parser les arguments de ligne de commande
    parser = argparse.ArgumentParser(description="Système de caisse multi-terminaux")
    parser.add_argument(
        "--cashier-id",
        type=int,
        choices=[1, 2, 3],
        help="ID de caisse spécifique (1, 2, ou 3)",
    )
    parser.add_argument(
        "--demo", action="store_true", help="Mode démo avec données de test"
    )

    args = parser.parse_args()  # Initialisation de la base de données
    # Utiliser la variable d'environnement pour l'hôte de la DB (Docker vs local)
    db_host = os.environ.get("DB_HOST", "localhost")
    engine = create_engine(
        f"postgresql+psycopg2://postgres:admin@{db_host}:5432/shopdb",
        future=True,
        echo=False,  # Moins de logs pour les 3 caisses
    )  # Créer les tables si elles n'existent pas (gestion de la concurrence)
    try:
        Base.metadata.create_all(engine, checkfirst=True)
    except Exception as e:
        # En cas de concurrence, une autre caisse a peut-être déjà créé les tables
        if "already exists" in str(e):
            print(f"ℹ️  Les tables existent déjà (créées par une autre caisse)")
        else:
            print(f"⚠️  Erreur lors de la création des tables: {e}")
            raise e

    # Mode caisse unique (pour Docker ou tests)
    if args.cashier_id:
        print(f"🏪 Démarrage en mode caisse unique: {args.cashier_id}")
        run_cashier_terminal(args.cashier_id, engine)
        return

    # Mode multi-caisses (3 caisses simultanées)
    print("🏪 === SYSTÈME MULTI-CAISSES ===")
    print("Démarrage de 3 caisses simultanées...")

    # Créer 3 threads pour les 3 caisses
    threads = []
    for cashier_id in [1, 2, 3]:
        thread = threading.Thread(
            target=run_cashier_terminal,
            args=(cashier_id, engine),
            name=f"Caisse-{cashier_id}",
        )
        threads.append(thread)
        thread.start()

    try:
        # Attendre que tous les threads se terminent
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("\n⏹️  Arrêt du système multi-caisses")

    print("🔒 Système fermé")


if __name__ == "__main__":
    main()
