"""
daily_brief_v2.py
=================
Reference solution for Week 4 Friday exercise.

The first script in the internship that uses TWO authenticated APIs:
  1. NewsAPI -> fetch today's top tech headlines
  2. Groq    -> rewrite each headline in plain English for a 10th grader

Both the original headline and the AI-rewritten version are shown
in the output, so the user can see what changed.

Defensive design choices:
  - If NewsAPI fails, we print "news unavailable" instead of crashing
  - If Groq fails on any particular headline, we fall back to the
    original headline rather than dropping the whole script
  - temperature=0.3 keeps summaries consistent (low creativity)
"""

import os
import sys

import requests
from dotenv import load_dotenv
from groq import Groq
from rich.console import Console
from rich.panel import Panel


NEWS_URL = "https://newsapi.org/v2/top-headlines"
NUM_ARTICLES = 5

SUMMARIZER_SYSTEM = (
    "You are a friendly summarizer. Rewrite this news headline in one "
    "sentence for a 10th grader who is not into tech. Keep it under 20 "
    "words. Output only the rewritten sentence, nothing else."
)


def load_keys():
    """Load both API keys from .env. Exit early if either is missing."""
    load_dotenv()
    news_key = os.getenv("NEWSAPI_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    missing = []
    if not news_key:
        missing.append("NEWSAPI_KEY")
    if not groq_key:
        missing.append("GROQ_API_KEY")
    if missing:
        print(f"Missing from .env: {', '.join(missing)}")
        sys.exit(1)
    return news_key, groq_key


def fetch_headlines(news_key, category="technology", country="us"):
    """Fetch headlines from NewsAPI. Returns [] on any failure."""
    try:
        response = requests.get(
            NEWS_URL,
            params={
                "category": category,
                "country": country,
                "pageSize": NUM_ARTICLES,
            },
            headers={"X-Api-Key": news_key},
            timeout=10,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(f"NewsAPI error: {err}")
        return []

    return response.json().get("articles", [])


def rewrite_headline(client, original_title):
    """
    Ask the LLM to rewrite a headline. Return the rewritten text.
    On any failure, fall back to the original headline so the
    script still produces useful output.
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SUMMARIZER_SYSTEM},
                {"role": "user",   "content": original_title},
            ],
            temperature=0.3,    # low temp -> consistent, factual summaries
            max_tokens=80,
        )
        return response.choices[0].message.content.strip()
    except Exception as err:
        print(f"Groq error on '{original_title[:40]}...': {err}")
        return original_title


def render(rows):
    """Print a rich Panel showing AI-rewrite + source + original."""
    console = Console()

    if not rows:
        console.print(Panel("(news unavailable)", title="Today's Brief"))
        return

    lines = []
    for i, (original, rewrite, source) in enumerate(rows, start=1):
        lines.append(f"[bold cyan]{i}. {rewrite}[/bold cyan]")
        lines.append(f"   [dim]Source: {source}[/dim]")
        lines.append(f"   [dim italic]Original: {original}[/dim italic]")
        lines.append("")
    body = "\n".join(lines).rstrip()

    console.print(Panel(body, title="Today's Brief (AI-summarised)", expand=False))


def main():
    news_key, groq_key = load_keys()
    articles = fetch_headlines(news_key)

    if not articles:
        render([])
        return

    groq_client = Groq(api_key=groq_key)
    rows = []
    for article in articles:
        original = article.get("title") or "(no title)"
        source = (article.get("source") or {}).get("name") or "Unknown"
        rewrite = rewrite_headline(groq_client, original)
        rows.append((original, rewrite, source))

    render(rows)


if __name__ == "__main__":
    main()
