import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from config import settings
import random

class RailwayAPIService:
    """Service for fetching live train data from Railway API"""
    
    def __init__(self):
        self.base_url = settings.RAIL_API_BASE_URL
        self.api_key = settings.RAIL_API_KEY
        self.demo_mode = settings.DEMO_MODE
    
    def get_live_trains(self, station_code: str) -> List[Dict]:
        """
        Get live train arrivals at a station
        
        Args:
            station_code: Railway station code (e.g., 'BAND' for Banaswadi)
        
        Returns:
            List of train arrival data
        """
        if self.demo_mode or not self.api_key:
            return self._get_mock_train_data(station_code)
        
        try:
            # Real API call
            url = f"{self.base_url}/livetrains/station/{station_code}"
            headers = {"X-API-KEY": self.api_key}
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return self._parse_train_data(data)
        
        except Exception as e:
            print(f"⚠️ Railway API error: {e}. Falling back to mock data.")
            return self._get_mock_train_data(station_code)
    
    def _parse_train_data(self, api_response: Dict) -> List[Dict]:
        """Parse Railway API response"""
        trains = []
        
        # Parse actual API structure (adjust based on real API format)
        if "trains" in api_response:
            for train in api_response["trains"]:
                trains.append({
                    "train_number": train.get("number"),
                    "train_name": train.get("name"),
                    "scheduled_arrival": train.get("arrival_time"),
                    "expected_arrival": train.get("expected_arrival"),
                    "delay_minutes": train.get("delay", 0),
                    "platform": train.get("platform")
                })
        
        return trains
    
    def _get_mock_train_data(self, station_code: str) -> List[Dict]:
        """
        Generate realistic mock train data for demo mode
        """
        now = datetime.now()
        trains = []
        
        # Generate 3-5 trains in the next 40 minutes
        num_trains = random.randint(3, 5)
        
        train_names = [
            "Bangalore City Express",
            "Shatabdi Express",
            "Yesvantpur Express",
            "KSR Bengaluru Passenger",
            "Mysuru Express",
            "Hubli Express",
            "Chennai Express"
        ]
        
        for i in range(num_trains):
            # Random arrival time within next 40 minutes
            minutes_ahead = random.randint(5, 40)
            arrival_time = now + timedelta(minutes=minutes_ahead)
            
            # Random delay 0-5 minutes
            delay = random.randint(0, 5)
            
            trains.append({
                "train_number": f"1{random.randint(1000, 9999)}",
                "train_name": random.choice(train_names),
                "scheduled_arrival": arrival_time.strftime("%H:%M"),
                "expected_arrival": (arrival_time + timedelta(minutes=delay)).strftime("%H:%M"),
                "delay_minutes": delay,
                "platform": random.randint(1, 6),
                "eta_minutes": minutes_ahead + delay
            })
        
        # Sort by ETA
        trains.sort(key=lambda x: x.get("eta_minutes", 999))
        
        return trains

# Global instance
railway_api = RailwayAPIService()
