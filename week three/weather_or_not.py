import requests
import rich
from rich.panel import Panel
from rich.console import Console
import sys
def get_weather():
    docs = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=32.8140"
        "&longitude=-96.9489"
        "&current=temperature_2m"
    )
    try:
        response = requests.get(docs)
        response.raise_for_status()
        data = response.json()
        return data["current"]["temperature_2m"]
    except requests.exceptions.RequestException as e:
        print("an error occurred:", e)
        return None   
    
def get_quote():
    random_quote = "https://zenquotes.io/api/random"
    try:
        response = requests.get(random_quote)
        response.raise_for_status()
        if response.status_code == 404:
            print("Website not found.")
            return None
        data = response.json()
        return data[0]["q"]  # Return the quote text
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        sys.exit()
if __name__ == "__main__":
    temperature = get_weather()
    quote = get_quote()
    if temperature  < 18:
        rich.print("[bold blue]stay warm[/bold blue]", quote) 
    elif temperature > 28:
        rich.print("[bold red]stay hydrated[/bold red]", quote)
    else:
        rich.print("[bold green]nice day for a walk[/bold green]", quote) 
    rich.print("[bold red] hello [/bold red]")
    print("hi")
print("hello")

