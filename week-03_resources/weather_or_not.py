"""
weather_or_not.py
=================
Reference solution for Week 3 Wednesday exercise.

Combines two free public APIs to produce a personal daily greeting:
  - Open-Meteo (no API key) for the current temperature
  - ZenQuotes  (no API key) for a random inspirational quote

Adds a context-aware note based on the temperature, and prints the
output as a styled panel using the `rich` library.

Demonstrates:
  - Each API call wrapped in its own function with a docstring
  - try/except requests.RequestException around each call so one
    failing API does not break the other
  - Defensive parsing: never assume a JSON field exists
  - Clean separation of "fetch", "format", and "render" steps
"""

import requests
from rich.console import Console
from rich.panel import Panel


# Edit these for your city if you want a different default location.
DEFAULT_CITY = "Mumbai"
DEFAULT_LAT = 19.0760
DEFAULT_LON = 72.8777


def fetch_temperature(latitude, longitude):
    """
    Fetch the current temperature in Celsius for a given lat/lon.

    Returns the temperature as a float, or None on failure.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as err:
        print(f"Could not fetch weather: {err}")
        return None

    data = response.json()
    weather = data.get("current_weather") or {}
    return weather.get("temperature")


def fetch_quote():
    """
    Fetch a random inspirational quote.

    Returns (quote_text, author) tuple, or (None, None) on failure.
    """
    url = "https://zenquotes.io/api/random"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as err:
        print(f"Could not fetch quote: {err}")
        return None, None

    payload = response.json()
    if not payload:
        return None, None
    first = payload[0]
    return first.get("q"), first.get("a")


def temperature_note(temp_celsius):
    """Return a short context note based on the temperature."""
    if temp_celsius is None:
        return ""
    if temp_celsius < 18:
        return "(Stay warm)"
    if temp_celsius > 28:
        return "(Stay hydrated)"
    return "(Nice day for a walk)"


def render_panel(city, temperature, quote, author):
    """Pretty-print the assembled greeting as a rich Panel."""
    console = Console()

    if temperature is None:
        weather_line = f"Weather in {city}: unavailable"
    else:
        note = temperature_note(temperature)
        weather_line = f"Weather in {city}: {temperature:.1f}°C {note}"

    if quote is None:
        quote_line = "Quote: unavailable"
    else:
        quote_line = f"\"{quote}\"\n  — {author}"

    body = f"{weather_line}\n\n{quote_line}"
    console.print(Panel(body, title="Your daily digest", expand=False))


def main():
    temperature = fetch_temperature(DEFAULT_LAT, DEFAULT_LON)
    quote, author = fetch_quote()
    render_panel(DEFAULT_CITY, temperature, quote, author)


if __name__ == "__main__":
    main()
