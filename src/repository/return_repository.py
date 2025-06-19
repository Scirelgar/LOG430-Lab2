from collections.abc import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session
from .repository import Registry
from src.model.return_model import Return, ReturnLine


class ReturnRepository(Registry):
    def __init__(self, session: Session):
        self.session = session

    def add(self, return_: Return) -> None:
        self.session.add(return_)
        self.session.commit()

    def get_by_id(self, return_id: int) -> Return | None:
        stmt = select(Return).where(Return.id == return_id)
        return self.session.execute(stmt).scalar_one_or_none()

    def get_all(self) -> Sequence[Return]:
        stmt = select(Return)
        return self.session.execute(stmt).scalars().all()

    def add_return_line(self, return_line: ReturnLine) -> None:
        self.session.add(return_line)
        self.session.commit()
