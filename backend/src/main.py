import sys
import os

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from aiohttp import ClientSession


sys.path.insert(
    0, 
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
)


from src.auth.router import auth_router
from src.geodata import state
from src.geodata.router import geo_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("created aiohttp session...")
    state.session = ClientSession()

    yield

    print("all done here!")
    await state.session.close()

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(geo_router)

if __name__ == '__main__':
    uvicorn.run("src.main:app", host='127.0.0.1', port=8000, reload=True)
