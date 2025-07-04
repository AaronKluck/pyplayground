from fastapi import FastAPI
from pyplay.api.db.helpers import init_db
from pyplay.api.routes import authors, books

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


app.include_router(authors.router, prefix="/authors", tags=["authors"])
app.include_router(books.router, prefix="/books", tags=["books"])
