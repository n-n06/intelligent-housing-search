from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Text,
    TIMESTAMP,
    ForeignKey,
    CheckConstraint,
    Boolean,
    Numeric,
    func,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid

from src.db import Base


# class Location(Base):
#     __tablename__ = "locations"
#
#     location_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     address = Column(String(512), nullable=False, unique=True)
#
#     region_name = Column(String(255), nullable=False)
#     latitude = Column(Float, nullable=True)
#     longitude = Column(Float, nullable=True)
#     # geo_boundary = Column(Geometry(geometry_type="POLYGON", srid=4326))
#     city = Column(String(255))
#     country = Column(String(255))
#
#     listings = relationship("Listing", back_populates="location")
#     metrics = relationship("Metrics", back_populates="region")
#     preferred_by_users = relationship("UserPreferences", back_populates="preferred_region")
#
#     __table_args__ = (
#         UniqueConstraint("city", "latitude", "longitude", name="uq_location_geo"),
#     )
#
#     def __repr__(self):
#         return f"<Location(region_name={self.region_name}, country={self.country})>"
#

# class Listing(Base):
#     __tablename__ = "listings"
#
#     listing_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     external_id = Column(String(32), nullable=False, unique=True)
#
#     title = Column(String(255), nullable=False)
#     room_count = Column(Integer, nullable=False)
#     area = Column(Float, nullable=False)
#     description = Column(Text)
#     price = Column(Float, nullable=False)
#     posted_at = Column(TIMESTAMP(False), server_default=func.now())
#
#     location_id = Column(UUID(as_uuid=True), ForeignKey("locations.location_id"), nullable=False)
#
#     location = relationship("Location", back_populates="listings")
#     favorites = relationship("FavoriteListing", back_populates="listings")
#
#     def __repr__(self):
#         return f"<Listing(title={self.title}, price={self.price})>"
#
#
# class FavoriteListing(Base):
#     __tablename__ = "favorite_listings"
#
#     favorite_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
#     listing_id = Column(UUID(as_uuid=True), ForeignKey("listings.listing_id"), nullable=False)
#     saved_at = Column(TIMESTAMP(False), server_default=func.now())
#
#     __table_args__ = (
#         UniqueConstraint("user_id", "listing_id", name="uq_user_listing"),
#     )
#
#     listing = relationship("Listing", back_populates="favorites")
#
#     def __repr__(self):
#         return f"<FavoriteListing(user_id={self.user_id}, listing_id={self.listing_id})>"
#
#


class Metrics(Base):
    __tablename__ = "metrics"

    metric_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    metric_type = Column(
        String(50),
        CheckConstraint("metric_type IN ('Market', 'Demographic', 'Environmental')"),
    )
    region_id = Column(UUID(as_uuid=True), ForeignKey("locations.location_id"), nullable=False)
    metric_value = Column(Numeric(15, 5), nullable=False)
    metric_data = Column(JSONB)
    source_id = Column(UUID(as_uuid=True), ForeignKey("data_sources.data_source_id"))
    effective_from = Column(TIMESTAMP)
    effective_to = Column(TIMESTAMP)
    is_current = Column(Boolean, server_default="TRUE")
    agent_name = Column(String(255))

    region = relationship("Location", back_populates="metrics")
    source = relationship("DataSource", back_populates="metrics")

    def __repr__(self):
        return f"<Metrics(metric_type={self.metric_type}, value={self.metric_value})>"

class UserPreferences(Base):
    __tablename__ = "user_preferences"

    preferences_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    max_price = Column(Float)
    min_rooms = Column(Integer)
    preferred_region_id = Column(UUID(as_uuid=True), ForeignKey("locations.location_id"))
    updated_at = Column(TIMESTAMP(False), server_default=func.now())

    preferred_region = relationship("Location", back_populates="preferred_by_users")

    def __repr__(self):
        return f"<UserPreferences(user_id={self.user_id}, max_price={self.max_price})>"


class DataSource(Base):
    __tablename__ = "data_sources"

    data_source_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_name = Column(String(255))
    source_type = Column(String(50))
    source_url = Column(Text)
    source_params = Column(JSONB)
    last_scraped_at = Column(TIMESTAMP)

    metrics = relationship("Metrics", back_populates="source")

    def __repr__(self):
        return f"<DataSource(source_name={self.source_name}, type={self.source_type})>"


