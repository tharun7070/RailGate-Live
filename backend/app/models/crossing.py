from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base

class Crossing(Base):
    """Railway level crossing model"""
    __tablename__ = "crossings"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    
    # Coordinates
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Railway station mapping
    nearest_station_code = Column(String, nullable=False)
    nearest_station_name = Column(String, nullable=False)
    distance_to_station_km = Column(Float, nullable=False)
    
    # Gate characteristics
    avg_close_duration_mins = Column(Float, default=8.0)
    buffer_minutes = Column(Float, default=2.5)
    reliability_score = Column(Float, default=85.0)  # 0-100
    
    # Status tracking
    current_status = Column(String, default="unknown")  # open, closing_soon, closed, unknown
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Active status
    is_active = Column(Boolean, default=True)
    
    # Detour information
    detour_distance_km = Column(Float, nullable=True)
    detour_time_mins = Column(Float, nullable=True)
    
    def __repr__(self):
        return f"<Crossing {self.name} ({self.id})>"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "nearest_station_code": self.nearest_station_code,
            "nearest_station_name": self.nearest_station_name,
            "distance_to_station_km": self.distance_to_station_km,
            "avg_close_duration_mins": self.avg_close_duration_mins,
            "buffer_minutes": self.buffer_minutes,
            "reliability_score": self.reliability_score,
            "current_status": self.current_status,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
            "is_active": self.is_active,
            "detour_distance_km": self.detour_distance_km,
            "detour_time_mins": self.detour_time_mins
        }
