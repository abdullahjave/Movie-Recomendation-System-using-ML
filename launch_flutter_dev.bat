@echo off
echo ==========================================
echo   Flutter Movie Recommendation App
echo ==========================================
echo.

REM Check if Flask API is already running
echo [1/4] Checking Flask API status...
timeout /t 2 >nul
curl -s http://localhost:5000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Flask API is already running
) else (
    echo [2/4] Starting Flask API backend...
    echo Opening new window for Flask API...
    start "Flask API Server" cmd /k "cd /d "%~dp0" && python flask_api.py"
    echo ⏳ Waiting for Flask API to start...
    timeout /t 8 >nul
)

echo.
echo [3/4] Opening Android Studio...
echo 📱 Please ensure you have:
echo    - Android Studio installed
echo    - Flutter plugin enabled
echo    - Android Virtual Device created
echo.

REM Try to open Android Studio with the Flutter project
if exist "C:\Program Files\Android\Android Studio\bin\studio64.exe" (
    echo Starting Android Studio...
    start "" "C:\Program Files\Android\Android Studio\bin\studio64.exe" "%~dp0Movie_recommend_App"
) else if exist "%LOCALAPPDATA%\Programs\Android Studio\bin\studio64.exe" (
    echo Starting Android Studio...
    start "" "%LOCALAPPDATA%\Programs\Android Studio\bin\studio64.exe" "%~dp0Movie_recommend_App"
) else (
    echo ⚠️  Android Studio not found in default location
    echo Please manually open Android Studio and load the project from:
    echo %~dp0Movie_recommend_App
)

echo.
echo [4/4] Next steps in Android Studio:
echo.
echo 🔧 Setup Steps:
echo    1. Wait for project to load
echo    2. Open Terminal in Android Studio
echo    3. Run: flutter pub get
echo    4. Start your Android Virtual Device
echo    5. Run: flutter run
echo.
echo 🎯 Testing the App:
echo    1. Search for a movie (e.g., "Avatar")
echo    2. Tap "Get Recommendations"
echo    3. View similar movies with details
echo.
echo 🐛 Troubleshooting:
echo    - If connection fails, ensure Flask API is running
echo    - Use movie titles exactly as they appear in search
echo    - Check that emulator has internet access
echo.
echo 📚 Full guide available in: flutter_setup_guide.md
echo.

REM Check Flask API one more time
echo Verifying Flask API connection...
timeout /t 3 >nul
curl -s http://localhost:5000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Flask API is ready at http://localhost:5000
) else (
    echo ❌ Flask API not responding
    echo    Please start it manually: python flask_api.py
)

echo.
echo 🚀 Ready to develop! Happy coding! 🎬
echo ==========================================
pause
