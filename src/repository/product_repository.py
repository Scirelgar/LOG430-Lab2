from collections.abc import Sequence
from sqlalchemy import select
from .repository import Registry
from sqlalchemy.orm import Session
from src.model.product import Product


class ProductRepository(Registry):
    def __init__(self, session: Session):
        self.session = session

    def add(self, product: Product) -> None:
        self.session.add(product)
        self.session.commit()

    def get_by_id(self, product_id: int) -> Product | None:
        stmt = select(Product).where(Product.id == product_id)
        result = self.session.execute(stmt).scalar_one_or_none()
        return result

    def get_all(self) -> Sequence[Product]:
        stmt = select(Product)
        return self.session.execute(stmt).scalars().all()
