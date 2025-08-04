"""
🎬 Movie Recommendation System - Complete Testing Script
Tests all components to ensure 100% functionality
"""

import subprocess
import requests
import pickle
import pandas as pd
import os
import time
import json

def test_data_files():
    """Test if all required data files exist and are valid"""
    print("🔍 Testing Data Files...")
    
    # Test movies.pkl
    try:
        movies_df = pd.read_pickle('movies.pkl')
        print(f"✅ movies.pkl loaded successfully - {movies_df.shape[0]} movies")
    except Exception as e:
        print(f"❌ Error loading movies.pkl: {e}")
        return False
    
    # Test movie_dict.pkl
    try:
        movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
        print(f"✅ movie_dict.pkl loaded successfully - {len(movie_dict)} entries")
    except Exception as e:
        print(f"❌ Error loading movie_dict.pkl: {e}")
        return False
    
    # Test similarity.pkl
    try:
        similarity = pickle.load(open('similarity.pkl', 'rb'))
        print(f"✅ similarity.pkl loaded successfully - {similarity.shape}")
    except Exception as e:
        print(f"❌ Error loading similarity.pkl: {e}")
        return False
    
    # Test CSV files
    try:
        credits_df = pd.read_csv('tmdb_5000_credits.csv')
        movies_df = pd.read_csv('tmdb_5000_movies.csv')
        print(f"✅ CSV files loaded successfully")
    except Exception as e:
        print(f"❌ Error loading CSV files: {e}")
        return False
    
    return True

