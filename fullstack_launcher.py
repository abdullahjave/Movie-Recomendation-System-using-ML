#!/usr/bin/env python3
"""
Full Stack Movie Recommendation System Setup
Launcher for both Flask API and Flutter app instructions
"""

import os
import sys
import subprocess
import time

def check_python_requirements():
    """Check if required Python packages are installed"""
    required_packages = ['flask', 'flask_cors', 'pandas', 'numpy', 'scikit-learn', 'requests']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    return missing

def install_requirements():
    """Install Python requirements"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Python dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Python dependencies")
        return False

def check_data_files():
    """Check if required data files exist"""
    required_files = ["movie_dict.pkl", "movies.pkl", "similarity.pkl"]
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    return missing_files

def start_flask_api():
    """Start the Flask API server"""
    print("🚀 Starting Flask API server...")
    print("📡 Server will be available at: http://localhost:5000")
    print("📱 Flutter Android Emulator should use: http://10.0.2.2:5000")
    print("📱 Flutter iOS Simulator should use: http://localhost:5000")
    print("-" * 60)
    
    try:
        subprocess.run([sys.executable, "flask_api.py"])
    except KeyboardInterrupt:
        print("\n👋 Flask API server stopped")

def print_flutter_instructions():
    """Print Flutter setup instructions"""
    print("\n" + "="*60)
    print("📱 FLUTTER APP SETUP INSTRUCTIONS")
    print("="*60)
    print("""
1. 📁 Open Android Studio
2. 📂 Open the 'reel_recommend' folder (not the root project)
3. 📦 Run: flutter pub get
4. 📱 Start an Android emulator or connect a device
5. ▶️  Run the app (F5 or Run button)

🔧 FLUTTER COMMANDS:
   cd reel_recommend
   flutter pub get
   flutter run

🌐 API ENDPOINTS:
   - Health Check: GET /health
   - All Movies: GET /movies  
   - Search: GET /search?q=movie_name
   - Recommendations: POST /recommend

📱 NETWORK CONFIGURATION:
   - Android Emulator: http://10.0.2.2:5000
   - iOS Simulator: http://localhost:5000
   - Physical Device: http://YOUR_IP:5000

🎯 If you have connection issues:
   1. Make sure Flask server is running
   2. Check your emulator/device network settings
   3. For physical devices, use your computer's IP address

""")

def main():
    """Main function"""
    print("🎬 Movie Recommendation System - Full Stack Setup")
    print("="*60)
    
    # Check Python environment
    missing_packages = check_python_requirements()
    if missing_packages:
        print(f"⚠️  Missing packages: {', '.join(missing_packages)}")
        if not install_requirements():
            return
    else:
        print("✅ Python environment ready")
    
    # Check data files
    missing_files = check_data_files()
    if missing_files:
        print(f"⚠️  Missing data files: {', '.join(missing_files)}")
        print("💡 Run the Jupyter notebook to generate missing files")
    else:
        print("✅ Data files ready")
    
    print("\n🚀 Starting services...")
    
    # Print Flutter instructions
    print_flutter_instructions()
    
    # Ask user if they want to start Flask API
    choice = input("Start Flask API server now? (y/n): ").lower().strip()
    if choice in ['y', 'yes']:
        start_flask_api()
    else:
        print("🔧 To start Flask API manually, run: python flask_api.py")

if __name__ == "__main__":
    main()
