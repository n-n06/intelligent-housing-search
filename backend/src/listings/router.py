from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.db import get_db
from src.listings.schemas import AlmatyRegion, ListingType
from src.listings.service import fetch_listing_by_id, fetch_listings, persist_all
from src.auth.dependencies import current_active_user

listing_router = APIRouter(prefix="/listings", tags=["Listings"])

@listing_router.get("/{listing_type}/{region}")
async def get_listings(
    listing_type: ListingType,
    region: AlmatyRegion,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user)
):
    listings = await fetch_listings(
        type=listing_type,
        region=region
    )
    await persist_all(
        db=db, 
        parsed_listings=listings,
        type=listing_type,
        region=region
    )

    return listings


@listing_router.get("/{listing_id}")
async def get_listing_by_id(
    listing_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user)
):
    listing = await fetch_listing_by_id(db, listing_id)

    return listing
