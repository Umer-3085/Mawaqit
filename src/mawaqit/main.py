from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mawaqit.config import settings
from mawaqit.api.main import api_router
from mawaqit.database import init_db, close_db

app = FastAPI(title=settings.app_name, version=settings.app_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.on_event("startup")
async def startup():
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    await close_db()