from sqlalchemy import (
    Column,
    String,
    Float,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from src.db import Base
from src.models import Metrics

class Location(Base):
    __tablename__ = "locations"

    location_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    address = Column(String(512), nullable=False, unique=True)

    region_name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    # geo_boundary = Column(Geometry(geometry_type="POLYGON", srid=4326))
    city = Column(String(255))
    country = Column(String(255))

    listings = relationship("Listing", back_populates="location")
    metrics = relationship("Metrics", back_populates="region")
    preferred_by_users = relationship("UserPreferences", back_populates="preferred_region")

    __table_args__ = (
        UniqueConstraint("city", "latitude", "longitude", name="uq_location_geo"),
    )

    def __repr__(self):
        return f"<Location(region_name={self.region_name}, country={self.country})>"


