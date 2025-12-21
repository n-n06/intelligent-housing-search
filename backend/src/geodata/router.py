from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db
from src.listings.service import fetch_listings, persist_all
from src.config import settings



