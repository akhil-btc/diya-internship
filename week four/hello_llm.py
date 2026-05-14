import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")  #loads key
if API_KEY is None:
    print("There is no API key given! Please give an API key.")
    exit()  #missing key
client = Groq(api_key=API_KEY) #bringforth groq 
response = client.chat.completions.create(model="llama-3.3-70b-versatile",
messages=[
         {"role": "user", "content": "In 3 sentences explain to me what a Large Language Model is."},     
         ]) #asks the model 
print(response.choices[0].message.content)


#Asks the model: "In 3 sentences, explain to me what a Large Language Model is, like I'm a 10th grader."
#Prints the response
#Run it 3 times. Notice that the output is slightly different each time. Write 2 observations in notes.md.
#Commit and push (without .env, of course).