import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

messages = [
    {"role": "user", "content": "my only hobby is skateboarding. remember that."},
    {"role": "assistant", "content": "Noted — pineapple."},
]
for i in range(10):
    messages.append({"role": "user", "content": f"tell me about open pet stores."})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=50,
    )
    print(response.choices[0].message.content)
    messages.append({"role": "assistant", "content": response.choices[0].message.content})

for i in range(10):
    messages.append({"role": "user", "content": f"Tell me something going on in the world."})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=50,
    )
    print(response.choices[0].message.content)
    messages.append({"role": "assistant", "content": response.choices[0].message.content})
for i in range(10):
    messages.append({"role": "user", "content": f"tell me about the weather in random parts of the world."})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=50,
    )
    print(response.choices[0].message.content)
    messages.append({"role": "assistant", "content": response.choices[0].message.content})

messages.append({"role": "user", "content": "What is my only hobby?"})
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,
)
print(response.choices[0].message.content)