# 🚀 Setup Instructions for Movie Recommendation System

This guide will help you set up and run the Movie Recommendation System on your local machine.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher** - [Download Python](https://python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads/)
- **pip** (comes with Python)

## 🔧 Step-by-Step Installation

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/abdullahjave/Movie-Recomendation-System-using-ML.git

# Navigate to the project directory
cd Movie-Recomendation-System-using-ML
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv movie_recommender_env

# Activate virtual environment
# On Windows:
movie_recommender_env\Scripts\activate
# On macOS/Linux:
source movie_recommender_env/bin/activate
```

### Step 3: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

### Step 4: Download Dataset (if needed)

If the pickle files are not present, you'll need to download the TMDB dataset:

1. Download the TMDB 5000 Movie Dataset from [Kaggle](https://www.kaggle.com/tmdb/tmdb-movie-metadata)
2. Place the following files in the project directory:
   - `tmdb_5000_movies.csv`
   - `tmdb_5000_credits.csv`

### Step 5: Generate Required Files

If `similarity.pkl` is missing, run the Jupyter notebook:

```bash
# Start Jupyter Notebook
jupyter notebook

# Open and run movie_recomended_with_UI.ipynb
# Execute all cells to generate the required pickle files
```

### Step 6: Run the Application

```bash
# Start the Streamlit application
streamlit run Website.py
```

The application will open in your default web browser at `http://localhost:8501`

## ⚙️ Configuration

### TMDB API Key (Optional but Recommended)

To get movie posters and additional details:

1. Create a free account at [TMDB](https://www.themoviedb.org/)
2. Go to Settings > API and request an API key
3. Replace the API key in `Website.py`:
   ```python
   api_key = "your_api_key_here"
   ```

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. Missing Pickle Files
**Error**: `FileNotFoundError: [Errno 2] No such file or directory: 'similarity.pkl'`

**Solution**: Run the Jupyter notebook to generate the required files:
```bash
jupyter notebook movie_recomended_with_UI.ipynb
```

#### 2. Module Not Found Error
**Error**: `ModuleNotFoundError: No module named 'streamlit'`

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

#### 3. Port Already in Use
**Error**: `Port 8501 is already in use`

**Solution**: Use a different port:
```bash
streamlit run Website.py --server.port 8502
```

#### 4. API Rate Limiting
**Error**: Movie posters not loading

**Solution**: 
- Check your internet connection
- Verify TMDB API key is valid
- Wait a few minutes and try again

### Performance Issues

#### Slow Loading
- Ensure all pickle files are present
- Check your internet connection for API calls
- Consider using a faster machine for large datasets

#### Memory Issues
- Close other applications
- Increase virtual memory
- Use a machine with at least 4GB RAM

## 📁 File Structure After Setup

```
Movie-Recommendation-System-using-ML/
│
├── Website.py                              # ✅ Main application
├── movie_recomended_with_UI.ipynb         # ✅ Data processing notebook
├── ensemble_learning.ipynb                # ✅ ML experiments
├── requirements.txt                        # ✅ Dependencies
├── README.md                              # ✅ Documentation
├── setup_instructions.md                  # ✅ This file
│
├── movie_dict.pkl                         # ✅ Generated from notebook
├── movies.pkl                             # ✅ Generated from notebook
├── similarity.pkl                         # ✅ Generated from notebook
│
└── movie_recommender_env/                 # ✅ Virtual environment (optional)
```

## 🎯 Verification

To verify everything is working correctly:

1. **Check Dependencies**:
   ```bash
   pip list
   ```

2. **Test Import**:
   ```python
   import streamlit as st
   import pandas as pd
   import pickle
   print("All imports successful!")
   ```

3. **Check Files**:
   ```python
   import os
   required_files = ['movie_dict.pkl', 'movies.pkl', 'similarity.pkl']
   for file in required_files:
       if os.path.exists(file):
           print(f"✅ {file} found")
       else:
           print(f"❌ {file} missing")
   ```

## 🔄 Updating the Project

To get the latest updates:

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade
```

## 📞 Need Help?

If you encounter any issues:

1. Check this troubleshooting guide
2. Look at the [GitHub Issues](https://github.com/abdullahjave/Movie-Recomendation-System-using-ML/issues)
3. Create a new issue with:
   - Error message
   - Your operating system
   - Python version
   - Steps to reproduce

## 🎉 Success!

If you see the Streamlit interface with the movie recommender, congratulations! You've successfully set up the project.

Enjoy discovering new movies! 🍿🎬
