from contextlib import asynccontextmanager
from aiohttp import ClientSession
from fastapi import FastAPI


session: ClientSession | None = None

