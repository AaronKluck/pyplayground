from pyplay.api.db.models import Book
from pyplay.api.db.helpers import async_session
from pyplay.api.models.books import BookCreate, BookRead
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import Tuple
from .exceptions import NotFoundError, ConflictError


async def create_book(book_create: BookCreate) -> Tuple[BookRead, bool]:
    async with async_session() as session:
        try:
            book = Book(title=book_create.title, author_id=book_create.author_id)
            session.add(book)
            await session.commit()
            await session.refresh(book)
            return BookRead.model_validate(book), True  # New resource created
        except IntegrityError:
            await session.rollback()
            # Try to find existing book with same author_id and title
            result = await session.execute(
                select(Book).where(
                    Book.author_id == book_create.author_id,
                    Book.title == book_create.title,
                )
            )
            existing_book = result.scalar_one_or_none()
            if existing_book:
                return (
                    BookRead.model_validate(existing_book),
                    False,
                )  # Existing resource found
            raise  # Re-raise if it's not a unique constraint violation


async def list_books() -> list[BookRead]:
    async with async_session() as session:
        result = await session.execute(select(Book))
        books = result.scalars().all()
        return [BookRead.model_validate(b) for b in books]


async def get_book(book_id: int) -> BookRead | None:
    async with async_session() as session:
        result = await session.execute(select(Book).where(Book.id == book_id))
        book = result.scalar_one_or_none()
        if book is None:
            return None
        return BookRead.model_validate(book)


async def update_book(book_id: int, book_create: BookCreate) -> BookRead:
    async with async_session() as session:
        result = await session.execute(select(Book).where(Book.id == book_id))
        book = result.scalar_one_or_none()
        if book is None:
            raise NotFoundError(f"Book with id {book_id} not found")

        # Check if the new title would conflict with another book by the same author
        if book.title != book_create.title or book.author_id != book_create.author_id:
            conflict_result = await session.execute(
                select(Book).where(
                    Book.author_id == book_create.author_id,
                    Book.title == book_create.title,
                    Book.id != book_id,
                )
            )
            if conflict_result.scalar_one_or_none():
                raise ConflictError(
                    f"Book with title '{book_create.title}' already exists for author {book_create.author_id}"
                )

        try:
            book.title = book_create.title
            book.author_id = book_create.author_id
            await session.commit()
            await session.refresh(book)
            return BookRead.model_validate(book)
        except IntegrityError:
            await session.rollback()
            raise ConflictError(
                f"Book with title '{book_create.title}' already exists for author {book_create.author_id}"
            )


async def delete_book(book_id: int) -> bool:
    async with async_session() as session:
        result = await session.execute(select(Book).where(Book.id == book_id))
        book = result.scalar_one_or_none()
        if book is None:
            return False
        await session.delete(book)
        await session.commit()
        return True
