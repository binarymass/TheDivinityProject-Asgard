
import random
import time
import os
from transformers import pipeline

class StealthTools:
    def __init__(self):
        self.agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "Mozilla/5.0 (X11; Linux x86_64)",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X)",
            "Mozilla/5.0 (Android 11; Mobile; rv:83.0)"
        ]
        self.headers = [
            {"Accept-Language": "en-US,en;q=0.9"},
            {"Cache-Control": "no-cache"},
            {"Accept-Encoding": "gzip, deflate"},
            {"DNT": "1"},
            {"Upgrade-Insecure-Requests": "1"}
        ]
        self.model = pipeline("text-generation", model="openai-community/gpt2")

    def get_headers(self):
        headers = random.choice(self.headers).copy()
        headers["User-Agent"] = random.choice(self.agents)
        return headers

    def jitter_delay(self, base=1.0, jitter=0.5):
        delay = random.uniform(base - jitter, base + jitter)
        time.sleep(max(delay, 0))

    def mutate_payload(self, payload, context="web fuzzing"):
        prompt = f"Obfuscate this payload for {context} evasion: {payload}"
        result = self.model(prompt, max_length=50)[0]["generated_text"]
        return result.strip()
