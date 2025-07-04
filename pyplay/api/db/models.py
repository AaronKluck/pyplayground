from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column,
    DeclarativeBase,
)
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(DeclarativeBase, AsyncAttrs):  # Include AsyncAttrs for convenience
    pass


class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    books: Mapped[list["Book"]] = relationship(
        "Book", back_populates="author", cascade="all, delete-orphan"
    )


class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("authors.id", ondelete="CASCADE"), nullable=False
    )
    author: Mapped[Author] = relationship("Author", back_populates="books")
