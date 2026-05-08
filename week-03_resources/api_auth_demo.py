import os
import requests
from dotenv import load_dotenv

load_dotenv() #automaticaaly load the .env in our system(computer)

api_key = os.getenv("NEWSAPI_KEY", 'No  NEWS API key exisits')

response = requests.get(
    "https://newsapi.org/v2/top-headlines",
    params={"country": "us", "category": "sports"},
    headers={"X-Api-Key": api_key}, # actual authentication
)

data = response.json()
print(data)
for article in data.get("articles", [])[:3]:
    print(article["title"])