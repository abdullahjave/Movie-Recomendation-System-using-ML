# 📱 Flutter Movie Recommendation App Setup Guide

## 🚀 Quick Start

### Prerequisites
- ✅ Flutter SDK installed
- ✅ Android Studio or VS Code
- ✅ Android Emulator or physical device
- ✅ Python Flask API running

### 1. Setup Flutter Dependencies
```bash
cd reel_recommend
flutter pub get
```

### 2. Start the Flask API
```bash
# In the root project directory
python flask_api.py
```

### 3. Run the Flutter App
```bash
# In the reel_recommend directory
flutter run
```

## 🔧 Detailed Setup Instructions

### Flutter Environment Setup

#### Install Flutter (if not already installed)
1. Download Flutter SDK from [flutter.dev](https://flutter.dev/docs/get-started/install)
2. Extract and add to PATH
3. Run `flutter doctor` to verify installation

#### Android Studio Setup
1. Install Android Studio
2. Install Flutter and Dart plugins
3. Create/start an Android Virtual Device (AVD)

### Project Structure
```
reel_recommend/
├── lib/
│   └── main.dart          # Main Flutter app
├── android/               # Android-specific files
├── ios/                   # iOS-specific files  
├── pubspec.yaml          # Dependencies
└── README.md             # This file
```

### Dependencies Used
- `http: ^1.1.0` - API calls
- `cached_network_image: ^3.3.0` - Image caching
- `flutter_spinkit: ^5.2.0` - Loading animations

## 🌐 API Configuration

### Network Setup for Different Environments

#### Android Emulator
- **API Base URL**: `http://10.0.2.2:5000`
- **Reason**: `10.0.2.2` is the special IP that maps to localhost on the host machine

#### iOS Simulator  
- **API Base URL**: `http://localhost:5000`
- **Reason**: iOS simulator can directly access localhost

#### Physical Device
- **API Base URL**: `http://YOUR_COMPUTER_IP:5000`
- **Find your IP**: 
  - Windows: `ipconfig`
  - Mac/Linux: `ifconfig`

### API Endpoints

#### 1. Health Check
```http
GET /health
Response: {"status": "healthy", "message": "Movie Recommendation API is running!"}
```

#### 2. Get All Movies
```http
GET /movies
Response: {"movies": ["Movie 1", "Movie 2", ...], "count": 5000}
```

#### 3. Search Movies
```http
GET /search?q=avengers
Response: {"movies": ["Avengers", "Avengers: Age of Ultron", ...], "count": 5, "query": "avengers"}
```

#### 4. Get Recommendations
```http
POST /recommend
Body: {"title": "Avatar"}
Response: {
  "input_movie": "Avatar",
  "recommendations": [
    {
      "title": "Guardians of the Galaxy",
      "movie_id": 118340,
      "similarity_score": 0.85,
      "poster_url": "https://image.tmdb.org/t/p/w500/...",
      "rating": 8.1,
      "release_date": "2014-07-30",
      "overview": "A group of intergalactic criminals...",
      "runtime": 121,
      "genres": ["Action", "Adventure", "Comedy"]
    }
  ],
  "count": 5
}
```

## 🎨 App Features

### Current Features
- ✅ Movie search with autocomplete
- ✅ Get 5 movie recommendations
- ✅ Display movie posters, ratings, and details
- ✅ Beautiful dark theme UI
- ✅ Loading animations
- ✅ Error handling
- ✅ Similarity percentage display

### UI Components
- **Search Bar**: Auto-complete movie search
- **Movie Cards**: Rich movie information display
- **Loading States**: Smooth loading animations
- **Error States**: User-friendly error messages

## 🚨 Troubleshooting

### Common Issues

#### 1. "Failed to connect to server"
**Solutions**:
- Ensure Flask API is running (`python flask_api.py`)
- Check network configuration (10.0.2.2 for Android emulator)
- Verify firewall settings

#### 2. "Movie not found"
**Solutions**:
- Try different movie titles
- Check spelling
- Use exact movie titles from the database

#### 3. Flutter pub get fails
**Solutions**:
```bash
flutter clean
flutter pub get
```

#### 4. Images not loading
**Solutions**:
- Check internet connection
- TMDB API might be rate-limited
- Some movies might not have poster images

### Network Debugging

#### Test API manually:
```bash
# Test health endpoint
curl http://localhost:5000/health

# Test recommendations
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"title": "Avatar"}'
```

#### Flutter Network Debugging:
- Enable network logging in Flutter
- Check Android/iOS network permissions
- Use device logs to debug connection issues

## 🔧 Development Commands

### Essential Flutter Commands
```bash
# Get dependencies
flutter pub get

# Run on connected device
flutter run

# Run in debug mode
flutter run --debug

# Run in release mode  
flutter run --release

# Build APK
flutter build apk

# Check for issues
flutter doctor

# Clean project
flutter clean
```

### Hot Reload
- **Hot Reload**: `r` (preserves app state)
- **Hot Restart**: `R` (full restart)
- **Quit**: `q`

## 📱 Testing on Different Devices

### Android Emulator
1. Start Android Studio
2. Open AVD Manager
3. Create/Start virtual device
4. Run `flutter run`

### Physical Android Device
1. Enable Developer Options
2. Enable USB Debugging
3. Connect via USB
4. Run `flutter run`
5. Update API URL to your computer's IP

### iOS Simulator (Mac only)
1. Install Xcode
2. Start iOS Simulator
3. Run `flutter run`

## 🎯 Performance Tips

### App Performance
- Images are cached for better performance
- Lazy loading for movie lists
- Optimized API calls

### Development Performance  
- Use hot reload during development
- Profile app performance with Flutter Inspector
- Monitor memory usage

## 🔄 Future Enhancements

### Planned Features
- [ ] Movie favorites/watchlist
- [ ] User ratings and reviews
- [ ] Movie trailers integration
- [ ] Advanced filtering options
- [ ] Offline mode
- [ ] Social sharing
- [ ] User profiles

### Technical Improvements
- [ ] State management (Provider/Bloc)
- [ ] Local database (SQLite)
- [ ] Push notifications
- [ ] Analytics integration
- [ ] Crash reporting

## 📞 Support

### Getting Help
- Check Flutter documentation: [flutter.dev](https://flutter.dev/docs)
- Stack Overflow: flutter tag
- GitHub Issues: Create issues in this repository

### Development Resources
- [Flutter Cookbook](https://flutter.dev/docs/cookbook)
- [Dart Language Tour](https://dart.dev/guides/language/language-tour)
- [Material Design](https://material.io/design)

---

**🎬 Happy coding! Your Flutter Movie Recommendation app is ready to discover amazing movies!** 📱✨
