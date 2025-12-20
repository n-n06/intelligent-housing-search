from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db
from src.geodata.parser import main
from src.listings.service import fetch_listings, persist_all
from src.config import settings

geo_router = APIRouter(prefix="/geo", tags=["Geodata"])

@geo_router.get("/listings/almaly")
async def get_listings(db: AsyncSession = Depends(get_db)):
    listings = await fetch_listings("almaly")
    await persist_all(db, listings)

    return listings



@geo_router.get("/")
async def get_geodata():
    return await main()
