import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Reel Recommend',
      theme: ThemeData(
        primarySwatch: Colors.deepPurple,
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF0D1117),
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF161B22),
          elevation: 0,
        ),
        cardTheme: CardThemeData(
          color: const Color(0xFF21262D),
          elevation: 4,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        ),
      ),
      home: MovieRecommendationScreen(),
    );
  }
}

class Movie {
  final String title;
  final int movieId;
  final double similarityScore;
  final String? posterUrl;
  final dynamic rating;
  final String releaseDate;
  final String overview;
  final dynamic runtime;
  final List<dynamic> genres;

  Movie({
    required this.title,
    required this.movieId,
    required this.similarityScore,
    this.posterUrl,
    required this.rating,
    required this.releaseDate,
    required this.overview,
    required this.runtime,
    required this.genres,
  });

  factory Movie.fromJson(Map<String, dynamic> json) {
    return Movie(
      title: json['title'] ?? '',
      movieId: json['movie_id'] ?? 0,
      similarityScore: (json['similarity_score'] ?? 0.0).toDouble(),
      posterUrl: json['poster_url'],
      rating: json['rating'],
      releaseDate: json['release_date'] ?? '',
      overview: json['overview'] ?? '',
      runtime: json['runtime'],
      genres: json['genres'] ?? [],
    );
  }
}

class MovieRecommendationScreen extends StatefulWidget {
  @override
  _MovieRecommendationScreenState createState() =>
      _MovieRecommendationScreenState();
}

