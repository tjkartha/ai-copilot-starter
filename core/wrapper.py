import requests
import time

class CappedOllamaClient:
    def __init__(self, model_name="llama3", max_calls_per_minute=5):
        self.url = "http://localhost:11434/api/generate"
        self.model = model_name
        self.call_history = []
        self.rate_limit = max_calls_per_minute

    def _check_rate_limit(self):
        # Clean up history older than 60 seconds
        current_time = time.time()
        self.call_history = [t for t in self.call_history if current_time - t < 60]
        
        if len(self.call_history) >= self.rate_limit:
            raise Exception("RateLimitError: You have exceeded your API quota. Please optimize your UI retries or implement caching.")
        
        self.call_history.append(current_time)

    def generate(self, prompt, system_prompt=""):
        self._check_rate_limit()
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False
        }
        
        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            # Simulated token economics
            prompt_tokens = len(prompt.split()) * 1.3
            completion_tokens = len(data.get("response", "").split()) * 1.3
            
            return {
                "text": data.get("response", ""),
                "metrics": {
                    "latency_ms": data.get("total_duration", 0) / 1_000_000,
                    "simulated_prompt_tokens": int(prompt_tokens),
                    "simulated_completion_tokens": int(completion_tokens)
                }
            }
        except requests.exceptions.ConnectionError:
            return {"error": "Failed to connect to local Ollama. Is it running?"}
