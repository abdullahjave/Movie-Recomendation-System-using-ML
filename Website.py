import streamlit as st
import pickle
import pandas as pd
import requests
import os
from datetime import datetime
import time


# Configure page
st.set_page_config(
    page_title="🎬 Movie Recommender System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #ff6b6b;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .subtitle {
        text-align: center;
        color: #4ecdc4;
        font-size: 1.2rem;
        margin-bottom: 3rem;
    }
    
    .movie-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .movie-card:hover {
        transform: translateY(-5px);
    }
    
    .movie-title {
        color: white;
        font-weight: bold;
        text-align: center;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    .stats-container {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .stat-item {
        text-align: center;
        color: white;
    }
    
    .recommendation-header {
        color: #ff6b6b;
        font-size: 1.5rem;
        font-weight: bold;
        text-align: center;
        margin: 2rem 0 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def check_internet_connection():
    """Check if internet connection is available for TMDB API"""
    try:
        response = requests.get("https://api.themoviedb.org/3", timeout=5)
        return True
    except (requests.RequestException, requests.exceptions.ConnectionError):
        return False


def fetch_poster(movie_id):
    """Fetch movie poster from TMDB API"""
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=75b3c80c1a67275c04868a92f6f50a4b",
            timeout=10
        )
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        if "poster_path" in data and data["poster_path"]:
            return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
        else:
            return "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTAwIiBoZWlnaHQ9Ijc1MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8cmVjdCB3aWR0aD0iNTAwIiBoZWlnaHQ9Ijc1MCIgZmlsbD0iIzMzMzMzMyIvPgogIDx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LWZhbWlseT0iQXJpYWwsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMjQiIGZpbGw9IndoaXRlIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkeT0iLjNlbSI+Tm8gSW1hZ2UgQXZhaWxhYmxlPC90ZXh0Pgo8L3N2Zz4="
    except (requests.RequestException, KeyError, ValueError, requests.exceptions.ConnectionError):
        return "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTAwIiBoZWlnaHQ9Ijc1MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8cmVjdCB3aWR0aD0iNTAwIiBoZWlnaHQ9Ijc1MCIgZmlsbD0iIzMzMzMzMyIvPgogIDx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LWZhbWlseT0iQXJpYWwsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMjQiIGZpbGw9IndoaXRlIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkeT0iLjNlbSI+Tm8gSW1hZ2UgQXZhaWxhYmxlPC90ZXh0Pgo8L3N2Zz4="


def fetch_movie_details(movie_id):
    """Fetch additional movie details from TMDB API"""
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=75b3c80c1a67275c04868a92f6f50a4b",
            timeout=10
        )
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return {
            "rating": data.get("vote_average", "N/A"),
            "release_date": data.get("release_date", "N/A"),
            "overview": data.get("overview", "No overview available")[:150] + "..." if data.get("overview") else "No overview available",
            "runtime": data.get("runtime", "N/A")
        }
    except (requests.RequestException, KeyError, ValueError, requests.exceptions.ConnectionError) as e:
        # Fallback for offline mode or API issues
        return {
            "rating": "N/A",
            "release_date": "N/A", 
            "overview": "Details unavailable (offline mode)",
            "runtime": "N/A"
        }


def recommend(movie):
    """Generate movie recommendations"""
    try:
        movie_index = movies[movies["title"] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_movies_posters = []
        movie_details = []
        
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            movie_title = movies.iloc[i[0]].title
            recommended_movies.append(movie_title)
            poster_url = fetch_poster(movie_id)
            recommended_movies_posters.append(poster_url)
            details = fetch_movie_details(movie_id)
            movie_details.append(details)
            
        return recommended_movies, recommended_movies_posters, movie_details
    except IndexError:
        return ["Movie not found. Please try again."], [], []


# Load movie data and similarity matrix
@st.cache_data
def load_data():
    try:
        movie_dict = pickle.load(open("movie_dict.pkl", "rb"))
        movies_df = pd.DataFrame(movie_dict)
        
        # Check if similarity.pkl exists, if not create a placeholder
        if os.path.exists("similarity.pkl"):
            similarity_matrix = pickle.load(open("similarity.pkl", "rb"))
        else:
            st.warning("⚠️ similarity.pkl not found. Please run the notebook to generate the similarity matrix.")
            similarity_matrix = None
            
        return movies_df, similarity_matrix
    except FileNotFoundError as e:
        st.error(f"❌ Required files not found: {e}")
        st.info("Please make sure you have run the Jupyter notebook to generate the required pickle files.")
        return None, None


# Load data
movies, similarity = load_data()

if movies is not None and similarity is not None:
    # Main header
    st.markdown('<h1 class="main-header">🎬 Movie Recommender System</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Discover your next favorite movie using Machine Learning!</p>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("📊 App Statistics")
        st.markdown(f"""
        <div class="stats-container">
            <div class="stat-item">
                <h3>{len(movies)}</h3>
                <p>Movies Available</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Connection status
        is_online = check_internet_connection()
        status_color = "🟢" if is_online else "🔴"
        status_text = "Online" if is_online else "Offline"
        st.markdown(f"**Connection Status:** {status_color} {status_text}")
        if not is_online:
            st.warning("⚠️ Working in offline mode. Movie posters and details may not be available.")
        
        st.header("ℹ️ About")
        st.info("""
        This Movie Recommender System uses **Content-Based Filtering** 
        with Machine Learning to suggest movies similar to your preferences.
        
        **Technology Stack:**
        - Python
        - Streamlit 
        - Scikit-learn
        - TMDB API
        """)
        
        st.header("🎯 How it works")
        st.markdown("""
        1. **Select** a movie you enjoyed
        2. **Click** the Recommend button
        3. **Discover** 5 similar movies
        4. **Enjoy** your personalized recommendations!
        """)

    # Main content
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("🔍 Select a Movie")
        
        # Search functionality
        search_term = st.text_input("🔍 Search for a movie:", placeholder="Type movie name...")
        
        if search_term:
            filtered_movies = movies[movies["title"].str.contains(search_term, case=False, na=False)]["title"].values
            if len(filtered_movies) > 0:
                selected_movie_name = st.selectbox("Select from search results:", filtered_movies)
            else:
                st.warning("No movies found matching your search.")
                selected_movie_name = st.selectbox("Or select from all movies:", movies["title"].values)
        else:
            selected_movie_name = st.selectbox("Select a movie:", movies["title"].values)
        
        # Recommendation button with animation
        if st.button("🎬 Get Recommendations", type="primary", use_container_width=True):
            with st.spinner("🔄 Finding amazing movies for you..."):
                time.sleep(1)  # Add a small delay for better UX
                names, posters, details = recommend(selected_movie_name)

                if posters and len(posters) > 0:  # If posters list is not empty
                    st.markdown('<div class="recommendation-header">🎯 Recommended Movies for You</div>', unsafe_allow_html=True)
                    
                    # Display recommendations in a more attractive format
                    cols = st.columns(5)
                    for idx, col in enumerate(cols):
                        with col:
                            st.markdown(f'<div class="movie-card">', unsafe_allow_html=True)
                            st.markdown(f'<div class="movie-title">{names[idx]}</div>', unsafe_allow_html=True)
                            st.image(posters[idx], use_container_width=True)
                            
                            # Add movie details
                            if idx < len(details):
                                detail = details[idx]
                                st.markdown(f"⭐ **Rating:** {detail['rating']}")
                                st.markdown(f"📅 **Year:** {detail['release_date'][:4] if detail['release_date'] != 'N/A' else 'N/A'}")
                                if detail['runtime'] != 'N/A':
                                    st.markdown(f"⏱️ **Runtime:** {detail['runtime']} min")
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Add success message
                    st.success("✅ Recommendations generated successfully!")
                    
                    # Add feedback section
                    st.markdown("---")
                    col1, col2, col3 = st.columns(3)
                    with col2:
                        st.markdown("**How did we do?**")
                        feedback = st.radio(
                            "Rate our recommendations:",
                            ["😍 Excellent", "😊 Good", "😐 Okay", "😞 Poor"],
                            horizontal=True
                        )
                        if feedback:
                            st.balloons()
                            st.success("Thank you for your feedback!")
                            
                else:
                    st.error("❌ " + names[0] if names else "❌ Error generating recommendations")

    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown("""
        <div style='text-align: center; color: #666;'>
            <p>Made with ❤️ using Streamlit & Machine Learning</p>
            <p>© 2025 Movie Recommender System</p>
        </div>
        """, unsafe_allow_html=True)

else:
    st.error("⚠️ Unable to load required data files. Please check that all pickle files are present.")
