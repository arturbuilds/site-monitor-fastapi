from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.templating import Jinja2Templates

from app.api.auth import router as auth_router
from app.api.sites import router as sites_router
from app.database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

templates = Jinja2Templates(directory='templates')
app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(sites_router)

@app.get('/')
async def start(request: Request):
    return templates.TemplateResponse('index.html', {'requests': request})