# 🚀 Flutter Movie Recommendation App - Setup & Run Guide

## 📋 Prerequisites

Before starting, ensure you have:

- ✅ Android Studio installed with Flutter plugin
- ✅ Flutter SDK properly configured
- ✅ Android Virtual Device (AVD) created
- ✅ Python 3.7+ installed

## 🎯 Step-by-Step Setup

### Step 1: Start the Flask API Backend

```powershell
# Navigate to project root
cd "e:\Projects\Movie-Recomendation-System-using-ML"

# Start the Flask API (this runs on http://localhost:5000)
python flask_api.py
```

**✅ Expected Output:**
```
Movie data loaded successfully. Shape: (4806, 20)
Similarity matrix loaded successfully. Shape: (4806, 4806)
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 2: Open Android Studio

1. **Launch Android Studio**
2. **Open the Flutter project:**
   - Click "Open an Existing Project"
   - Navigate to: `e:\Projects\Movie-Recomendation-System-using-ML\Movie_recommend_App`
   - Click "OK"

### Step 3: Setup Android Virtual Device

1. **Open AVD Manager:**
   - Tools → AVD Manager
   - Click "Create Virtual Device"

2. **Recommended Device Setup:**
   - **Device:** Pixel 6 Pro
   - **API Level:** 33 (Android 13)
   - **RAM:** 4GB
   - **Internal Storage:** 8GB

3. **Start the AVD**

### Step 4: Configure Flutter Dependencies

Open Terminal in Android Studio and run:

```bash
# Navigate to Flutter project
cd Movie_recommend_App

# Get Flutter dependencies
flutter pub get

# Verify Flutter installation
flutter doctor
```

### Step 5: Run the Flutter App

```bash
# Make sure you're in the Movie_recommend_App directory
flutter run
```

## 🌐 Network Configuration Details

### Why `10.0.2.2` for Android Emulator?

In `lib/main.dart`, the API base URL is set to `http://10.0.2.2:5000`:

```dart
static const String baseUrl = 'http://10.0.2.2:5000';
```

**Explanation:**

- `10.0.2.2` is a special IP address in Android emulator
- It maps to `localhost` (127.0.0.1) on your host machine
- This allows the Flutter app to communicate with your Flask API

### For Physical Android Device

If testing on a real Android device:

1. **Find your computer's IP address:**
   ```powershell
   ipconfig
   ```
   Look for "IPv4 Address" under your active network adapter

2. **Update the API URL in `main.dart`:**
   ```dart
   static const String baseUrl = 'http://YOUR_IP_ADDRESS:5000';
   ```

3. **Ensure both devices are on the same WiFi network**

## 🎮 Using the App

### Main Features

1. **Search Movies:**
   - Tap the search bar at the top
   - Type any movie name (e.g., "Avatar", "Avengers")
   - Select from autocomplete suggestions

2. **Get Recommendations:**
   - Tap "Get Recommendations" button
   - View 5 similar movies with details:
     - Movie poster
     - Title and rating
     - Release date and runtime
     - Overview/plot
     - Similarity percentage

3. **Movie Details:**
   - Each recommendation shows rich information
   - High-quality posters from TMDB API
   - Ratings, genres, and descriptions

## 🐛 Troubleshooting

### Issue 1: "Failed to connect to server"

**Symptoms:**
- App shows connection error
- No movie recommendations appear

**Solutions:**

1. **Check Flask API is running:**
   ```powershell
   # Test API manually
   curl http://localhost:5000/health
   ```

2. **Verify Android emulator network:**
   ```powershell
   # Test from emulator perspective
   curl http://10.0.2.2:5000/health
   ```

3. **Check Windows Firewall:**
   - Allow Python through Windows Firewall
   - Allow port 5000 for local connections

### Issue 2: Flutter build errors

**Solutions:**
```bash
# Clean Flutter project
flutter clean

# Get dependencies again
flutter pub get

# Restart Android Studio
```

### Issue 3: Android emulator not starting

**Solutions:**

1. **Enable Virtualization in BIOS**
2. **Ensure Hyper-V is disabled** (for AMD processors)
3. **Check Android SDK is properly installed**
4. **Restart Android Studio as Administrator**

### Issue 4: Movies not found

**Solutions:**
- Try exact movie titles: "Avatar", "Titanic", "The Dark Knight"
- Check spelling carefully
- Some movies might not be in the dataset

## 📱 Testing Workflow

### Complete Test Sequence

1. **Start Flask API** → Should see "Running on http://127.0.0.1:5000"
2. **Start Android Emulator** → Wait for full boot
3. **Run Flutter app** → `flutter run`
4. **Test search** → Type "Avatar"
5. **Get recommendations** → Should see 5 movie cards
6. **Verify images** → Movie posters should load

### Expected Performance

- **App startup:** 3-5 seconds
- **Search response:** Instant (local data)
- **Recommendations:** 1-2 seconds (API call)
- **Image loading:** 2-3 seconds (TMDB API)

## 🎯 Advanced Tips

### Hot Reload During Development

- Press `r` in terminal for hot reload
- Press `R` for hot restart
- Press `q` to quit

### Debugging Network Issues

```bash
# Enable Flutter network logging
flutter run --verbose
```

### Building for Release

```bash
# Build APK for testing
flutter build apk

# Build App Bundle for Play Store
flutter build appbundle
```

## 🔧 VS Code Alternative

If you prefer VS Code:

1. **Install Extensions:**
   - Flutter
   - Dart

2. **Open project:**
   ```bash
   code Movie_recommend_App
   ```

3. **Run with F5** or:
   ```bash
   flutter run
   ```

## 📊 API Endpoints Reference

Your Flutter app uses these Flask API endpoints:

- **Health Check:** `GET /health`
- **Search Movies:** `GET /search?q=movie_name`
- **Get All Movies:** `GET /movies`
- **Get Recommendations:** `POST /recommend` with `{"title": "Movie Name"}`

## 🎉 Success Checklist

- [ ] Flask API running on port 5000
- [ ] Android emulator started and responsive
- [ ] Flutter dependencies installed (`flutter pub get`)
- [ ] App successfully runs (`flutter run`)
- [ ] Search functionality works
- [ ] Recommendations display with images
- [ ] No network connection errors

---

**🎬 Your Flutter Movie Recommendation app is now ready! Start by searching for your favorite movie and discover similar films!** 📱✨

**💡 Pro Tip:** Keep the Flask API running in one terminal while developing the Flutter app in Android Studio for the best experience!
