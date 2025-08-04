from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import pickle
import requests
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})  # Enable CORS for Flutter app

# Load data using pickle files (enhanced version)
try:
    # Try to load from pickle files first
    with open('movie_dict.pkl', 'rb') as f:
        movie_dict = pickle.load(f)
    movies_df = pd.DataFrame(movie_dict)
    
    with open('similarity.pkl', 'rb') as f:
        similarity = pickle.load(f)
    
    print("✅ Loaded data from pickle files")
    
except FileNotFoundError:
    print("⚠️ Pickle files not found, loading from CSV...")
    # Fallback to CSV loading
    movies = pd.read_csv("tmdb_5000_movies.csv")
    credits = pd.read_csv("tmdb_5000_credits.csv")
    
    # Merge datasets
    movies = movies.merge(credits, on='title')
    movies_df = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']].dropna()
    
    # Preprocessing function
    def preprocess_text(data):
        return str(data['genres']) + " " + str(data['keywords']) + " " + str(data['cast']) + " " + str(data['crew'])
    
    movies_df['tags'] = movies_df.apply(preprocess_text, axis=1)
    
    # Text vectorization and similarity
    vectorizer = CountVectorizer(max_features=5000, stop_words='english')
    vectors = vectorizer.fit_transform(movies_df['tags']).toarray()
    similarity = cosine_similarity(vectors)
    
    print("✅ Generated similarity matrix from CSV")

# Add request logging middleware
@app.before_request
def log_request_info():
    print(f"📥 Incoming request: {request.method} {request.url}")
    print(f"   Headers: {dict(request.headers)}")
    if request.data:
        print(f"   Body: {request.data}")

@app.after_request
def log_response_info(response):
    print(f"📤 Response: {response.status_code}")
    return response

def fetch_poster(movie_id):
    """Fetch movie poster from TMDB API"""
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=75b3c80c1a67275c04868a92f6f50a4b",
            timeout=5
        )
        data = response.json()
        if "poster_path" in data and data["poster_path"]:
            return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
        else:
            return None
    except:
        return None

def fetch_movie_details(movie_id):
    """Fetch additional movie details from TMDB API"""
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=75b3c80c1a67275c04868a92f6f50a4b",
            timeout=5
        )
        data = response.json()
        return {
            "rating": data.get("vote_average", "N/A"),
            "release_date": data.get("release_date", "N/A"),
            "overview": data.get("overview", "No overview available")[:200] + "..." if data.get("overview") else "No overview available",
            "runtime": data.get("runtime", "N/A"),
            "genres": [genre["name"] for genre in data.get("genres", [])]
        }
    except:
        return {
            "rating": "N/A",
            "release_date": "N/A",
            "overview": "Details unavailable",
            "runtime": "N/A",
            "genres": []
        }

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Movie Recommendation API is running!'})

@app.route('/movies', methods=['GET'])
def get_movies():
    """Get all available movies"""
    try:
        movies_list = movies_df['title'].tolist()
        return jsonify({
            'movies': movies_list,
            'count': len(movies_list)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/search', methods=['GET'])
def search_movies():
    """Search movies by title"""
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({'error': 'Query parameter is required'}), 400
        
        # Case insensitive search
        filtered_movies = movies_df[movies_df['title'].str.contains(query, case=False, na=False)]
        movies_list = filtered_movies['title'].tolist()
        
        return jsonify({
            'movies': movies_list,
            'count': len(movies_list),
            'query': query
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/recommend', methods=['POST'])
def recommend():
    """Get movie recommendations"""
    try:
        data = request.json
        movie_title = data.get('title')
        
        if movie_title is None or movie_title == "":
            return jsonify({'error': 'Movie title is required'}), 400
        
        # Find movie in database
        movie_matches = movies_df[movies_df['title'].str.contains(movie_title, case=False, na=False)]
        
        if movie_matches.empty:
            return jsonify({'error': f'Movie "{movie_title}" not found'}), 404
        
        # Get the first match
        movie_index = movie_matches.index[0]
        movie_id = movies_df.iloc[movie_index]['movie_id']
        actual_title = movies_df.iloc[movie_index]['title']
        
        # Calculate similarity
        distances = similarity[movie_index]
        movie_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        recommendations = []
        for i, score in movie_indices:
            movie_data = movies_df.iloc[i]
            movie_id = movie_data['movie_id']
            title = movie_data['title']
            
            # Get poster and details
            poster_url = fetch_poster(movie_id)
            details = fetch_movie_details(movie_id)
            
            recommendations.append({
                'title': title,
                'movie_id': int(movie_id),
                'similarity_score': float(score),
                'poster_url': poster_url,
                'rating': details['rating'],
                'release_date': details['release_date'],
                'overview': details['overview'],
                'runtime': details['runtime'],
                'genres': details['genres']
            })
        
        return jsonify({
            'input_movie': actual_title,
            'recommendations': recommendations,
            'count': len(recommendations)
        })
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

if __name__ == '__main__':
    print("🎬 Starting Movie Recommendation API...")
    print(f"📊 Loaded {len(movies_df)} movies")
    print("🚀 Server running on http://localhost:5000")
    print("📱 Flutter app can connect to: http://10.0.2.2:5000 (Android Emulator)")
    print("📱 Flutter app can connect to: http://localhost:5000 (iOS Simulator)")
    print("🔧 Debug mode enabled")
    
    # Add request logging
    import logging
    logging.basicConfig(level=logging.INFO)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()
