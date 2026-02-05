# 🚧 RailGate Live

[![Made with FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React Native](https://img.shields.io/badge/React_Native-0.72+-61DAFB?logo=react&logoColor=black)](https://reactnative.dev/)
[![Expo](https://img.shields.io/badge/Expo-~49.0-000020?logo=expo&logoColor=white)](https://expo.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Smart Railway Level Crossing Status & Intelligent Route Decision App**

RailGate Live helps Bengaluru commuters avoid unnecessary waiting at railway level crossings by providing **real-time gate status predictions** up to 40 minutes in advance and **smart detour recommendations** backed by live crowd wisdom.

> *Don't wait at the gate. Decide before you reach it.* 🚀

---

## 📌 The Problem

In metro cities like Bengaluru, railway level crossings close frequently and unpredictably. Daily commuters face:
- **5-10 minute delays** at closed gates with no advance warning
- Uncertainty about whether to wait or take an alternate route
- Traffic congestion and fuel wastage at crossings
- No visibility into when the gate will reopen

**Impact:** 1000s of commuters lose precious time every day, especially on the Whitefield-KR Puram corridor.

---

## 💡 Our Solution

**RailGate Live** predicts railway crossing status in real-time using live train data and crowd-sourced intelligence, empowering commuters to make informed routing decisions **before** they encounter a closed gate.

### Core Features

✅ **Advanced Prediction** - Know gate status up to 40 minutes ahead  
✅ **Smart Detour Scoring** - "Wait 8 mins vs detour adds 12 mins → Save time by waiting"  
✅ **Gate Personality** - Each gate gets a reliability rating (Reliable ✅ | Sneaky 🔀 | Predictable 📊)  
✅ **Live Crowd Wisdom** - "3 people just passed this gate ✅"  
✅ **Seamless Navigation** - One-tap integration with Google Maps  
✅ **Cross-Platform** - Single React Native app for iOS & Android  

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Mobile App (React Native + Expo)         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  List View   │  │   Map View   │  │  Onboarding  │      │
│  │ - Status Card│  │ - Markers    │  │ - 3-page flow│      │
│  │ - Pull Refresh│ │ - Nav buttons│  │ - Disclaimer │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API (HTTPS)
                         │
┌────────────────────────▼────────────────────────────────────┐
│              FastAPI Backend (Python 3.11)                   │
│  ┌──────────────────┐  ┌──────────────────┐               │
│  │ Prediction Engine│  │ Background Jobs  │               │
│  │ - Multi-window   │  │ - Auto-refresh   │               │
│  │ - Confidence calc│  │ - Every 90 sec   │               │
│  └──────────────────┘  └──────────────────┘               │
└────────────┬──────────────┬──────────────┬─────────────────┘
             │              │              │
    ┌────────▼────┐  ┌─────▼──────┐  ┌────▼─────────┐
    │ PostgreSQL  │  │ Railway    │  │ Crowd        │
    │ Database    │  │ Live API   │  │ Feedback     │
    │ - 4 tables  │  │ (Train ETA)│  │ (Real-time)  │
    └─────────────┘  └────────────┘  └──────────────┘
```

---

## 🔧 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework with auto-generated API docs
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Robust relational database
- **APScheduler** - Background task scheduler for auto-updates
- **Requests** - HTTP client for Railway API integration
- **Docker** - Containerized deployment

### Mobile
- **React Native** - Cross-platform mobile framework
- **Expo** - Development toolchain and runtime
- **TypeScript** - Type-safe JavaScript
- **react-native-maps** - Interactive map component
- **@react-navigation** - Screen navigation
- **axios** - HTTP client for API calls

### Infrastructure
- **Docker Compose** - Multi-container orchestration
- **Railway / Render** - Cloud deployment platforms
- **Git** - Version control

---

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ and npm
- **Python** 3.11+
- **Docker** & Docker Compose (recommended)
- **Expo Go** app on your mobile device

### 1. Clone the Repository
```bash
git clone <repository-url>
cd railway
```

### 2. Start Backend (Option A: Docker - Recommended)
```bash
cd backend
cp .env.example .env
# Edit .env and add your RAIL_API_KEY from indianrailapi.com

docker-compose up -d
```

The backend will be available at `http://localhost:8000`  
API Documentation: `http://localhost:8000/docs`

### 2. Start Backend (Option B: Without Docker)
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python seed_data.py  # Populate sample data
python main.py
```

### 3. Start Mobile App
```bash
cd mobile
npm install
npm start
```

Scan the QR code with **Expo Go** app on your phone, or:
- Press `a` for Android emulator
- Press `i` for iOS simulator

---

## 📱 App Screens

### Home Screen
- **Summary Card**: Quick overview (X Open, Y Closing, Z Closed)
- **Crossing List**: Scrollable cards with live status
- **Status Indicators**: 🟢 Open | 🟡 Closing Soon | 🔴 Closed
- **Pull to Refresh**: Swipe down to force update
- **Map View Button**: Switch to map visualization

### Map Screen
- **Interactive Map**: Centered on Bengaluru with gate markers
- **Color-Coded Markers**: Green/Yellow/Red based on status
- **Bottom Sheet**: Tap marker to see details
- **Navigation Buttons**: 
  - 🧭 Navigate via gate
  - 🔀 Navigate avoiding gate
  - 📝 Report current status

### Onboarding (First Launch)
- Welcome screen with app features
- How it works explanation
- Safety disclaimer and user responsibility

---

## 🎯 Unique Selling Points

### 1. Smart Detour Score 🧮
Not just status - we calculate if detouring **actually saves time**:
```
Wait 8 mins vs detour adds 4 mins → Save 4 minutes ✅ (Detour recommended)
Wait 8 mins vs detour adds 12 mins → Lose 4 minutes ❌ (Wait recommended)
```

### 2. Gate Personality 🎭
Each gate gets a **reliability rating** based on prediction accuracy:
- **Reliable** ✅: 90%+ accurate predictions
- **Sneaky** 🔀: <75% accurate, unpredictable closures
- **Predictable** 📊: 75-90% accurate, follows schedule

### 3. Live Crowd Wisdom 👥
Real-time confirmations from other users:
- "**3 people just passed this gate** ✅"
- Community-driven accuracy improvements
- Anonymous, privacy-first feedback

---

## 📊 Prediction Algorithm

```
INPUT: Crossing location + Nearest railway station code
  ↓
FETCH: All trains arriving at station (next 40 minutes) from Railway API
  ↓
FOR EACH TRAIN:
  Calculate gate closure window:
    pass_time = train_eta - (distance_to_gate / avg_train_speed)
    window = [pass_time - buffer, pass_time + close_duration]
  ↓
CHECK CURRENT TIME against all windows:
  - Inside any window? → Status: CLOSED
  - Window starts in < 7 mins? → Status: CLOSING_SOON  
  - Otherwise → Status: OPEN
  ↓
CALCULATE CONFIDENCE: Based on data quality & gate history
  ↓
OUTPUT: Status + Confidence + Next closure time + Duration
```

**Key Parameters:**
- `buffer_minutes`: 2.5 (gate closes before train arrives)
- `avg_close_duration`: 8.0 minutes
- `train_speed`: 0.8 km/min (~48 km/h average)
- `prediction_window`: 40 minutes ahead

---

## 📂 Project Structure

```
railway/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── models/            # SQLAlchemy database models
│   │   ├── routes/            # API endpoint handlers
│   │   ├── services/          # Business logic (prediction, Railway API)
│   │   └── database.py        # DB connection setup
│   ├── docker-compose.yml     # Multi-container setup
│   ├── Dockerfile             # Backend container
│   ├── main.py               # FastAPI app entry point
│   ├── config.py             # Environment configuration
│   ├── seed_data.py          # Sample data initialization
│   └── requirements.txt      # Python dependencies
│
├── mobile/                     # React Native app
│   ├── api/                   # API client (railApi.ts)
│   ├── components/            # Reusable UI components
│   │   ├── CrossingCard.tsx
│   │   ├── CrossingMap.tsx
│   │   └── StatusBadge.tsx
│   ├── screens/              # App screens
│   │   ├── HomeScreen.tsx
│   │   ├── MapScreen.tsx
│   │   └── OnboardingScreen.tsx
│   ├── App.tsx               # Root component
│   ├── app.json              # Expo configuration
│   └── package.json          # Node dependencies
│
├── README.md                  # This file
├── QUICKSTART.md             # 5-minute setup guide
├── DEPLOYMENT.md             # Production deployment guide
├── PROJECT_SUMMARY.md        # Detailed project overview
├── TROUBLESHOOTING.md        # Common issues & solutions
└── API_TESTING.md            # API endpoint examples

```

---

## � Documentation

- **[QUICKSTART.md](./QUICKSTART.md)** - Get started in 5 minutes
- **[PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)** - Comprehensive project overview
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Deploy to Railway/Render
- **[DEVELOPMENT.md](./DEVELOPMENT.md)** - Development workflow
- **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)** - Common issues & fixes
- **[API_TESTING.md](./API_TESTING.md)** - API endpoint reference
- **[DEMO_MODE_QUICKSTART.md](./DEMO_MODE_QUICKSTART.md)** - Demo mode setup

---

## 🔌 API Endpoints

### Core Endpoints
```bash
GET  /crossings/               # List all railway crossings
GET  /crossings/{id}           # Get specific crossing details
GET  /crossings/{id}/status    # Get detailed status with prediction
POST /feedback/                # Submit crowd-sourced status update
GET  /health                   # Health check
```

**Interactive API Docs:** Visit `http://localhost:8000/docs` after starting the backend

---

## 🧪 Testing

### Backend API
```bash
# Health check
curl http://localhost:8000/health

# Get all crossings
curl http://localhost:8000/crossings/

# Get detailed status
curl http://localhost:8000/crossings/{crossing_id}/status

# Submit feedback
curl -X POST http://localhost:8000/feedback/ \
  -H "Content-Type: application/json" \
  -d '{"crossing_id":"xxx","actual_status":"open","notes":"Just passed"}'
```

### Mobile App
1. Pull down on home screen to refresh
2. Tap "Map View" to test navigation
3. Tap a gate marker to open bottom sheet
4. Test navigation buttons (requires Google Maps installed)
5. Submit feedback and verify it appears in status

---

## 🌐 Deployment

### Backend Deployment (Railway)
```bash
cd backend
railway login
railway init
railway add  # Add PostgreSQL plugin
railway up
```

### Backend Deployment (Render)
1. Create new Web Service
2. Connect GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add PostgreSQL database
6. Configure environment variables

### Mobile App Build
```bash
cd mobile
eas build --platform android  # Build APK
eas build --platform ios       # Build for iOS
eas submit                     # Submit to app stores
```

**Detailed instructions:** See [DEPLOYMENT.md](./DEPLOYMENT.md)

---

## 🔐 Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/railgate
RAIL_API_KEY=your_key_from_indianrailapi_com
ENVIRONMENT=development
CORS_ORIGINS=*
```

### Mobile (api/railApi.ts)
```typescript
const API_BASE_URL = 'http://localhost:8000';  // Development
// const API_BASE_URL = 'https://your-app.railway.app';  // Production
```

---

## 🎨 Screenshots

| Home Screen | Map View | Gate Details |
|-------------|----------|--------------|
| ![Home](docs/screenshots/home.png) | ![Map](docs/screenshots/map.png) | ![Details](docs/screenshots/details.png) |

---

## 🚧 Current Limitations

- **Location Coverage**: Currently seeded with 3 Bengaluru gates (Hoodi, Whitefield, KR Puram)
- **Railway API**: Depends on external API uptime and accuracy
- **Prediction Accuracy**: Improves with more crowd-sourced feedback
- **Free Tier**: Limited to ~1000 API requests/day on free hosting

---

## 🗺️ Roadmap

### Phase 1 (Current) ✅
- [x] Real-time status prediction
- [x] Mobile app with map view
- [x] Crowd-sourced feedback
- [x] Smart detour recommendations
- [x] Gate personality system

### Phase 2 (Next) 🚀
- [ ] Push notifications for favorite gates
- [ ] Historical analytics ("Usually closes at 5 PM")
- [ ] Multi-city support (Mumbai, Delhi, Chennai)
- [ ] Route optimization (avoid all closed gates)
- [ ] Integration with Ola/Uber APIs

### Phase 3 (Future) 🌟
- [ ] Machine learning for improved predictions
- [ ] Traffic integration (combine gate + traffic data)
- [ ] Web dashboard for administrators
- [ ] Enterprise API for delivery companies

---

## 👥 Target Users

1. **Daily Commuters** - Whitefield ↔ Bangalore East corridor
2. **Delivery Drivers** - Zomato, Swiggy, Amazon riders  
3. **Cab Drivers** - Ola, Uber, auto drivers
4. **Logistics** - Courier services, delivery fleets
5. **Residents** - Anyone living near railway crossings

---

## 🏆 Competitive Advantage

| Feature | RailGate Live | Google Maps | Other Apps |
|---------|---------------|-------------|------------|
| Real-time gate status | ✅ Yes | ❌ No | ⚠️ Limited |
| Future predictions (40 mins) | ✅ Yes | ❌ No | ❌ No |
| Detour time calculations | ✅ Yes | ⚠️ Traffic only | ❌ No |
| Gate reliability rating | ✅ Unique | ❌ No | ❌ No |
| Crowd wisdom | ✅ Yes | ⚠️ Implicit | ❌ No |
| Bengaluru-optimized | ✅ Yes | ⚠️ Generic | ⚠️ Generic |

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Indian Railway API** - Live train status data
- **OpenStreetMap** - Gate location data  
- **Bengaluru Commuters** - Problem validation and feedback
- **Railway Community** - Testing and insights

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Documentation**: Check the `/docs` endpoint on your backend
- **Community**: Share feedback to improve predictions

---

**Built with ❤️ for Bengaluru commuters**

*Don't wait at the gate. Decide before you reach it.* 🚧



