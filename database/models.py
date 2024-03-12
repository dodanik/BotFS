from sqlalchemy import Text, String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Post(Base):
    __tablename__ = 'post'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    link: Mapped[str] = mapped_column(Text)
    image: Mapped[str] = mapped_column(String(150), nullable=False)
    type: Mapped[str] = mapped_column(String(150), nullable=False)
    button: Mapped[str] = mapped_column(String(150), nullable=False)


class Users(Base):
    __tablename__ = 'users'

    userid: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    username: Mapped[str] = mapped_column(Text, nullable=True)
    firstname: Mapped[str] = mapped_column(Text, nullable=True)
    lastname: Mapped[str] = mapped_column(Text, nullable=True)
    language: Mapped[str] = mapped_column(String(5), nullable=False)

