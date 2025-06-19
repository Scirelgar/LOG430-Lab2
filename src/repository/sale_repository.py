from collections.abc import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session
from .repository import Registry
from src.model.sale_model import Sale, SaleLine


class SaleRepository(Registry):
    def __init__(self, session: Session):
        self.session = session

    def add(self, sale: Sale) -> None:
        self.session.add(sale)
        self.session.commit()

    def get_by_id(self, sale_id: int) -> Sale | None:
        stmt = select(Sale).where(Sale.id == sale_id)
        return self.session.execute(stmt).scalar_one_or_none()

    def get_all(self) -> Sequence[Sale]:
        stmt = select(Sale)
        return self.session.execute(stmt).scalars().all()

    def add_sale_line(self, sale_line: SaleLine) -> None:
        self.session.add(sale_line)
        self.session.commit()
