import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
try:
    API_KEY = os.getenv("GROQ_API_KEY")

    if not API_KEY:
        raise ValueError("Missing GROQ_API_KEY in .env file.")

    client = Groq(api_key=API_KEY)
    
except ValueError as e:
    print("Wrong value for API key: " + str(e)) #pitfall 1
    exit()
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
    compare_prompt.append(response.choices[0].message.content)
with open("compare_prompts_output.md", "w", encoding="utf-8") as file:
    file.write("\n".join(compare_prompt))
#For each, print the system message and the response in a clearly formatted block.#
#Save all 4 outputs to a single compare_prompts_output.md file. # have to open a file and write it, 
# plus save all output to one variable to be easy/
# 
# #Write 3 observations in notes.md about what changed and what stayed the same.