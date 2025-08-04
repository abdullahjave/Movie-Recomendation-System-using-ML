#!/usr/bin/env python3
"""
Movie Recommendation System Launcher
This script helps set up and run the movie recommendation system.
"""

import os
import sys
import subprocess
import pickle
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} found")
    return True

def check_required_files():
    """Check if all required files exist"""
    required_files = [
        "movie_dict.pkl",
        "movies.pkl", 
        "Website.py",
        "requirements.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"✅ {file} found")
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    # Check optional but important file
    if not os.path.exists("similarity.pkl"):
        print("⚠️  similarity.pkl not found - please run the notebook to generate it")
        return "warning"
    else:
        print("✅ similarity.pkl found")
    
    return True

def install_requirements():
    """Install required packages"""
    try:
        print("📥 Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def run_streamlit():
    """Run the Streamlit application"""
    try:
        print("🚀 Starting Movie Recommendation System...")
        print("📱 Opening in your default browser...")
        print("Press Ctrl+C to stop the application")
        print("-" * 50)
        
        subprocess.run([sys.executable, "-m", "streamlit", "run", "Website.py"])
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start application: {e}")
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")

def main():
    """Main launcher function"""
    print("🎬 Movie Recommendation System Launcher")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check required files
    file_check = check_required_files()
    if file_check is False:
        print("\n💡 Please ensure all required files are present")
        print("Run the Jupyter notebook to generate missing pickle files")
        return
    
    # Install requirements
    if not install_requirements():
        return
    
    # Run the application
    run_streamlit()

if __name__ == "__main__":
    main()
