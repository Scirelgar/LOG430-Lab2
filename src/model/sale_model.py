from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Float, ForeignKey, DateTime
from datetime import datetime
from src.model.declarative_base import Base
from src.model.product import Product


class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(primary_key=True)
    sale_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    total_amount: Mapped[float] = mapped_column(Float, default=0.0)

    sale_lines: Mapped[list["SaleLine"]] = relationship(
        "SaleLine", back_populates="sale", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Sale(id={self.id}, date={self.sale_date}, total_amount={self.total_amount})>"


class SaleLine(Base):
    __tablename__ = "sale_lines"

    id: Mapped[int] = mapped_column(primary_key=True)
    sale_id: Mapped[int] = mapped_column(ForeignKey("sales.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)

    sale: Mapped["Sale"] = relationship("Sale", back_populates="sale_lines")
    product = relationship("Product")

    def __repr__(self) -> str:
        return f"<SaleLine(product_id={self.product_id}, quantity={self.quantity}, unit_price={self.unit_price})>"
