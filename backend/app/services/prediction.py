from typing import Dict, List, Optional
from datetime import datetime, timedelta
from app.services.railway_api import railway_api
from config import settings

class PredictionEngine:
    """
    Advanced prediction engine for railway crossing status
    
    Algorithm:
    1. Fetch live trains arriving at nearest station (next 40 mins)
    2. Calculate when each train will pass the crossing
    3. Determine gate closure windows
    4. Check if current time falls in any window
    5. Calculate confidence based on data quality
    """
    
    def __init__(self):
        self.buffer_minutes = settings.BUFFER_MINUTES
        self.avg_close_duration = settings.AVG_CLOSE_DURATION
        self.train_speed = settings.TRAIN_SPEED_KM_MIN
        self.prediction_window = settings.PREDICTION_WINDOW_MINUTES
        self.closing_soon_threshold = settings.CLOSING_SOON_THRESHOLD_MINUTES
    
    def predict_status(self, crossing: Dict) -> Dict:
        """
        Predict crossing status with detailed information
        
        Args:
            crossing: Crossing object with station and location data
        
        Returns:
            Detailed status prediction
        """
        station_code = crossing.get("nearest_station_code")
        distance_km = crossing.get("distance_to_station_km", 2.0)
        
        # Fetch live train data
        trains = railway_api.get_live_trains(station_code)
        
        # Calculate closure windows
        closure_windows = self._calculate_closure_windows(trains, distance_km)
        
        # Determine current status
        now = datetime.now()
        status_data = self._determine_status(now, closure_windows)
        
        # Calculate confidence
        confidence = self._calculate_confidence(trains, crossing)
        
        # Get crowd wisdom
        crowd_data = self._get_crowd_wisdom(crossing.get("id"))
        
        # Build response
        return {
            "status": status_data["status"],
            "confidence": confidence,
            "next_closure": status_data.get("next_closure"),
            "estimated_duration_mins": status_data.get("duration"),
            "time_until_closure_mins": status_data.get("time_until"),
            "trains_approaching": len(trains),
            "closure_windows": closure_windows[:3],  # Next 3 windows
            "crowd_confirmations": crowd_data["confirmations"],
            "last_crowd_update": crowd_data["last_update"],
            "detour_recommendation": self._calculate_detour_score(
                status_data, crossing
            )
        }
    
    def _calculate_closure_windows(self, trains: List[Dict], distance_km: float) -> List[Dict]:
        """Calculate when gates will close based on train schedule"""
        windows = []
        
        for train in trains:
            # Get train ETA in minutes
            eta_mins = train.get("eta_minutes")
            if eta_mins is None:
                continue
            
            # Calculate time for train to reach crossing from station
            travel_time = distance_km / self.train_speed
            
            # Time when train passes crossing
            pass_time_mins = eta_mins - travel_time
            
            # Gate closes BEFORE train arrives
            close_start = pass_time_mins - self.buffer_minutes
            close_end = pass_time_mins + self.avg_close_duration
            
            if close_start < self.prediction_window:
                windows.append({
                    "train_name": train.get("train_name"),
                    "train_number": train.get("train_number"),
                    "close_start_mins": round(close_start, 1),
                    "close_end_mins": round(close_end, 1),
                    "duration_mins": round(self.avg_close_duration, 1)
                })
        
        # Sort by closure start time
        windows.sort(key=lambda x: x["close_start_mins"])
        return windows
    
    def _determine_status(self, now: datetime, windows: List[Dict]) -> Dict:
        """Determine if gate is open, closing soon, or closed"""
        if not windows:
            return {
                "status": "open",
                "next_closure": None,
                "duration": None,
                "time_until": None
            }
        
        # Check if we're in any closure window
        for window in windows:
            if window["close_start_mins"] <= 0 <= window["close_end_mins"]:
                return {
                    "status": "closed",
                    "next_closure": "now",
                    "duration": abs(window["close_end_mins"]),
                    "time_until": 0,
                    "train_info": {
                        "name": window["train_name"],
                        "number": window["train_number"]
                    }
                }
        
        # Check if closure is imminent
        next_window = windows[0]
        if 0 < next_window["close_start_mins"] <= self.closing_soon_threshold:
            return {
                "status": "closing_soon",
                "next_closure": f"in {int(next_window['close_start_mins'])} mins",
                "duration": next_window["duration_mins"],
                "time_until": round(next_window["close_start_mins"], 1),
                "train_info": {
                    "name": next_window["train_name"],
                    "number": next_window["train_number"]
                }
            }
        
        # Gate is open
        return {
            "status": "open",
            "next_closure": f"in {int(next_window['close_start_mins'])} mins",
            "duration": next_window["duration_mins"],
            "time_until": round(next_window["close_start_mins"], 1),
            "train_info": {
                "name": next_window["train_name"],
                "number": next_window["train_number"]
            }
        }
    
    def _calculate_confidence(self, trains: List[Dict], crossing: Dict) -> float:
        """Calculate prediction confidence (0-100)"""
        base_confidence = 75.0
        
        # More trains = more data = higher confidence
        if len(trains) >= 3:
            base_confidence += 10
        
        # Use gate's historical reliability
        reliability = crossing.get("reliability_score", 85.0)
        
        # Weighted average
        confidence = (base_confidence * 0.6) + (reliability * 0.4)
        
        return round(min(confidence, 95.0), 1)
    
    def _get_crowd_wisdom(self, crossing_id: str) -> Dict:
        """Get recent crowd confirmations (simplified for now)"""
        # TODO: Query feedback table for recent confirmations
        return {
            "confirmations": 0,
            "last_update": None
        }
    
    def _calculate_detour_score(self, status_data: Dict, crossing: Dict) -> Optional[Dict]:
        """Calculate if detouring saves time"""
        if status_data["status"] == "open":
            return None
        
        wait_time = status_data.get("duration", 8)
        detour_time = crossing.get("detour_time_mins")
        
        if not detour_time:
            return None
        
        time_saved = wait_time - detour_time
        
        if time_saved > 2:
            recommendation = "detour"
            message = f"Save ~{int(time_saved)} minutes by detouring"
        elif time_saved < -2:
            recommendation = "wait"
            message = f"Waiting saves ~{int(abs(time_saved))} minutes"
        else:
            recommendation = "neutral"
            message = "Similar time either way"
        
        return {
            "recommendation": recommendation,
            "wait_time_mins": round(wait_time, 1),
            "detour_time_mins": round(detour_time, 1),
            "time_saved_mins": round(time_saved, 1),
            "message": message
        }

# Global instance
prediction_engine = PredictionEngine()
