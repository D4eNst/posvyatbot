from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from repository.models.base import Base


class Station(Base):
    __tablename__ = "stations"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(String)
    group: Mapped[str] = mapped_column(String(length=8), nullable=True)
    code: Mapped[str] = mapped_column(String)
