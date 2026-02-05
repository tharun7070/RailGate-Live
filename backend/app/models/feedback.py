from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base
import uuid

class Feedback(Base):
    """User feedback model for crowd-sourced status updates"""
    __tablename__ = "feedback"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    crossing_id = Column(String, nullable=False, index=True)
    
    # Status reported by user
    actual_status = Column(String, nullable=False)  # open, closed
    
    # Optional details
    notes = Column(Text, nullable=True)
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Feedback {self.id} for {self.crossing_id}>"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "crossing_id": self.crossing_id,
            "actual_status": self.actual_status,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