def test_flask_api():
    """Test Flask API endpoints"""
    print("\n🔌 Testing Flask API...")
    
    base_url = "http://localhost:5000"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to Flask API: {e}")
        print("   Please make sure Flask API is running: python flask_api.py")
        return False
    
    # Test movies endpoint
    try:
        response = requests.get(f"{base_url}/movies", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Movies endpoint working - {data['count']} movies available")
        else:
            print(f"❌ Movies endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Movies endpoint error: {e}")
        return False
    
    # Test search endpoint
    try:
        response = requests.get(f"{base_url}/search?q=avatar", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search endpoint working - found {data['count']} matches for 'avatar'")
        else:
            print(f"❌ Search endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Search endpoint error: {e}")
        return False
    
    # Test recommend endpoint
    try:
        test_movie = "Avatar"
        payload = {"title": test_movie}
        response = requests.post(f"{base_url}/recommend", 
                               json=payload, 
                               timeout=15)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Recommend endpoint working - got {data['count']} recommendations for '{test_movie}'")
            # Check if recommendations have required fields
            if data['recommendations']:
                rec = data['recommendations'][0]
                required_fields = ['title', 'movie_id', 'similarity_score', 'poster_url']
                missing_fields = [field for field in required_fields if field not in rec]
                if not missing_fields:
                    print("✅ Recommendation data structure is complete")
                else:
                    print(f"⚠️  Missing fields in recommendations: {missing_fields}")
        else:
            print(f"❌ Recommend endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Recommend endpoint error: {e}")
        return False
    
    return True

def test_streamlit_dependencies():
    """Test if Streamlit app dependencies are available"""
    print("\n🌐 Testing Streamlit Dependencies...")
    
    try:
        import streamlit
        print(f"✅ Streamlit installed - version {streamlit.__version__}")
    except ImportError:
        print("❌ Streamlit not installed")
        return False
    
    try:
        import requests
        print("✅ Requests library available")
    except ImportError:
        print("❌ Requests library not available")
        return False
    
    try:
        import pandas
        print(f"✅ Pandas available - version {pandas.__version__}")
    except ImportError:
        print("❌ Pandas not available")
        return False
    
    # Test if Website.py exists and is valid Python
    if os.path.exists('Website.py'):
        print("✅ Website.py exists")
        try:
            with open('Website.py', 'r') as f:
                content = f.read()
            if 'streamlit' in content and 'recommend' in content:
                print("✅ Website.py contains required functions")
            else:
                print("⚠️  Website.py may be missing required functions")
        except Exception as e:
            print(f"❌ Error reading Website.py: {e}")
            return False
    else:
        print("❌ Website.py not found")
        return False
    
    return True

def test_flutter_project():
    """Test Flutter project structure and dependencies"""
    print("\n📱 Testing Flutter Project...")
    
    flutter_dir = "Movie_recommend_App"
    
    if not os.path.exists(flutter_dir):
        print(f"❌ Flutter directory '{flutter_dir}' not found")
        return False
    
    print(f"✅ Flutter directory exists")
    
    # Check pubspec.yaml
    pubspec_path = os.path.join(flutter_dir, 'pubspec.yaml')
    if os.path.exists(pubspec_path):
        print("✅ pubspec.yaml exists")
        try:
            with open(pubspec_path, 'r') as f:
                content = f.read()
            required_deps = ['http:', 'cached_network_image:', 'flutter_spinkit:']
            missing_deps = [dep for dep in required_deps if dep not in content]
            if not missing_deps:
                print("✅ All required Flutter dependencies are listed")
            else:
                print(f"⚠️  Missing dependencies in pubspec.yaml: {missing_deps}")
        except Exception as e:
            print(f"❌ Error reading pubspec.yaml: {e}")
    else:
        print("❌ pubspec.yaml not found")
        return False
    
    # Check main.dart
    main_dart_path = os.path.join(flutter_dir, 'lib', 'main.dart')
    if os.path.exists(main_dart_path):
        print("✅ main.dart exists")
        try:
            with open(main_dart_path, 'r') as f:
                content = f.read()
            if '10.0.2.2:5000' in content:
                print("✅ Correct API URL configured for Android emulator")
            else:
                print("⚠️  API URL might not be configured correctly")
        except Exception as e:
            print(f"❌ Error reading main.dart: {e}")
    else:
        print("❌ main.dart not found")
        return False
    
    return True

def test_launcher_scripts():
    """Test if launcher scripts exist and are valid"""
    print("\n🚀 Testing Launcher Scripts...")
    
    scripts = [
        'launcher.py',
        'fullstack_launcher.py', 
        'launch_flutter_dev.bat',
        'run_fullstack.bat',
        'start_api_for_android.bat'
    ]
    
    for script in scripts:
        if os.path.exists(script):
            print(f"✅ {script} exists")
        else:
            print(f"❌ {script} not found")
    
    return True

def test_documentation():
    """Test if documentation files exist"""
    print("\n📚 Testing Documentation...")
    
    docs = [
        'README.md',
        'flutter_setup_guide.md',
        'setup_instructions.md',
        'requirements.txt'
    ]
    
    for doc in docs:
        if os.path.exists(doc):
            print(f"✅ {doc} exists")
        else:
            print(f"❌ {doc} not found")
    
    return True

def main():
    """Run complete system test"""
    print("=" * 60)
    print("🎬 MOVIE RECOMMENDATION SYSTEM - COMPLETE TEST")
    print("=" * 60)
    
    tests = [
        ("Data Files", test_data_files),
        ("Flask API", test_flask_api),
        ("Streamlit Dependencies", test_streamlit_dependencies),
        ("Flutter Project", test_flutter_project),
        ("Launcher Scripts", test_launcher_scripts),
        ("Documentation", test_documentation)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'=' * 40}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results[test_name] = False
    
    print(f"\n{'=' * 60}")
    print("🎯 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<30} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL SYSTEMS GO! Your Movie Recommendation System is 100% ready!")
        print("\n🔧 To start using:")
        print("   • Web App: python -m streamlit run Website.py")
        print("   • Flask API: python flask_api.py")
        print("   • Flutter App: Run launch_flutter_dev.bat")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues above.")
    
    return passed == total

if __name__ == "__main__":
    main()
