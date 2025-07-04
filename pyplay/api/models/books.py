from pydantic import BaseModel

__all__ = ["BookCreate", "BookRead"]


class BookCreate(BaseModel):
    title: str
    author_id: int


class BookRead(BaseModel):
    id: int
    title: str
    author_id: int

    class Config:
        from_attributes = True
