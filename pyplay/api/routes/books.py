from fastapi import APIRouter, HTTPException, status
from typing import List
from pyplay.api.models.books import BookCreate, BookRead
from pyplay.api.controllers import books as book_controller
from pyplay.api.controllers.exceptions import NotFoundError, ConflictError


router = APIRouter()


@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate):
    result, is_new = await book_controller.create_book(book)
    if is_new:
        return result
    else:
        # Return existing resource with 200 status
        from fastapi.responses import Response

        return Response(
            content=result.model_dump_json(),
            media_type="application/json",
            status_code=200,
        )


@router.get("/", response_model=List[BookRead])
async def list_books():
    return await book_controller.list_books()


@router.get("/{book_id}", response_model=BookRead)
async def get_book(book_id: int):
    book = await book_controller.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=BookRead)
async def update_book(book_id: int, book: BookCreate):
    try:
        return await book_controller.update_book(book_id, book)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    deleted = await book_controller.delete_book(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
