import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

messages = [
    {"role": "user", "content": "My favourite fruit is pineapple. Remember that."},
    {"role": "assistant", "content": "Noted — pineapple."},
]

for i in range(10):
    messages.append({"role": "user", "content": f"Tell me a random fact about science."})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=50,
    )
    messages.append({"role": "assistant", "content": response.choices[0].message.content})

messages.append({"role": "user", "content": "What is my favourite fruit?"})
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,
)

#128k
#100k context wondow, 200k context window , 1M context window
print("Did the model remember?")
print(response.choices[0].message.content)