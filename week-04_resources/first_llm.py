import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# response = client.chat.completions.create(model="llama-3.3-70b-versatile",messages=[ {"role": "user", "content": "Hello! Who are you?"}],)

# response = client.chat.completions.create(model="llama-3.3-70b-versatile",
# messages=[
#         {"role": "system", "content": "You are a poet. Answer everything in 4 lines of rhyming verse."},
#         {"role": "user", "content": "Why is the sky blue?"}
#     ])


# response = client.chat.completions.create(model="llama-3.3-70b-versatile",
# messages=[
#         {"role": "system", "content": "You are a 5-year-old. Answer using only short, simple words."},
#         {"role": "user", "content": "Why is the sky blue?"}
#     ])

# response = client.chat.completions.create(model="llama-3.3-70b-versatile",
# messages=[
#         {"role": "system", "content": "You are a physicist. Be technical and precise. In 3-4 sentences"},
#         {"role": "user", "content": "Why is the sky blue?"}
#     ])

response = client.chat.completions.create(model="llama-3.3-70b-versatile",
messages=[
        {"role": "system", "content": "Rewrite this headline in one sentence for a 10th grader who isn't into tech:"},
        {"role": "user", "content": "Apple unveils new chip with 50% more performance."}
    ])

print(response.choices[0].message.content)


