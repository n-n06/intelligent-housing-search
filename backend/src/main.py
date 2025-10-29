from fastapi import FastAPI
import uvicorn

from src.auth.router import auth_router

app = FastAPI()


app.include_router(auth_router)

