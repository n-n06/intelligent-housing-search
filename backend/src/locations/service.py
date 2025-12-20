from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.locations.models import Location

async def get_or_create_location(
    db: AsyncSession,
    *,
    address: str,
    region_name: str,
    latitude: float | None,
    longitude: float | None,
    city: str | None = "Алматы",
    country: str | None = "Казахстан",
) -> Location:

    stmt = select(Location).where(
        Location.latitude == latitude,
        Location.longitude == longitude,
        Location.city == city,
    )

    result = await db.execute(stmt)
    location = result.scalar_one_or_none()

    if location:
        return location

    location = Location(
        address=address,
        region_name=region_name,
        latitude=latitude,
        longitude=longitude,
        city=city,
        country=country,
    )

    db.add(location)
    await db.commit()
    await db.refresh(location)

    return location
