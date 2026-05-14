import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

prompt = "Write one sentence about cat"

for temp in [0.0, 0.7, 1.5]:
    print(f"\n=== Temperature: {temp} ===")
    for _ in range(2):
        r = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=temp,
        )
        print(r.choices[0].message.content)

#summarize news = low
#writing poetry = high
#doing math = 0