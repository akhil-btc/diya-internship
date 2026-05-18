import os
from dotenv import load_dotenv
from groq import Groq
import sys

load_dotenv()
# try:
#     API_KEY = os.getenv("GROQ_API_KEY")

#     if not API_KEY:
#         raise ValueError("Missing GROQ_API_KEY in .env file.")

#     client = Groq(api_key=API_KEY)
    
# except ValueError as e:
#     print("Wrong value for API key: " + str(e)) #pitfall 1
#     exit()

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    print("Missing GROQ_API_KEY in .env file.")
    sys.exit(1)
client = Groq(api_key=API_KEY)

question = "Can deaf people whisper?"
prompts = ["You are a poet. Answer in 4 lines of rhyming verse.",  "You are a 5-year-old. Use only short words.",  "You are a Wikipedia editor. Be neutral and factual.",  "You are an enthusiastic teacher. Use analogies and exclamation points."]
compare_prompt = []
for prompt in prompts:
    response = client.chat.completions.create(model="llama-3.3-70b-versatile",
       
    messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
        ])
    print(f"System Prompt: {prompt}\nResponse:\n{response.choices[0].message.content}\n{'-'*50}\n") 
    value = response.choices[0].message.content
    value = value.replace('\n', '') #removeing paragraph lines
    compare_prompt.append(value)
with open("compare_prompts_output.md", "w", encoding="utf-8") as file:
    file.write(f"# Same question, 4 system prompts\n\n")
    file.write(f"**Question:** {question}\n\n---\n\n")
    for system_prompt, response_text in zip(prompts, compare_prompt):
        file.write(f"## System: {system_prompt}\n\n")
        file.write(f"{response_text}\n\n---\n\n")
#For each, print the system message and the response in a clearly formatted block.#
#Save all 4 outputs to a single compare_prompts_output.md file. # have to open a file and write it, 
# plus save all output to one variable to be easy/
# 
# #Write 3 observations in notes.md about what changed and what stayed the same.

#[] - system, #compare_prompt []
#zip -> [{system_prompt, compare_prompt}], [{system, None}]