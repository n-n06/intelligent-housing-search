import asyncio
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.geodata.parser import parse
from src.listings.schemas import AlmatyRegion, ListingType
from src.locations.service import get_or_create_location
from src.listings.models import Listing
from src.geodata import state



sem = asyncio.Semaphore(5)
async def fetch_listings(
    type: ListingType, region: AlmatyRegion, page: int | None = None
):
    """
    Returns a JSON array of listings
    """
    path = f"https://krisha.kz/{type.path}/kvartiry/almaty-{region.path}/"
    if page is not None:
        path = path + f"?page={page}"
        
    async with sem:
        async with state.session.get(path) as response:
            response.raise_for_status()
            html = await response.text()

    return parse(html=html)


async def fetch_listing_by_id(
    db: AsyncSession, listing_id: str
):
    result = await db.execute(select(Listing).where(
        Listing.external_id == listing_id
    ))
    listing = result.scalar_one_or_none()

    if not listing:
        raise HTTPException(status_code=404, detail="Note not found")

    return listing


async def persist_listing(
    db: AsyncSession, data: dict, type: ListingType, region: AlmatyRegion
):
    stmt = select(Listing).where(
        Listing.external_id == data["external_id"]
    )
    result = await db.execute(stmt)
    exists = result.scalar_one_or_none()

    if exists:
        return exists  # already persisted

    location = await get_or_create_location(
        db,
        address=data["location"]["address"],
        region_name=region.display_name,
        latitude=None,
        longitude=None,
        city="Алматы",
        country="Казахстан",
    )

    listing = Listing(
        external_id=data["external_id"],
        type=type.display_name,
        title=data["title"],
        room_count=int(data["room_count"]),
        area=float(data["area"]),
        description=data["description"],
        price=data["price"],
        location_id=location.location_id,
        year_built=data["year_built"],
        complex=data["complex"]
    )

    db.add(listing)
    await db.commit()
    return listing


async def persist_all(
    db: AsyncSession, parsed_listings: list[dict], type: ListingType, region: AlmatyRegion
):
    results = []
    for listing in parsed_listings:
        result = await persist_listing(
            db=db, 
            data=listing,
            type=type,
            region=region
        )
        results.append(result)
    return results
