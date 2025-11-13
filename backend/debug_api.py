"""
Debug script to test API endpoints and LLM responses
Run this while your FastAPI server is running
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_endpoint(name, method, endpoint, data=None, params=None):
    """Test a single endpoint and show response"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")
    
    try:
        start = time.time()
        
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}", params=params, timeout=120)
        else:  # POST
            response = requests.post(f"{BASE_URL}{endpoint}", json=data, timeout=120)
        
        elapsed = time.time() - start
        
        print(f"Status: {response.status_code}")
        print(f"Time: {elapsed:.2f}s")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success!")
            print(f"Response preview:")
            print(json.dumps(result, indent=2)[:500])
        else:
            print(f"❌ Error: {response.text[:200]}")
            
    except requests.exceptions.Timeout:
        print(f"❌ Timeout after 120 seconds")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("🚀 Starting API Debug Tests")
    print("Make sure your FastAPI server is running on port 8000!")
    
    # 1. Health Check
    test_endpoint(
        "Health Check",
        "GET",
        "/health"
    )
    
    # 2. Stats
    test_endpoint(
        "Statistics",
        "GET",
        "/stats"
    )
    
    # 3. Simple Query
    test_endpoint(
        "Natural Language Query",
        "POST",
        "/query",
        data={
            "question": "How many customers have high churn risk?",
            "max_context_rows": 20
        }
    )
    
    # 4. Topic Modeling (reduced sample)
    test_endpoint(
        "Topic Modeling",
        "GET",
        "/topic-modeling",
        params={"sample_size": 10}  # Very small sample for testing
    )
    
    # 5. Text Analysis
    test_endpoint(
        "Text Analysis",
        "POST",
        "/analyze-text",
        data={
            "text": "My internet is very slow and keeps disconnecting. I'm paying too much for this service!"
        }
    )
    
    # 6. Leads
    test_endpoint(
        "Get Leads",
        "GET",
        "/leads/internet_connectivity",
        params={"limit": 5}
    )
    
    print(f"\n{'='*60}")
    print("🎯 TEST SUMMARY")
    print(f"{'='*60}")
    print("If all tests passed, your API is working correctly!")
    print("If any failed, check the error messages above.")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()