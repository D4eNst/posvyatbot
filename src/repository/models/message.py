from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from repository.models.base import Base


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    slug: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(String)
