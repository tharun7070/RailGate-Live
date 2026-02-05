from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.crossing import Crossing
from app.services.prediction import prediction_engine

router = APIRouter(prefix="/crossings", tags=["crossings"])

@router.get("/", response_model=List[dict])
def get_all_crossings(db: Session = Depends(get_db)):
    """Get all active railway crossings"""
    crossings = db.query(Crossing).filter(Crossing.is_active == True).all()
    return [crossing.to_dict() for crossing in crossings]

@router.get("/{crossing_id}", response_model=dict)
def get_crossing(crossing_id: str, db: Session = Depends(get_db)):
    """Get specific crossing details"""
    crossing = db.query(Crossing).filter(Crossing.id == crossing_id).first()
    
    if not crossing:
        raise HTTPException(status_code=404, detail="Crossing not found")
    
    return crossing.to_dict()

@router.get("/{crossing_id}/status", response_model=dict)
def get_crossing_status(crossing_id: str, db: Session = Depends(get_db)):
    """
    Get detailed crossing status with live prediction
    
    Returns:
    - Current status (open/closing_soon/closed)
    - Confidence score
    - Next closure time
    - Train information
    - Detour recommendations
    """
    crossing = db.query(Crossing).filter(Crossing.id == crossing_id).first()
    
    if not crossing:
        raise HTTPException(status_code=404, detail="Crossing not found")
    
    # Get prediction
    prediction = prediction_engine.predict_status(crossing.to_dict())
    
    # Update crossing status in database
    crossing.current_status = prediction["status"]
    db.commit()
    
    # Combine crossing info with prediction
    response = crossing.to_dict()
    response["prediction"] = prediction
    
    return response
