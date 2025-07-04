from pydantic import BaseModel

__all__ = ["AuthorCreate", "AuthorRead"]


class AuthorCreate(BaseModel):
    name: str


class AuthorRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
