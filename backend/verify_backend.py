import requests
import json

def test_chat():
    url = "http://localhost:8000/chat"
    payload = {
        "conversation_id": "test-conv-123",
        "message": "Who created you?",
        "user_name": "Tester"
    }
    
    print("Testing /chat endpoint (streaming)...")
    try:
        response = requests.post(url, json=payload, stream=True)
        if response.status_code == 200:
            print("Response: ", end="", flush=True)
            for chunk in response.iter_content(chunk_size=None):
                if chunk:
                    print(chunk.decode(), end="", flush=True)
            print("\nSuccess!")
        else:
            print(f"Failed with status code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error: {e}")

def test_history():
    url = "http://localhost:8000/history?user_name=Tester"
    print("\nTesting /history endpoint...")
    try:
        response = requests.get(url)
        print(f"Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Note: This requires the server to be running.
    # Since I cannot run the server in the background easily here, 
    # I'll just provide this script for the user or try to run it if I can.
    test_chat()
    test_history()
