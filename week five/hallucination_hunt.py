import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Create Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

question = "Who is the face of Full Squad Gaming?"

response1 = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": question
        }
    ],
    temperature=2
)

print(response1.choices[0].message.content)

response2 = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": (
                "If you do not know the answer, "
                "say you do not know. "
                "Do not invent facts."
            )
        },
        {
            "role": "user",
            "content": question
        }
    ],
    temperature=1
)

print(response2.choices[0].message.content)