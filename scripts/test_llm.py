import requests
import time
import sys

API_URL = "http://localhost:8000"

def test_llm_pipeline():
    print("🚀 Starting LLM Pipeline Test...")
    
    # 1. Ingest some data
    symbol = "BTC-USD"
    print(f"1️⃣  Ingesting data for {symbol}...")
    for i in range(5):
        price = 50000 + i * 100
        requests.post(f"{API_URL}/ingest/", params={"symbol": symbol, "price": price})
    
    # 2. Trigger summary generation
    print(f"2️⃣  Triggering summary generation for {symbol}...")
    response = requests.post(f"{API_URL}/insights/trigger", params={"symbol": symbol})
    if response.status_code != 200:
        print(f"❌ Failed to trigger summary: {response.text}")
        return
    
    print("⏳ Waiting for worker to process (10s)...")
    time.sleep(10)
    
    # 3. Check for summary
    print(f"3️⃣  Checking for latest summary...")
    response = requests.get(f"{API_URL}/insights/latest", params={"symbol": symbol})
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Summary found!")
        print(f"   Summary: {data.get('summary')[:100]}...")
        print(f"   Embedding length: {len(data.get('embedding', []))}")
    else:
        print(f"❌ No summary found yet (Status: {response.status_code})")
        print("   (Worker might still be processing or LLM failed)")

if __name__ == "__main__":
    try:
        test_llm_pipeline()
    except Exception as e:
        print(f"❌ Error: {e}")
