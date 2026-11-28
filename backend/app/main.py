from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.links.migrate import migrate


@asynccontextmanager
async def lifespan(app: FastAPI):
    migrate()
    yield


app = FastAPI(lifespan=lifespan)
