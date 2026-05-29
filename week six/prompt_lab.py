import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Create Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
prompts = []
prompt = "explain pythagorean theorem in three sentences or less."
prompts.append(prompt)
prompt2 = "explain pythagorean theorem to 7th grader who is just learning basic geometry in the style of a teacher in 3 sentences or less."
prompts.append(prompt2)
for prompt in prompts:
    print(prompt)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )
    print(response.choices[0].message.content)