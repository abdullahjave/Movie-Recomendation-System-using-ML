#!/usr/bin/env python3
"""
Simple test script to verify Flask API is working correctly
"""
import requests
import json

def test_api():
    base_urls = [
        "http://localhost:5000",
        "http://127.0.0.1:5000",
        "http://10.0.2.2:5000"
    ]
    
    for base_url in base_urls:
        print(f"\n🧪 Testing {base_url}")
        try:
            # Test health endpoint
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ Health check successful: {response.json()}")
                
                # Test movies endpoint
                response = requests.get(f"{base_url}/movies", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Movies endpoint successful: {data['count']} movies loaded")
                else:
                    print(f"❌ Movies endpoint failed: {response.status_code}")
                
                # Test recommend endpoint
                test_data = {"title": "Avatar"}
                response = requests.post(f"{base_url}/recommend", 
                                       json=test_data, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Recommend endpoint successful: {len(data['recommendations'])} recommendations")
                else:
                    print(f"❌ Recommend endpoint failed: {response.status_code}")
            else:
                print(f"❌ Health check failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    test_api()
