@echo off
echo 🎬 Starting Movie Recommendation System - Full Stack
echo.

echo 📦 Installing Python dependencies...
pip install -r requirements.txt

echo.
echo 🚀 Starting Flask API Server...
echo Server will be available at: http://localhost:5000
echo Flutter Android Emulator should use: http://10.0.2.2:5000
echo.

start "Flask API" python flask_api.py

echo.
echo 📱 Now you can run the Flutter app:
echo   1. Open Android Studio
echo   2. Open the reel_recommend folder
echo   3. Run flutter pub get
echo   4. Start an Android emulator or connect a device
echo   5. Run the app
echo.

pause
