from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Float, ForeignKey, DateTime, String
from datetime import datetime
from src.model.declarative_base import Base
from src.model.product import Product
from src.model.sale_model import Sale


class Return(Base):
    __tablename__ = "returns"

    id: Mapped[int] = mapped_column(primary_key=True)
    return_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    original_sale_id: Mapped[int | None] = mapped_column(
        ForeignKey("sales.id"), nullable=True
    )
    total_amount: Mapped[float] = mapped_column(Float, default=0.0)

    return_lines: Mapped[list["ReturnLine"]] = relationship(
        "ReturnLine", back_populates="return_", cascade="all, delete-orphan"
    )
    original_sale = relationship("Sale")

    def __repr__(self) -> str:
        return f"<Return(id={self.id}, date={self.return_date}, total_amount={self.total_amount})>"


class ReturnLine(Base):
    __tablename__ = "return_lines"

    id: Mapped[int] = mapped_column(primary_key=True)
    return_id: Mapped[int] = mapped_column(ForeignKey("returns.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)
    reason: Mapped[str | None] = mapped_column(String(255), nullable=True)

    return_: Mapped["Return"] = relationship("Return", back_populates="return_lines")
    product = relationship("Product")

    def __repr__(self) -> str:
        return f"<ReturnLine(product_id={self.product_id}, quantity={self.quantity}, unit_price={self.unit_price})>"
