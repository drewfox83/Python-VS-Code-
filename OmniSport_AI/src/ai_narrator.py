import os 
import random 
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class AINarrator: 
    def __init__(self):
        self.api_key = os.getenv("OPEN_API_KEY") 
        self.client = None 
        if self.api_key: 
            try: 
                self.client = OpenAI(api_key=self.api_key) 
            except: 
                pass
    
    def generate_commentary(self, data, persona): 
        # 1. Try Real AI 
        if self.client and "error" not in data: 
            try: 
                prompt = f"You are a {persona} commentator. Game: {data['matchup']}. Score: {data['score']}. Event: {data['momentum']}. Write 1 short, exciting sentence."
                response = self.client.chat.completions.create(
                  model="gpt-3.5-turbo", 
                  messages=[{"role": "user", "content": prompt}]  
                )
                return response.choices[0].message.content
            except: 
                pass # Fallback to simulation if API fails 

        # 2. Simulation Backup 
        templates = [
            f"🔥 {persona}: {data['matchup']} is UNREAL! {data['momentum']} just changed everything!",
            f"🎙️ {persona}: Can you believe this score?! {data['score']}!",
            f"👀 {persona}: {data['momentum']}!! This is why we watch!"
        ]
        return random.choice(templates)