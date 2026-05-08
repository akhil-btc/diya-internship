import sys
import requests
if len(sys.argv) < 2:
    print("Usage: python github_profile.py <username>")
    sys.exit()
username = sys.argv[1]
website = "https://api.github.com/users/" + username
try:
    response = requests.get(website, timeout=10)
except requests.exceptions.RequestException as e:
    print("An error occurred:", e)
    sys.exit()
if response.status_code == 404:
    print("No such User Found.")
    sys.exit()
response.raise_for_status()
data = response.json()
name = data.get("name")
bio = data.get("bio")
public_repos = data.get("public_repos")
followers = data.get("followers")
location = data.get("location")
created_at = data.get("created_at")
print("Name: ", name)
print("Bio: ", bio)
print("Public Repositories: ", public_repos)
print("Followers: ", followers)
print("Location: ", location)
print("Created On: ", created_at)
