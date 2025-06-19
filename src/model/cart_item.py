class CartItem:
    """
    Represents an item in a shopping cart.
    Attributes:
        product_id (int): Unique identifier for the product.
        product_name (str): Name of the product.
        quantity (int): Number of units of the product in the cart.
        unit_price (float): Price per unit of the product.
    Methods:
        get_total_price() -> float:
            Calculates and returns the total price for this cart item (quantity * unit_price).
    """

    def __init__(
        self, product_id: int, product_name: str, quantity: int, unit_price: float
    ):
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.unit_price = unit_price

    def get_total_price(self) -> float:
        return self.quantity * self.unit_price

    def __repr__(self) -> str:
        return f"<CartItem(product_id={self.product_id}, product_name={self.product_name}, quantity={self.quantity}, unit_price={self.unit_price})>"
