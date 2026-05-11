"""
daily_brief.py
==============
Reference solution for Week 3 Friday exercise.

Fetches today's top tech headlines from NewsAPI and prints them in a
nicely styled rich Panel.

This is Diya's first script that uses an authenticated API. The API
key is loaded from a .env file using python-dotenv. The .env file
must NEVER be committed to git.

Usage:
    python daily_brief.py                  # default category 'technology'
    python daily_brief.py business         # any NewsAPI category
"""

import os
import sys

import requests
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel


NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
DEFAULT_CATEGORY = "technology"
DEFAULT_COUNTRY = "us"        # change to "in", "gb", etc.
NUM_ARTICLES = 5


def load_api_key():
    """
    Load NEWSAPI_KEY from .env into the environment.
    Returns the key, or exits with a friendly error if missing.
    """
    load_dotenv()
    key = os.getenv("NEWSAPI_KEY")
    if not key:
        print(
            "Missing API key.\n"
            "Create a file named '.env' in this folder with one line:\n"
            "  NEWSAPI_KEY=your_actual_key_here\n"
            "Get a free key at https://newsapi.org/register"
        )
        sys.exit(1)
    return key


def fetch_headlines(api_key, category, country):
    """
    Fetch top-headlines from NewsAPI for a given category and country.

    Returns a list of article dicts on success.
    Returns None on rate-limit (429) or any other failure.
    """
    headers = {"X-Api-Key": api_key}
    params = {"category": category, "country": country, "pageSize": NUM_ARTICLES}

    try:
        response = requests.get(
            NEWS_API_URL, params=params, headers=headers, timeout=10
        )
    except requests.exceptions.RequestException as err:
        print(f"Network error: {err}")
        return None

    if response.status_code == 429:
        print("Rate limit hit. NewsAPI free tier allows 100 requests/day.")
        return None

    if response.status_code == 401:
        print("API key was rejected. Check your .env file.")
        return None

    if response.status_code != 200:
        print(f"Unexpected response: HTTP {response.status_code}")
        return None

    data = response.json()
    return data.get("articles", [])


def render_panel(category, articles):
    """Print the articles inside a styled rich Panel."""
    console = Console()

    if not articles:
        console.print(Panel("No articles to show.", title="Today's Brief"))
        return

    lines = []
    for i, article in enumerate(articles, start=1):
        title = article.get("title") or "(no title)"
        source = (article.get("source") or {}).get("name") or "(unknown)"
        url = article.get("url") or ""
        lines.append(f"[bold]{i}. {title}[/bold]")
        lines.append(f"   [dim]{source}[/dim]   {url}")
        lines.append("")

    body = "\n".join(lines).strip()
    title = f"Today's {category.title()} Brief"
    console.print(Panel(body, title=title, expand=False))


def main():
    category = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CATEGORY
    api_key = load_api_key()
    articles = fetch_headlines(api_key, category, DEFAULT_COUNTRY)
    if articles is None:
        sys.exit(1)
    render_panel(category, articles)


if __name__ == "__main__":
    main()
