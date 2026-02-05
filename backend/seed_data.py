"""
Seed initial crossing data for Bengaluru
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, init_db
from app.models.crossing import Crossing

def seed_data():
    """Populate database with sample Bengaluru crossing data"""
    
    # Initialize database
    init_db()
    
    db = SessionLocal()
    
    # Check if data already exists
    existing = db.query(Crossing).count()
    if existing > 0:
        print(f"⚠️ Database already has {existing} crossings. Skipping seed.")
        return
    
    crossings_data = [
        {
            "id": "hoodi-crossing",
            "name": "Hoodi Railway Crossing",
            "location": "Hoodi Circle, Whitefield, Bengaluru",
            "latitude": 12.9897,
            "longitude": 77.7166,
            "nearest_station_code": "BAND",
            "nearest_station_name": "Banaswadi",
            "distance_to_station_km": 3.5,
            "avg_close_duration_mins": 8.0,
            "buffer_minutes": 2.5,
            "reliability_score": 88.5,
            "detour_distance_km": 4.2,
            "detour_time_mins": 12.0,
            "is_active": True
        },
        {
            "id": "whitefield-crossing",
            "name": "Whitefield Railway Crossing",
            "location": "Whitefield Main Road, Bengaluru",
            "latitude": 12.9698,
            "longitude": 77.7499,
            "nearest_station_code": "WFD",
            "nearest_station_name": "Whitefield",
            "distance_to_station_km": 1.2,
            "avg_close_duration_mins": 7.5,
            "buffer_minutes": 2.0,
            "reliability_score": 92.0,
            "detour_distance_km": 3.8,
            "detour_time_mins": 10.0,
            "is_active": True
        },
        {
            "id": "kr-puram-crossing",
            "name": "KR Puram Railway Crossing",
            "location": "Old Madras Road, KR Puram, Bengaluru",
            "latitude": 13.0053,
            "longitude": 77.6957,
            "nearest_station_code": "KRU",
            "nearest_station_name": "KR Puram",
            "distance_to_station_km": 0.8,
            "avg_close_duration_mins": 9.0,
            "buffer_minutes": 3.0,
            "reliability_score": 76.5,
            "detour_distance_km": 5.5,
            "detour_time_mins": 15.0,
            "is_active": True
        }
    ]
    
    # Insert crossings
    for data in crossings_data:
        crossing = Crossing(**data)
        db.add(crossing)
    
    db.commit()
    
    print(f"✅ Seeded {len(crossings_data)} railway crossings:")
    for data in crossings_data:
        print(f"   - {data['name']}")
    
    db.close()

if __name__ == "__main__":
    print("🌱 Seeding database with sample crossing data...")
    seed_data()
    print("✅ Database seeding complete!")
