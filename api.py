from contextlib import asynccontextmanager
from fastapi import FastAPI

from pyplay.api.db.helpers import init_db
from pyplay.api.routes import authors, books


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    pass


app = FastAPI(lifespan=lifespan)


app.include_router(authors.router, prefix="/authors", tags=["authors"])
app.include_router(books.router, prefix="/books", tags=["books"])
