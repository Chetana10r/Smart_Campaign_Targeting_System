import requests
import time

def test_ollama_speed():
    """Test Ollama response time with different models"""
    
    models = ["llama3.2:1b", "llama3.2:3b", "llama3:latest"]
    
    for model in models:
        print(f"\n{'='*60}")
        print(f"Testing model: {model}")
        print(f"{'='*60}")
        
        try:
            start = time.time()
            
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": model,
                    "prompt": "Say 'Hello' in one word.",
                    "stream": False,
                    "options": {
                        "num_predict": 10
                    }
                },
                timeout=30
            )
            
            elapsed = time.time() - start
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Response time: {elapsed:.2f} seconds")
                print(f"Response: {data.get('response', 'N/A')[:100]}")
            else:
                print(f"❌ HTTP {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"❌ Timeout after 30 seconds")
        except requests.exceptions.ConnectionError:
            print(f"⚠️  Model not found. Run: ollama pull {model}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n{'='*60}")
    print("RECOMMENDATION:")
    print("Use the fastest model that completed successfully")
    print(f"{'='*60}")

if __name__ == "__main__":
    test_ollama_speed()