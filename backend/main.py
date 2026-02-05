from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from app.database import init_db, get_db, SessionLocal
from app.routes import crossings, feedback
from app.models.crossing import Crossing
from app.services.prediction import prediction_engine
from config import settings

# Background scheduler
scheduler = BackgroundScheduler()

def update_all_crossing_status():
    """Background job to update all crossing statuses"""
    print("🔄 Updating crossing statuses...")
    db = SessionLocal()
    
    try:
        crossings_list = db.query(Crossing).filter(Crossing.is_active == True).all()
        
        for crossing in crossings_list:
            try:
                prediction = prediction_engine.predict_status(crossing.to_dict())
                crossing.current_status = prediction["status"]
            except Exception as e:
                print(f"⚠️ Error updating {crossing.name}: {e}")
        
        db.commit()
        print(f"✅ Updated {len(crossings_list)} crossings")
    
    except Exception as e:
        print(f"❌ Background update failed: {e}")
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    print("🚀 Starting RailGate Live API...")
    init_db()
    
    # Start background scheduler
    if not scheduler.running:
        scheduler.add_job(
            update_all_crossing_status,
            'interval',
            seconds=settings.AUTO_REFRESH_INTERVAL_SECONDS,
            id='update_crossings',
            replace_existing=True
        )
        scheduler.start()
        print(f"⏰ Background updates every {settings.AUTO_REFRESH_INTERVAL_SECONDS}s")
    
    yield
    
    # Shutdown
    print("👋 Shutting down...")
    if scheduler.running:
        scheduler.shutdown()

# Create FastAPI app
app = FastAPI(
    title="RailGate Live API",
    description="Smart Railway Level Crossing Status & Route Decision API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(",") if settings.CORS_ORIGINS != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(crossings.router)
app.include_router(feedback.router)

@app.get("/")
def root():
    """API root endpoint"""
    return {
        "message": "🚧 RailGate Live API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "operational"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "demo_mode": settings.DEMO_MODE,
        "environment": settings.ENVIRONMENT
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
