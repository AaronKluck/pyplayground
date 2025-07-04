from pyplay.api.db.models import Author
from pyplay.api.db.helpers import async_session
from pyplay.api.models.authors import AuthorCreate, AuthorRead
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import Tuple
from .exceptions import NotFoundError, ConflictError


async def create_author(author_create: AuthorCreate) -> Tuple[AuthorRead, bool]:
    async with async_session() as session:
        try:
            author = Author(name=author_create.name)
            session.add(author)
            await session.commit()
            await session.refresh(author)
            return AuthorRead.model_validate(author), True  # New resource created
        except IntegrityError:
            await session.rollback()
            # Try to find existing author with same name
            result = await session.execute(
                select(Author).where(Author.name == author_create.name)
            )
            existing_author = result.scalar_one_or_none()
            if existing_author:
                return (
                    AuthorRead.model_validate(existing_author),
                    False,
                )  # Existing resource found
            raise  # Re-raise if it's not a unique constraint violation


async def list_authors() -> list[AuthorRead]:
    async with async_session() as session:
        result = await session.execute(select(Author))
        authors = result.scalars().all()
        return [AuthorRead.model_validate(a) for a in authors]


async def get_author(author_id: int) -> AuthorRead | None:
    async with async_session() as session:
        result = await session.execute(select(Author).where(Author.id == author_id))
        author = result.scalar_one_or_none()
        if author is None:
            return None
        return AuthorRead.model_validate(author)


async def update_author(author_id: int, author_create: AuthorCreate) -> AuthorRead:
    async with async_session() as session:
        result = await session.execute(select(Author).where(Author.id == author_id))
        author = result.scalar_one_or_none()
        if author is None:
            raise NotFoundError(f"Author with id {author_id} not found")

        # Check if the new name would conflict with another author
        if author.name != author_create.name:
            conflict_result = await session.execute(
                select(Author).where(
                    Author.name == author_create.name, Author.id != author_id
                )
            )
            if conflict_result.scalar_one_or_none():
                raise ConflictError(
                    f"Author with name '{author_create.name}' already exists"
                )

        try:
            author.name = author_create.name
            await session.commit()
            await session.refresh(author)
            return AuthorRead.model_validate(author)
        except IntegrityError:
            await session.rollback()
            raise ConflictError(
                f"Author with name '{author_create.name}' already exists"
            )


async def delete_author(author_id: int) -> bool:
    async with async_session() as session:
        result = await session.execute(select(Author).where(Author.id == author_id))
        author = result.scalar_one_or_none()
        if author is None:
            return False
        await session.delete(author)
        await session.commit()
        return True
