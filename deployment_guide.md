# 🚀 Deployment Guide

This guide explains how to deploy your Movie Recommendation System to various platforms.

## 🌐 Deployment Options

### 1. Streamlit Cloud (Recommended - Free)

#### Prerequisites
- GitHub account
- All files committed to GitHub

#### Steps
1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Enhanced movie recommendation system"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `Website.py`
   - Click "Deploy"

3. **Configuration**:
   - Your app will be available at: `https://[your-app-name].streamlit.app`
   - Automatic updates when you push to GitHub

### 2. Heroku (Free Tier Available)

#### Prerequisites
- Heroku account
- Heroku CLI installed

#### Setup Files

Create `Procfile`:
```
web: streamlit run Website.py --server.port=$PORT --server.address=0.0.0.0
```

Create `runtime.txt`:
```
python-3.9.16
```

#### Deployment Steps
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-movie-recommender

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Open app
heroku open
```

### 3. Railway (Modern Platform)

#### Steps
1. Connect GitHub repository to Railway
2. Select your repository
3. Railway will auto-detect Streamlit
4. Add environment variables if needed
5. Deploy automatically

### 4. Docker Deployment

#### Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "Website.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Build and Run
```bash
# Build image
docker build -t movie-recommender .

# Run container
docker run -p 8501:8501 movie-recommender
```

### 5. Local Network Deployment

#### For Local Network Access
```bash
streamlit run Website.py --server.address=0.0.0.0 --server.port=8501
```
Access via: `http://[your-ip]:8501`

## ⚙️ Environment Variables

For production deployment, consider using environment variables:

```python
# In Website.py, replace:
api_key = os.environ.get('TMDB_API_KEY', 'your_default_key')
```

Add to your deployment platform:
- `TMDB_API_KEY=your_actual_api_key`

## 📊 Performance Optimization

### For Production
1. **Enable Caching**:
   ```python
   @st.cache_data(ttl=3600)  # Cache for 1 hour
   def load_data():
       # Your data loading code
   ```

2. **Optimize Pickle Files**:
   - Compress pickle files if needed
   - Consider using parquet for large datasets

3. **Memory Management**:
   - Monitor memory usage
   - Use pagination for large datasets

## 🔒 Security Considerations

1. **API Keys**:
   - Never commit API keys to GitHub
   - Use environment variables
   - Rotate keys regularly

2. **Rate Limiting**:
   - Implement request throttling
   - Cache API responses

3. **Input Validation**:
   - Sanitize user inputs
   - Validate movie selections

## 📱 Mobile Optimization

Add to your CSS:
```css
@media (max-width: 768px) {
    .main-header {
        font-size: 2rem;
    }
    
    .movie-card {
        margin: 0.2rem;
        padding: 0.5rem;
    }
}
```

## 🔍 Monitoring & Analytics

### Add Basic Analytics
```python
# Track usage
import time
import json

def log_recommendation(movie, recommendations):
    log_data = {
        'timestamp': time.time(),
        'input_movie': movie,
        'recommendations': recommendations
    }
    # Log to file or service
```

### Health Check Endpoint
```python
# Add to your app
def health_check():
    return {"status": "healthy", "timestamp": time.time()}
```

## 🚨 Troubleshooting Deployment

### Common Issues

1. **Memory Errors**:
   - Reduce similarity matrix size
   - Use sparse matrices
   - Implement lazy loading

2. **Slow Loading**:
   - Optimize pickle file sizes
   - Use CDN for static assets
   - Implement progressive loading

3. **API Rate Limits**:
   - Implement exponential backoff
   - Cache responses
   - Use multiple API keys

### Debug Commands
```bash
# Check logs
streamlit run Website.py --logger.level=debug

# Memory profiling
pip install memory-profiler
python -m memory_profiler Website.py
```

## 📈 Scaling Considerations

### For High Traffic
1. **Use Load Balancer**
2. **Implement Redis Caching**
3. **Database Integration**
4. **Microservices Architecture**

### Database Migration
```python
# Instead of pickle files, use database
import sqlite3
# or
import postgresql
```

## ✅ Pre-Deployment Checklist

- [ ] All files committed to version control
- [ ] Requirements.txt updated
- [ ] API keys as environment variables
- [ ] Error handling implemented
- [ ] Performance testing completed
- [ ] Mobile responsiveness tested
- [ ] Security review conducted
- [ ] Backup strategy in place

## 🎯 Go Live!

Once deployed, your Movie Recommendation System will be accessible worldwide! 

Share your deployment URL and let users discover amazing movies! 🎬

---

**Need help?** Check the troubleshooting section or create an issue on GitHub.
