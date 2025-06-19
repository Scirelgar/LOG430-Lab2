from typing import Optional, List
from src.model.product import Product
from src.model.sale_model import Sale, SaleLine
from src.model.return_model import Return, ReturnLine
from src.repository.product_repository import ProductRepository
from src.repository.sale_repository import SaleRepository
from src.repository.return_repository import ReturnRepository
from src.model.cart_item import CartItem
from datetime import datetime


class Controller:

    def __init__(
        self,
        product_repository: ProductRepository,
        sale_repository: Optional[SaleRepository] = None,
        return_repository: Optional[ReturnRepository] = None,
    ):
        self.product_repository = product_repository
        self.sale_repository = sale_repository
        self.return_repository = return_repository
        self._cart_items: List[CartItem] = []  # Temporary cart for current transaction

    def add_product(self, name, category, price, stock):
        prod = Product(name=name, category=category, price=price, stock_quantity=stock)
        self.product_repository.add(prod)
        return prod

    def get_product_by_id(self, product_id):
        return self.product_repository.get_by_id(product_id)

    def get_all_products(self):
        return self.product_repository.get_all()

    def add_to_cart(self, product_id, quantity):
        """Adds a product to the temporary cart"""
        product = self.get_product_by_id(product_id)
        if not product:
            return False

        # Create a temporary CartItem object instead of SaleLine
        cart_item = CartItem(
            product_id=product_id,
            product_name=product.name,
            quantity=quantity,
            unit_price=product.price,
        )

        self._cart_items.append(cart_item)
        return True

    def get_cart_items(self):
        """Returns the items in the cart"""
        return self._cart_items

    def process_purchase(self):
        """Process the purchase and create a Sale object"""
        if not self._cart_items or not self.sale_repository:
            return None

        # Create a new Sale object
        sale = Sale(
            sale_date=datetime.now(),
            total_amount=sum(
                item.quantity * item.unit_price for item in self._cart_items
            ),
        )

        # Add the sale to the database first to get an ID
        self.sale_repository.add(sale)

        # Create and add SaleLines to the database
        for item in self._cart_items:
            # Get the product to update stock
            product = self.get_product_by_id(item.product_id)
            if product:
                # Create a persistent SaleLine
                db_sale_line = SaleLine(
                    sale_id=sale.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=product.price,
                )

                # Add SaleLine to database
                self.sale_repository.add_sale_line(db_sale_line)

                # Update product stock
                product.stock_quantity -= item.quantity
                self.product_repository.add(product)  # Update the product in database

        # Clear the cart
        self._cart_items = []

        return sale

    def process_return(self, sale_id, product_returns):
        """
        Process a return from a previous sale

        Args:
            sale_id: The ID of the original sale
            product_returns: A list of dictionaries with product_id, quantity, and reason
        """
        if not self.return_repository:
            return None

        # Get the original sale
        original_sale = (
            self.sale_repository.get_by_id(sale_id)
            if (self.sale_repository and sale_id)
            else None
        )

        # Create a new return
        return_obj = Return(
            return_date=datetime.now(),
            original_sale_id=sale_id if original_sale else None,
            # Initialize total_amount to 0.0 when creating the object
            total_amount=0.0,
        )

        # Add the return to the database first to get an ID
        self.return_repository.add(return_obj)

        total_amount = 0.0

        # Process each returned product
        for pr in product_returns:
            product = self.get_product_by_id(pr["product_id"])
            if product:
                # Get unit price from original sale if possible, or use current price
                unit_price = product.price
                quantity = pr["quantity"]

                # Create return line with explicitly passed values
                return_line = ReturnLine(
                    return_id=return_obj.id,
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=unit_price,
                    reason=pr.get("reason", None),
                )

                # Add return line to database
                self.return_repository.add_return_line(return_line)

                # Update product stock
                product.stock_quantity += quantity
                self.product_repository.add(product)

                # Calculate the line total with the actual values, not the Column objects
                line_total = quantity * unit_price
                total_amount += line_total

        # Update the total amount - we need to set it before adding to the repository
        return_obj.total_amount = total_amount
        self.return_repository.add(return_obj)

        return return_obj
