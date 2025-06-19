from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float
from src.model.declarative_base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0)

    def __repr__(self) -> str:
        return (
            f"<Product(id={self.id!r}, name={self.name!r}, "
            f"category={self.category!r}, price={self.price!r}, "
            f"stock_quantity={self.stock_quantity!r})>"
        )
