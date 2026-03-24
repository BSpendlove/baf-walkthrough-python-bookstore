from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI

from app.database import Base, engine
from app.routes.books import router as books_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Bookstore API", version="0.1.0", lifespan=lifespan)
app.include_router(books_router)
