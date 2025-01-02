import requests

class ChatService:
    def __init__(self):
        self.api_url = "https://api.deepseek.com/chat/completions"  # Updated endpoint
        self.api_key = "sk-ea416e0955f840208c4cdc1558ee7e4f"
    
    def generate_response(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
        
        try:
            print(f"Attempting to connect to: {self.api_url}")
            response = requests.post(self.api_url, headers=headers, json=data)
            print(f"Response status: {response.status_code}")
            
            response.raise_for_status()
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            return "No response generated"
            
        except requests.exceptions.RequestException as e:
            print(f"Detailed error: {str(e)}")
            return f"Error: {str(e)}"
