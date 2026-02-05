# RailGate Live - Quick Start Guide

## 🚀 Running the Project

### Backend Setup (Terminal 1)

1. **Activate virtual environment:**
   ```bash
   cd backend
   venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Seed database:**
   ```bash
   python seed_data.py
   ```

4. **Start backend:**
   ```bash
   python main.py
   ```

   Backend will run at: http://localhost:8000
   API Docs: http://localhost:8000/docs

### Mobile App Setup (Terminal 2)

1. **Install dependencies:**
   ```bash
   cd mobile
   npm install
   ```

2. **Start Expo:**
   ```bash
   npm start
   ```

3. **Run on device:**
   - Scan QR code with Expo Go app (iOS/Android)
   - Press 'a' for Android emulator
   - Press 'i' for iOS simulator

## 📝 Important Notes

- Backend uses **DEMO MODE** by default (no API key needed)
- Database is SQLite (no PostgreSQL setup required)
- Mobile app connects to `http://localhost:8000`
  - For physical device: Update `API_BASE_URL` in `mobile/api/railApi.ts` to your computer's IP
  - For Android emulator: Use `http://10.0.2.2:8000`

## ✅ Verify Setup

1. Backend health check:
   ```bash
   curl http://localhost:8000/health
   ```

2. Get crossings:
   ```bash
   curl http://localhost:8000/crossings/
   ```

## 🎯 Features to Test

- ✅ Pull down to refresh crossing status
- ✅ Tap crossing card to view details
- ✅ Switch to map view
- ✅ Tap markers on map
- ✅ Test navigation buttons
- ✅ Submit status feedback

Enjoy! 🚧
