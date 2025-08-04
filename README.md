# 🎬 Movie Recommendation System using Machine Learning

A sophisticated movie recommendation system built with Python and Machine Learning that suggests movies based on content similarity. The system uses **Content-Based Filtering** with **Natural Language Processing** and **Cosine Similarity** to provide personalized movie recommendations.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3%2B-orange)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

- **🎯 Content-Based Filtering**: Recommends movies based on genre, cast, director, and keywords
- **🔍 Smart Search**: Search for movies with auto-complete functionality
- **🎨 Modern UI**: Beautiful, responsive interface built with Streamlit
- **📊 Movie Details**: Get ratings, release dates, runtime, and overview for each recommendation
- **⚡ Fast Performance**: Optimized with caching for quick responses
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices
- **🎭 Rich Movie Information**: Integration with TMDB API for posters and metadata

## 🛠️ Technology Stack

- **Backend**: Python, Pandas, NumPy
- **Machine Learning**: Scikit-learn, Natural Language Processing
- **Frontend**: Streamlit
- **API Integration**: The Movie Database (TMDB) API
- **Data Processing**: Pickle for model persistence
- **Similarity Calculation**: Cosine Similarity with TF-IDF Vectorization

## 📁 Project Structure

```
Movie-Recommendation-System-using-ML/
│
├── 📄 Website.py                           # Main Streamlit application
├── 📓 movie_recomended_with_UI.ipynb      # Data processing & model training
├── 📓 ensemble_learning.ipynb             # Ensemble learning experiments
├── 🗃️ movie_dict.pkl                      # Processed movie data
├── 🗃️ movies.pkl                          # Movie features dataset
├── 🗃️ similarity.pkl                      # Cosine similarity matrix
├── 📋 requirements.txt                    # Python dependencies
├── 📖 README.md                           # Project documentation
└── 🚀 setup_instructions.md               # Setup guide
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Internet connection (for TMDB API)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/abdullahjave/Movie-Recomendation-System-using-ML.git
   cd Movie-Recomendation-System-using-ML
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate required data files** (if not present)
   ```bash
   # Run the Jupyter notebook to generate pickle files
   jupyter notebook movie_recomended_with_UI.ipynb
   # Execute all cells to generate: similarity.pkl, movies.pkl, movie_dict.pkl
   ```

4. **Run the application**
   ```bash
   streamlit run Website.py
   ```

5. **Open your browser** and navigate to `http://localhost:8501`

## 📊 How It Works

### 1. Data Preprocessing
- **Data Source**: TMDB 5000 Movie Dataset
- **Feature Engineering**: Combines genres, keywords, cast, crew, and overview
- **Text Processing**: Removes spaces, converts to lowercase, handles missing values

### 2. Feature Extraction
- **TF-IDF Vectorization**: Converts text features into numerical vectors
- **Dimensionality**: Creates high-dimensional feature space
- **Normalization**: L2 normalization for cosine similarity

### 3. Similarity Calculation
```python
# Cosine Similarity Formula
similarity = cosine_similarity(tfidf_matrix)
```

### 4. Recommendation Algorithm
```python
def recommend(movie_title):
    # Find movie index
    movie_index = movies[movies['title'] == movie_title].index[0]
    
    # Calculate similarity scores
    distances = similarity[movie_index]
    
    # Sort and get top 5 similar movies
    movies_list = sorted(list(enumerate(distances)), 
                        reverse=True, key=lambda x: x[1])[1:6]
    
    return recommended_movies
```

## 🎯 Usage Examples

### Basic Usage
1. **Select a Movie**: Choose from the dropdown or use the search feature
2. **Get Recommendations**: Click "Get Recommendations" button
3. **Explore Results**: Browse through 5 personalized movie suggestions

### Advanced Features
- **Search Functionality**: Type partial movie names for quick search
- **Movie Details**: View ratings, release year, and runtime
- **Feedback System**: Rate the quality of recommendations

## 📈 Performance Metrics

- **Dataset Size**: 5,000 movies
- **Feature Dimensions**: ~5,000 features after TF-IDF
- **Response Time**: < 2 seconds for recommendations
- **Accuracy**: Content-based similarity matching
- **Coverage**: 100% of dataset movies

## 🔧 Configuration

### TMDB API Setup
1. Get API key from [TMDB](https://www.themoviedb.org/settings/api)
2. Replace the API key in `Website.py`:
   ```python
   api_key = "your_api_key_here"
   ```

### Customization Options
- **Number of Recommendations**: Modify the slice `[1:6]` in recommendation function
- **Feature Weights**: Adjust TF-IDF parameters in the notebook
- **UI Themes**: Customize CSS in `Website.py`

## 🧪 Model Details

### Content-Based Filtering
- **Algorithm**: TF-IDF + Cosine Similarity
- **Features Used**:
  - Movie Genres
  - Cast Members (Top 3)
  - Director
  - Keywords
  - Movie Overview

### Feature Engineering
```python
# Combine all features into tags
movies['tags'] = movies['overview'] + movies['genres'] + 
                movies['keywords'] + movies['cast'] + movies['crew']
```

### Similarity Matrix
- **Size**: 5000 x 5000
- **Storage**: Compressed pickle format
- **Memory**: ~200MB RAM usage

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **TMDB**: For providing the movie database and API
- **Kaggle**: For the TMDB 5000 Movie Dataset
- **Streamlit**: For the amazing web app framework
- **Scikit-learn**: For machine learning algorithms

## 📞 Contact

**Abdullah Javed**
- GitHub: [@abdullahjave](https://github.com/abdullahjave)
- Email: abdjaved634@gmail.com
- LinkedIn:[https://www.linkedin.com/in/abdullah-javed-a1b316310/](https://www.linkedin.com/in/abdullah-javed-a1b316310/)

## 🔮 Future Enhancements

- [ ] **Hybrid Filtering**: Combine content-based with collaborative filtering
- [ ] **Deep Learning**: Implement neural networks for better recommendations
- [ ] **User Profiles**: Add user registration and preference learning
- [ ] **Real-time Updates**: Dynamic model updates with new movies
- [ ] **Multi-language Support**: Support for international movies
- [ ] **Advanced Analytics**: User behavior tracking and recommendation metrics
- [ ] **Mobile App**: React Native mobile application
- [ ] **API Endpoint**: RESTful API for third-party integrations

---

⭐ **If you found this project helpful, please give it a star!** ⭐ 
