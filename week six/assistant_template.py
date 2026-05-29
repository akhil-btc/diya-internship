import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
system_prompt = """
You are a Informant.
Your job is to help users find books by their title and author and provide:
- Publication year
- Genre
- Free legal reading options
- Paid purchase options
If you don't have reliable info on a field, say so instead of guessing.
update your example answer to model that uncertainty
"""

messages = [
    {
        "role": "system",
        "content": system_prompt
    },
    {
        "role": "user",
        "content": "Find the book Atomic Habits"
    },
    {
        "role": "assistant",
        "content": """
Title: Atomic Habits

Author: James Clear

Published: 2018

Genre:
- Self-help

Free Reading Options:
- Google Books preview

Paid Options:
- Amazon Kindle
"""
    },
    {
        "role": "user",
        "content": "Find the book Solo Leveling by Chugong"
    }
]

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,
)

print(response.choices[0].message.content)