class _MovieRecommendationScreenState
    extends State<MovieRecommendationScreen> {
  final TextEditingController _controller = TextEditingController();
  List<Movie> _recommendations = [];
  List<String> _allMovies = [];
  List<String> _filteredMovies = [];
  String _error = '';
  bool _isLoading = false;
  bool _isSearching = false;
  String _inputMovie = '';

  // For Android Emulator (most common):
  static const String baseUrl = 'http://10.0.2.2:5000';

// For Physical Android Device:
// static const String baseUrl = 'http://192.168.1.4:5000';

// For iOS Simulator:
// static const String baseUrl = 'http://localhost:5000';

  @override
  void initState() {
    super.initState();
    _loadAllMovies();
    _controller.addListener(_onSearchChanged);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _onSearchChanged() {
    final query = _controller.text.toLowerCase();
    if (query.isEmpty) {
      setState(() {
        _filteredMovies = [];
        _isSearching = false;
      });
    } else {
      setState(() {
        _filteredMovies = _allMovies
            .where((movie) => movie.toLowerCase().contains(query))
            .take(10)
            .toList();
        _isSearching = true;
      });
    }
  }

  Future<void> _loadAllMovies() async {
    try {
      print('🔄 Attempting to load movies from: $baseUrl/movies');
      final response = await http.get(
        Uri.parse('$baseUrl/movies'),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      ).timeout(Duration(seconds: 10)); // Added timeout

      print('📡 Response status: ${response.statusCode}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        setState(() {
          _allMovies = List<String>.from(data['movies']);
        });
        print('✅ Successfully loaded ${_allMovies.length} movies');
      } else {
        print('❌ Failed to load movies: ${response.statusCode}');
      }
    } catch (e) {
      print('💥 Error loading movies: $e');
      // Show user-friendly error
      setState(() {
        _error = 'Cannot connect to server. Please check if the Flask API is running.';
      });
    }
  }

  Future<void> fetchRecommendations(String title) async {
    if (title.trim().isEmpty) {
      setState(() {
        _error = 'Please enter a movie title';
      });
      return;
    }

    setState(() {
      _isLoading = true;
      _error = '';
      _recommendations = [];
      _isSearching = false;
    });

    try {
      print('🔄 Fetching recommendations for: $title');
      print('🌐 Using URL: $baseUrl/recommend');

      final response = await http.post(
        Uri.parse('$baseUrl/recommend'),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: json.encode({'title': title}),
      ).timeout(Duration(seconds: 15)); // Added timeout

      print('📡 Response status: ${response.statusCode}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        setState(() {
          _inputMovie = data['input_movie'];
          _recommendations = (data['recommendations'] as List)
              .map((item) => Movie.fromJson(item))
              .toList();
          _error = '';
          _isLoading = false;
        });
        print('✅ Successfully loaded ${_recommendations.length} recommendations');
      } else {
        final errorData = json.decode(response.body);
        setState(() {
          _error = errorData['error'] ?? 'Movie not found!';
          _recommendations = [];
          _isLoading = false;
        });
        print('❌ Error response: ${errorData['error']}');
      }
    } catch (e) {
      print('💥 Connection error: $e');
      setState(() {
        _error = 'Failed to connect to server.\n\nPlease check:\n• Flask API is running\n• Using correct URL: $baseUrl\n• Device is on same network';
        _recommendations = [];
        _isLoading = false;
      });
    }
  }

  Widget _buildSearchSuggestions() {
    if (!_isSearching || _filteredMovies.isEmpty) {
      return SizedBox.shrink();
    }

    return Container(
      margin: EdgeInsets.only(top: 8),
      decoration: BoxDecoration(
        color: Color(0xFF21262D),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: Colors.grey[700]!),
      ),
      child: ListView.builder(
        shrinkWrap: true,
        physics: NeverScrollableScrollPhysics(),
        itemCount: _filteredMovies.length,
        itemBuilder: (context, index) {
          return ListTile(
            title: Text(
              _filteredMovies[index],
              style: TextStyle(color: Colors.white),
            ),
            onTap: () {
              _controller.text = _filteredMovies[index];
              setState(() {
                _isSearching = false;
                _filteredMovies = [];
              });
              fetchRecommendations(_filteredMovies[index]);
            },
          );
        },
      ),
    );
  }

  Widget _buildMovieCard(Movie movie) {
    return Card(
      margin: EdgeInsets.symmetric(vertical: 8, horizontal: 16),
      child: Padding(
        padding: EdgeInsets.all(12),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Movie Poster
            Container(
              width: 80,
              height: 120,
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(8),
                color: Colors.grey[800],
              ),
              child: movie.posterUrl != null
                  ? ClipRRect(
                borderRadius: BorderRadius.circular(8),
                child: CachedNetworkImage(
                  imageUrl: movie.posterUrl!,
                  fit: BoxFit.cover,
                  placeholder: (context, url) => Center(
                    child: SpinKitFadingCircle(
                      color: Colors.deepPurple,
                      size: 20,
                    ),
                  ),
                  errorWidget: (context, url, error) => Icon(
                    Icons.movie,
                    color: Colors.grey,
                    size: 30,
                  ),
                ),
              )
                  : Icon(
                Icons.movie,
                color: Colors.grey,
                size: 30,
              ),
            ),
            SizedBox(width: 12),
            // Movie Details
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    movie.title,
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                  SizedBox(height: 4),
                  if (movie.rating != "N/A")
                    Row(
                      children: [
                        Icon(Icons.star, color: Colors.amber, size: 16),
                        SizedBox(width: 4),
                        Text(
                          '${movie.rating}/10',
                          style: TextStyle(color: Colors.grey[300]),
                        ),
                      ],
                    ),
                  SizedBox(height: 4),
                  if (movie.releaseDate.isNotEmpty && movie.releaseDate != "N/A")
                    Text(
                      'Released: ${movie.releaseDate.substring(0, 4)}',
                      style: TextStyle(color: Colors.grey[400], fontSize: 12),
                    ),
                  if (movie.runtime != "N/A")
                    Text(
                      'Runtime: ${movie.runtime} min',
                      style: TextStyle(color: Colors.grey[400], fontSize: 12),
                    ),
                  SizedBox(height: 4),
                  if (movie.genres.isNotEmpty)
                    Wrap(
                      spacing: 4,
                      children: movie.genres
                          .take(3)
                          .map((genre) => Container(
                        padding: EdgeInsets.symmetric(
                            horizontal: 6, vertical: 2),
                        decoration: BoxDecoration(
                          color: Colors.deepPurple.withOpacity(0.3),
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: Text(
                          genre.toString(),
                          style: TextStyle(
                            color: Colors.deepPurpleAccent,
                            fontSize: 10,
                          ),
                        ),
                      ))
                          .toList(),
                    ),
                  SizedBox(height: 8),
                  Text(
                    movie.overview,
                    style: TextStyle(color: Colors.grey[300], fontSize: 12),
                    maxLines: 3,
                    overflow: TextOverflow.ellipsis,
                  ),
                  SizedBox(height: 4),
                  Text(
                    'Match: ${(movie.similarityScore * 100).toStringAsFixed(1)}%',
                    style: TextStyle(
                      color: Colors.green,
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  // 🔧 ADDED: Connection Status Widget
  Widget _buildConnectionStatus() {
    return Container(
      margin: EdgeInsets.all(16),
      padding: EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.blue.withOpacity(0.1),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: Colors.blue.withOpacity(0.3)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(Icons.info_outline, color: Colors.blue, size: 16),
              SizedBox(width: 8),
              Text(
                'Connection Info',
                style: TextStyle(
                  color: Colors.blue,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
          SizedBox(height: 8),
          Text(
            'API URL: $baseUrl',
            style: TextStyle(color: Colors.grey[400], fontSize: 12),
          ),
          Text(
            'Movies loaded: ${_allMovies.length}',
            style: TextStyle(color: Colors.grey[400], fontSize: 12),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: [
            Icon(Icons.movie_filter, color: Colors.deepPurpleAccent),
            SizedBox(width: 8),
            Text(
              'Reel Recommend',
              style: TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 22,
                color: Colors.white,
              ),
            ),
          ],
        ),
        centerTitle: false,
        elevation: 0,
        actions: [
          // 🔧 ADDED: Debug info button
          IconButton(
            icon: Icon(Icons.info_outline),
            onPressed: () {
              showDialog(
                context: context,
                builder: (context) => AlertDialog(
                  backgroundColor: Color(0xFF21262D),
                  title: Text('Connection Info', style: TextStyle(color: Colors.white)),
                  content: Column(
                    mainAxisSize: MainAxisSize.min,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('API URL: $baseUrl', style: TextStyle(color: Colors.grey[300])),
                      Text('Movies loaded: ${_allMovies.length}', style: TextStyle(color: Colors.grey[300])),
                      SizedBox(height: 8),
                      Text('Troubleshooting:', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                      Text('• Make sure Flask API is running', style: TextStyle(color: Colors.grey[400], fontSize: 12)),
                      Text('• Check network connection', style: TextStyle(color: Colors.grey[400], fontSize: 12)),
                      Text('• Verify correct URL for your device', style: TextStyle(color: Colors.grey[400], fontSize: 12)),
                    ],
                  ),
                  actions: [
                    TextButton(
                      onPressed: () => Navigator.pop(context),
                      child: Text('OK'),
                    ),
                  ],
                ),
              );
            },
          ),
        ],
      ),
      body: Column(
        children: [
          // Search Section
          Container(
            padding: EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Color(0xFF161B22),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.1),
                  blurRadius: 4,
                  offset: Offset(0, 2),
                ),
              ],
            ),
            child: Column(
              children: [
                TextField(
                  controller: _controller,
                  decoration: InputDecoration(
                    filled: true,
                    fillColor: Color(0xFF21262D),
                    labelText: 'Search for a movie...',
                    labelStyle: TextStyle(color: Colors.grey[400]),
                    prefixIcon: Icon(Icons.search, color: Colors.deepPurpleAccent),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: BorderSide.none,
                    ),
                    focusedBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: BorderSide(color: Colors.deepPurpleAccent, width: 2),
                    ),
                  ),
                  style: TextStyle(color: Colors.white),
                  onSubmitted: (value) => fetchRecommendations(value),
                ),
                SizedBox(height: 12),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: _isLoading
                        ? null
                        : () => fetchRecommendations(_controller.text),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.deepPurple,
                      padding: EdgeInsets.symmetric(vertical: 16),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                      elevation: 4,
                    ),
                    child: _isLoading
                        ? SpinKitThreeBounce(
                      color: Colors.white,
                      size: 20,
                    )
                        : Text(
                      'Get Recommendations',
                      style: TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
                        fontSize: 16,
                      ),
                    ),
                  ),
                ),
                _buildSearchSuggestions(),
              ],
            ),
          ),

          // Content Section
          Expanded(
            child: _isLoading
                ? Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  SpinKitFadingCircle(
                    color: Colors.deepPurple,
                    size: 50,
                  ),
                  SizedBox(height: 16),
                  Text(
                    'Finding amazing movies for you...',
                    style: TextStyle(color: Colors.grey[400]),
                  ),
                ],
              ),
            )
                : _error.isNotEmpty
                ? Center(
              child: SingleChildScrollView(
                padding: EdgeInsets.all(16),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(
                      Icons.error_outline,
                      color: Colors.redAccent,
                      size: 64,
                    ),
                    SizedBox(height: 16),
                    Text(
                      _error,
                      style: TextStyle(
                        color: Colors.redAccent,
                        fontSize: 14,
                      ),
                      textAlign: TextAlign.center,
                    ),
                    SizedBox(height: 16),
                    ElevatedButton(
                      onPressed: () {
                        setState(() {
                          _error = '';
                        });
                        _loadAllMovies(); // Retry loading movies
                      },
                      child: Text('Try Again'),
                    ),
                    SizedBox(height: 16),
                    _buildConnectionStatus(),
                  ],
                ),
              ),
            )
                : _recommendations.isNotEmpty
                ? Column(
              children: [
                if (_inputMovie.isNotEmpty)
                  Container(
                    width: double.infinity,
                    padding: EdgeInsets.all(16),
                    margin: EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        colors: [Colors.deepPurple, Colors.purple],
                      ),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Column(
                      children: [
                        Icon(Icons.movie_creation,
                            color: Colors.white, size: 32),
                        SizedBox(height: 8),
                        Text(
                          'Movies similar to:',
                          style: TextStyle(
                            color: Colors.white70,
                            fontSize: 14,
                          ),
                        ),
                        Text(
                          _inputMovie,
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                          textAlign: TextAlign.center,
                        ),
                      ],
                    ),
                  ),
                Expanded(
                  child: ListView.builder(
                    itemCount: _recommendations.length,
                    itemBuilder: (context, index) {
                      return _buildMovieCard(_recommendations[index]);
                    },
                  ),
                ),
              ],
            )
                : Center(
              child: SingleChildScrollView(
                padding: EdgeInsets.all(16),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(
                      Icons.movie_filter,
                      color: Colors.grey[600],
                      size: 64,
                    ),
                    SizedBox(height: 16),
                    Text(
                      'Welcome to Reel Recommend!',
                      style: TextStyle(
                        color: Colors.grey[300],
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    SizedBox(height: 8),
                    Text(
                      'Search for a movie to get personalized recommendations',
                      style: TextStyle(
                        color: Colors.grey[500],
                        fontSize: 14,
                      ),
                      textAlign: TextAlign.center,
                    ),
                    SizedBox(height: 24),
                    _buildConnectionStatus(),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
