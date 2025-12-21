import uuid
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Text,
    TIMESTAMP,
    ForeignKey,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM as PgEnum


from src.db import Base
from src.listings.schemas import ListingTypeDisplay


class Listing(Base):
    __tablename__ = "listings"

    listing_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    external_id = Column(String(32), nullable=False, unique=True)

    type = Column(
        PgEnum(ListingTypeDisplay, name="listing_type", create_type=False),
        nullable=False,
        index=True,
    )

    title = Column(String(255), nullable=False)
    room_count = Column(Integer, nullable=False)
    area = Column(Float, nullable=False)
    floor = Column(String(64), nullable=True)
    description = Column(Text)
    price = Column(Float, nullable=False)
    year_built = Column(Integer, nullable=True)
    complex = Column(String(128), nullable=True)
    posted_at = Column(TIMESTAMP(False), server_default=func.now())

    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.location_id"), nullable=False)

    location = relationship("Location", back_populates="listings")

    favorites = relationship(
        "FavoriteListing",
        back_populates="listing",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Listing(title={self.title}, price={self.price})>"


class FavoriteListing(Base):
    __tablename__ = "favorite_listings"

    favorite_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    listing_id = Column(UUID(as_uuid=True), ForeignKey("listings.listing_id"), nullable=False)
    saved_at = Column(TIMESTAMP(False), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "listing_id", name="uq_user_listing"),
    )

    listing = relationship(
        "Listing",
        back_populates="favorites"
    )

    def __repr__(self):
        return f"<FavoriteListing(user_id={self.user_id}, listing_id={self.listing_id})>"
