from fastapi import APIRouter, HTTPException, status
from typing import List

from pyplay.api.models.authors import AuthorCreate, AuthorRead
from pyplay.api.controllers import authors as author_controller
from pyplay.api.controllers.exceptions import NotFoundError, ConflictError


router = APIRouter()


@router.post("/", response_model=AuthorRead, status_code=status.HTTP_201_CREATED)
async def create_author(author: AuthorCreate):
    result, is_new = await author_controller.create_author(author)
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


@router.get("/", response_model=List[AuthorRead])
async def list_authors():
    return await author_controller.list_authors()


@router.get("/{author_id}", response_model=AuthorRead)
async def get_author(author_id: int):
    author = await author_controller.get_author(author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.put("/{author_id}", response_model=AuthorRead)
async def update_author(author_id: int, author: AuthorCreate):
    try:
        return await author_controller.update_author(author_id, author)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(author_id: int):
    deleted = await author_controller.delete_author(author_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Author not found")
