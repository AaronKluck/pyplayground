from fastapi import APIRouter, HTTPException, status
from typing import List
from pydantic import BaseModel
from pyplay.api.controllers import authors as author_controller


class AuthorCreate(BaseModel):
    name: str


class AuthorRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


router = APIRouter()


@router.post("/", response_model=AuthorRead, status_code=status.HTTP_201_CREATED)
async def create_author(author: AuthorCreate):
    try:
        return await author_controller.create_author(author)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


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
        updated = await author_controller.update_author(author_id, author)
        if not updated:
            raise HTTPException(status_code=404, detail="Author not found")
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(author_id: int):
    deleted = await author_controller.delete_author(author_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Author not found")
