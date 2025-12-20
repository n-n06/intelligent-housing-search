import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.geodata.parser import parse
from src.locations.service import get_or_create_location
from src.listings.models import Listing
from src.geodata import state

BASE_PATH = "https://krisha.kz/arenda/kvartiry/"


sem = asyncio.Semaphore(5)
async def fetch_listings(region: str, page: int | None = None):
    """
    Returns a JSON array of listings
    """
    path = "https://krisha.kz/arenda/kvartiry/almaty-almalinskij/"
    if page is not None:
        path = path + f"?page={page}"
        
    async with sem:
        async with state.session.get(path) as response:
            response.raise_for_status()
            html = await response.text()

    return parse(html)




async def persist_listing(db: AsyncSession, data: dict):
    stmt = select(Listing).where(
        Listing.external_id == data["external_id"]
    )
    result = await db.execute(stmt)
    exists = result.scalar_one_or_none()

    if exists:
        return exists  # already persisted

    location = await get_or_create_location(
        db,
        address=data["location"]["street"],
        region_name="Алмалинский р-н",
        latitude=None,
        longitude=None,
        city="Алматы",
        country="KZ",
    )

    listing = Listing(
        external_id=data["external_id"],
        title=data["title"],
        room_count=int(data["rooms"]),
        area=float(data["area_m2"]),
        description=data["description"],
        price=data["price"]["value"],
        location_id=location.location_id
    )

    db.add(listing)
    await db.commit()
    return listing


async def persist_all(db: AsyncSession, parsed_listings: list[dict]):
    results = []
    for listing in parsed_listings:
        result = await persist_listing(db, listing)
        results.append(result)
    return results
