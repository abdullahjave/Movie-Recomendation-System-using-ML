@echo off
echo 🎬 Starting Movie Recommendation API for Android Connection...
echo.
echo 📍 Your machine IP: 192.168.1.4
echo 🚀 API will be available at:
echo    - http://localhost:5000 (local testing)
echo    - http://192.168.1.4:5000 (physical Android device)
echo    - http://10.0.2.2:5000 (Android emulator)
echo.
echo ⚠️  Make sure your Android device and computer are on the same WiFi network
echo ⚠️  For emulator, use http://10.0.2.2:5000
echo ⚠️  For physical device, use http://192.168.1.4:5000
echo.
echo 🔧 Starting Flask server...
python flask_api.py
pause
