@echo off
echo 🎬 Starting Movie Recommendation System...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python found

REM Check if virtual environment exists
if not exist "movie_recommender_env" (
    echo 📦 Creating virtual environment...
    python -m venv movie_recommender_env
)

echo 🔧 Activating virtual environment...
call movie_recommender_env\Scripts\activate

echo 📥 Installing dependencies...
pip install -r requirements.txt

echo 🔍 Checking required files...
if not exist "similarity.pkl" (
    echo ⚠️  similarity.pkl not found
    echo Please run the Jupyter notebook to generate required files
    echo Or download them from the repository
)

echo 🚀 Starting Streamlit application...
echo.
echo Opening in your default browser...
echo Press Ctrl+C to stop the application
echo.
streamlit run Website.py

pause
