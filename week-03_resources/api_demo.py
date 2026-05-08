import requests

# response = requests.get("https://api.github.com/users/torvalds") # public url
# print(response.status_code)
# data = response.json()

# print(f"Name: {data['name']}")
# print(f"Bio: {data['bio']}")
# print(f"Public repos: {data['public_repos']}")
# print(f"Followers: {data['followers']:,}")


# response = requests.get("https://api.github.com/users/this_user_definitely_does_not_exist_xyz") 
# print(response.status_code)
# print(response.json())

# 200 - ok, good
# 404 - not found
# 500 - means server is broken
# 401 - not authorised


# Open-Meteo - no API key needed, free
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 19.0760,    # Mumbai
    "longitude": 72.8777,
    "current_weather": True,
}
response = requests.get(url, params=params)
data = response.json()
print(f"Temperature in Mumbai: {data['current_weather']['temperature']}°C")