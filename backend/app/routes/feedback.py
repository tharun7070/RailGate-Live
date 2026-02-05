from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta
from app.database import get_db
from app.models.feedback import Feedback

router = APIRouter(prefix="/feedback", tags=["feedback"])

class FeedbackCreate(BaseModel):
    crossing_id: str
    actual_status: str  # "open" or "closed"
    notes: Optional[str] = None

@router.post("/", response_model=dict)
def submit_feedback(feedback_data: FeedbackCreate, db: Session = Depends(get_db)):
    """
    Submit crowd-sourced status feedback
    
    Allows users to report actual gate status for accuracy improvement
    """
    # Validate status
    if feedback_data.actual_status not in ["open", "closed"]:
        raise HTTPException(
            status_code=400, 
            detail="Status must be 'open' or 'closed'"
        )
    
    # Create feedback record
    feedback = Feedback(
        crossing_id=feedback_data.crossing_id,
        actual_status=feedback_data.actual_status,
        notes=feedback_data.notes
    )
    
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    
    return {
        "success": True,
        "message": "Thank you for your feedback!",
        "feedback": feedback.to_dict()
    }

@router.get("/{crossing_id}/recent", response_model=List[dict])
def get_recent_feedback(
    crossing_id: str, 
    hours: int = 1,
    db: Session = Depends(get_db)
):
    """Get recent feedback for a crossing (last N hours)"""
    cutoff_time = datetime.now() - timedelta(hours=hours)
    
    feedback_list = db.query(Feedback).filter(
        Feedback.crossing_id == crossing_id,
        Feedback.created_at >= cutoff_time
    ).order_by(Feedback.created_at.desc()).all()
    
    return [f.to_dict() for f in feedback_list]

@router.get("/{crossing_id}/stats", response_model=dict)
def get_feedback_stats(crossing_id: str, db: Session = Depends(get_db)):
    """Get aggregated feedback statistics"""
    # Last hour
    one_hour_ago = datetime.now() - timedelta(hours=1)
    
    recent = db.query(Feedback).filter(
        Feedback.crossing_id == crossing_id,
        Feedback.created_at >= one_hour_ago
    ).all()
    
    open_count = sum(1 for f in recent if f.actual_status == "open")
    closed_count = sum(1 for f in recent if f.actual_status == "closed")
    
    return {
        "crossing_id": crossing_id,
        "last_hour_total": len(recent),
        "open_reports": open_count,
        "closed_reports": closed_count,
        "consensus": "open" if open_count > closed_count else "closed" if closed_count > 0 else "unknown"
    }
