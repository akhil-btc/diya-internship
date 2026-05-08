"""
github_profile.py
=================
Reference solution for Week 3 Tuesday exercise.

Fetches a GitHub user's public profile from the GitHub REST API and
prints a clean summary.

Usage:
    python github_profile.py <username>
    python github_profile.py torvalds
    python github_profile.py anthropics

Demonstrates:
  - Reading a CLI argument with sys.argv
  - Making a GET request with the requests library
  - Checking response.status_code before parsing
  - Safely accessing dict fields with .get(key, default)
  - Catching network errors with requests.RequestException
  - Formatting numbers with f-string formatting
"""

import sys
import requests


GITHUB_API_URL = "https://api.github.com/users/{username}"


def fetch_profile(username):
    """
    Fetch the public profile JSON for a GitHub user.

    Returns the parsed JSON dict on success.
    Returns None if the user does not exist or the network fails.
    """
    url = GITHUB_API_URL.format(username=username)

    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException as err:
        print(f"Network error: {err}")
        return None

    if response.status_code == 404:
        print(f"GitHub user '{username}' not found.")
        return None

    if response.status_code != 200:
        print(f"Unexpected response: HTTP {response.status_code}")
        return None

    return response.json()


def print_profile(data):
    """Pretty-print the relevant fields from a GitHub profile dict."""
    # Use .get(...) so missing fields show "(not set)" instead of crashing.
    name = data.get("name") or "(not set)"
    bio = data.get("bio") or "(no bio)"
    location = data.get("location") or "(not set)"
    public_repos = data.get("public_repos", 0)
    followers = data.get("followers", 0)
    created_at = data.get("created_at", "")[:10]   # YYYY-MM-DD only

    print(f"Name:          {name}")
    print(f"Bio:           {bio}")
    print(f"Location:      {location}")
    print(f"Public repos:  {public_repos}")
    print(f"Followers:     {followers:,}")
    print(f"Joined GitHub: {created_at}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python github_profile.py <username>")
        sys.exit(1)

    username = sys.argv[1]
    data = fetch_profile(username)
    if data is None:
        sys.exit(1)

    print_profile(data)


if __name__ == "__main__":
    main()
