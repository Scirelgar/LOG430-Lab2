import sys
import os

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


class Menu:
    def __init__(self, controller: Controller):
        self.controller = controller
        self.current_menu = "main"
        self.running = True
        self.current_sale_id = None  # For returns

        self.menus = {
            "main": {
                "display": self.display_main_menu,
                "options": {
                    "1": lambda: self.change_menu("products"),
                    "2": lambda: self.change_menu("transactions"),
                    "0": self.exit,
                },
            },
            "products": {
                "display": self.display_products_menu,
                "options": {
                    "1": self.add_product,
                    "2": self.get_product_by_id,
                    "3": self.list_all_products,
                    "0": lambda: self.change_menu("main"),
                },
            },
            "transactions": {
                "display": self.display_transactions_menu,
                "options": {
                    "1": lambda: self.change_menu("start_purchase"),
                    "2": lambda: self.change_menu("start_return"),
                    "0": lambda: self.change_menu("main"),
                },
            },
            "start_purchase": {
                "display": self.display_start_purchase,
                "options": {
                    "1": self.add_product_to_cart,
                    "2": self.process_purchase,
                    "0": lambda: self.change_menu("transactions"),
                },
            },
            "start_return": {
                "display": self.display_start_return,
                "options": {
                    "1": self.process_return,
                    "0": lambda: self.change_menu("transactions"),
                },
            },
        }

    def change_menu(self, menu_name):
        self.current_menu = menu_name

    def display_main_menu(self):
        print("\n===== Menu Principal =====")
        print("1. Produits")
        print("2. Transactions")
        print("0. Quitter")
        print("========================")

    def display_products_menu(self):
        print("\n===== Menu Produits =====")
        print("1. Ajouter un nouveau produit")
        print("2. Rechercher un produit par id")
        print("3. Lister tous les produits")
        print("0. Menu principal")
        print("========================")

    def display_transactions_menu(self):
        print("\n===== Menu Transactions =====")
        print("1. Achats")
        print("2. Retours")
        print("0. Menu principal")
        print("===========================")

    def display_start_purchase(self):
        print("\n===== Démarrer un achat =====")
        print("1. Ajouter un produit au panier")
        print("2. Finaliser l'achat")
        print("0. Annuler et retourner au menu des transactions")
        print("=============================")

    def display_start_return(self):
        print("\n===== Démarrer un retour =====")
        print("1. Retourner un produit")
        print("0. Annuler et retourner au menu des transactions")
        print("=============================")

    def run(self):
        while self.running:
            current = self.menus[self.current_menu]
            current["display"]()

            choice = input("Choisissez une option: ")
            action = current["options"].get(choice)

            if action:
                action()
            else:
                print("Option invalide. Veuillez réessayer.")

    def add_product(self):
        name = input("Nom du produit: ")
        category = input("Catégorie: ")
        try:
            price = float(input("Prix: "))
            stock = int(input("Quantité en stock: "))

            prod = self.controller.add_product(name, category, price, stock)
            print(f"Produit '{name}' ajouté avec succès! ID: {prod.id}")
        except ValueError:
            print("Erreur: Prix ou quantité en stock invalide.")

    def get_product_by_id(self):
        try:
            product_id = int(input("Entrez l'ID du produit: "))
            product = self.controller.get_product_by_id(product_id)
            if product:
                print(f"Produit trouvé: {product}")
            else:
                print(f"Aucun produit trouvé avec l'ID {product_id}")
        except ValueError:
            print("Veuillez entrer un ID valide (nombre entier)")

    def list_all_products(self):
        products = self.controller.get_all_products()
        if products:
            print("\nListe de tous les produits:")
            for product in products:
                print(f"- {product}")
        else:
            print("Aucun produit dans la base de données.")

    def add_product_to_cart(self):
        try:
            # Récupérer les informations du produit
            product_id = int(input("ID du produit à ajouter: "))
            quantity = int(input("Quantité: "))

            # Vérifier que le produit existe
            product = self.controller.get_product_by_id(product_id)
            if not product:
                print(f"Aucun produit trouvé avec l'ID {product_id}")
                return

            # Vérifier que la quantité est disponible
            if product.stock_quantity < quantity:
                print(f"Stock insuffisant. Disponible: {product.stock_quantity}")
                return

            # Ajouter le produit au panier (via le controller)
            self.controller.add_to_cart(product_id, quantity)

            # Confirmer l'ajout
            print(f"{quantity} x {product.name} ajouté au panier.")

            # Afficher le contenu actuel du panier
            cart_items = self.controller.get_cart_items()
            if cart_items:
                print("\nContenu du panier:")
                total = 0
                for item in cart_items:
                    line_total = item.quantity * item.unit_price
                    total += line_total
                    print(
                        f"- {item.quantity} x {item.product_name} ({item.unit_price} $) = {line_total} $"
                    )
                print(f"Total: {total} $")

        except ValueError:
            print("Erreur: Veuillez entrer des valeurs numériques valides")

    def process_purchase(self):
        # Vérifier si le panier contient des items
        cart_items = self.controller.get_cart_items()

        if not cart_items or len(cart_items) == 0:
            print("Le panier est vide. Impossible de finaliser l'achat.")
            return

        # Afficher un résumé de la commande
        print("\n===== Résumé de la commande =====")
        total = 0
        for item in cart_items:
            line_total = item.quantity * item.unit_price
            total += line_total
            print(
                f"- {item.quantity} x {item.product_name} ({item.unit_price} $) = {line_total} $"
            )
        print(f"Total: {total} $")

        # Demander confirmation
        confirm = input("\nConfirmer l'achat? (o/n): ").lower()

        if confirm == "o":
            # Traiter l'achat via le controller
            sale = self.controller.process_purchase()

            if sale:
                # Store the sale ID for potential returns
                self.current_sale_id = sale.id

                # Afficher confirmation
                print(f"\nAchat finalisé avec succès!")
                print(f"Numéro de transaction: {sale.id}")
                print(f"Montant total: {sale.total_amount} $")
                print(f"Date: {sale.sale_date}")
            else:
                print("Erreur lors de la finalisation de l'achat.")
        else:
            print("Achat annulé.")

    def process_return(self):
        try:
            # Get the sale ID for the return
            sale_id = int(
                input("Entrez l'ID de la vente à retourner (laissez vide si inconnu): ")
                or "0"
            )
            if sale_id == 0:
                sale_id = None

            # Get products to return
            product_returns = []
            while True:
                try:
                    product_id = int(
                        input("ID du produit à retourner (0 pour terminer): ")
                    )
                    if product_id == 0:
                        break

                    quantity = int(input("Quantité à retourner: "))
                    reason = input("Raison du retour (optionnel): ")

                    # Verify product exists
                    product = self.controller.get_product_by_id(product_id)
                    if not product:
                        print(f"Produit {product_id} non trouvé, veuillez réessayer.")
                        continue

                    product_returns.append(
                        {
                            "product_id": product_id,
                            "quantity": quantity,
                            "reason": reason,
                        }
                    )

                    print(f"Produit {product_id} ajouté au retour.")

                except ValueError:
                    print("Veuillez entrer des valeurs numériques valides.")

            if not product_returns:
                print("Aucun produit sélectionné pour le retour.")
                return

            # Process the return
            return_obj = self.controller.process_return(sale_id, product_returns)

            if return_obj:
                print(f"\nRetour traité avec succès!")
                print(f"ID du retour: {return_obj.id}")
                print(f"Montant total remboursé: {return_obj.total_amount} $")
                print(f"Date: {return_obj.return_date}")
            else:
                print("Erreur lors du traitement du retour.")

        except ValueError:
            print("Veuillez entrer des valeurs numériques valides.")

    def exit(self):
        print("Système en fermeture...")
        self.running = False


def main():
    # Initialize database connection
    engine = create_engine(
        "postgresql+psycopg2://postgres:admin@localhost:5432/shopdb",
        future=True,
        echo=True,
    )

    # Create tables if they don't exist
    Base.metadata.create_all(engine)

    # Create session
    Session = sessionmaker(bind=engine, future=True)
    session = Session()

    # Initialize repositories
    product_repo = ProductRepository(session)
    sale_repo = SaleRepository(session)
    return_repo = ReturnRepository(session)

    # Initialize controller with all repositories
    controller = Controller(product_repo, sale_repo, return_repo)

    # Run the menu
    menu = Menu(controller)
    menu.run()


if __name__ == "__main__":
    main()
