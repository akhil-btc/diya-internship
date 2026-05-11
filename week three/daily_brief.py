import os
import requests
import dotenv
import sys
from rich.console import Console
from rich.panel import Panel


dotenv.load_dotenv()
console = Console()
# gets the key (1/6 requiremenetts)
API_KEY = os.getenv("NEWSAPI_KEY")
URL = "https://newsapi.org/v2/top-headlines"
if API_KEY is None:
    console.print("[bold red]API key not found. Please set the NEWSAPI_KEY environment variable.[/bold red]")
    sys.exit()
# handles no API KEY 6.1/3 

info = {
    "country": "us",
    "category": "technology",
    "pageSize": 5, #asked chatgpt how to pull only five, (3/6)
    "apiKey": API_KEY
    }
# gets API data (2/6)
#4, 5 remaining
try:
    response = requests.get(URL, params=info, timeout=10)
    if response.status_code == 429: # 6.3/3 
        console.print("[bold red]Error:[/bold red] [bold blue] Rate limit exceeded. [/bold blue]")
        sys.exit() #using because no point in contining
    response.raise_for_status() # deal with others
    data = response.json()
    articles = data.get("articles", [])
    if not articles:
        console.print("[bold yellow]No articles found.[/bold yellow]")
    else:
        articles_formatted = []
        for article in articles:
            title = article.get("title", "No Title")
            description = article.get("source", "No Source")
            url = article.get("url", "No URL")
        #4 and 5
            articles_formatted.append(f"[bold blue]{title}[/bold blue]\n[bold green]Source: {description}[/bold green]\n[link={url}]Read more[/link]")
        formatted = "\n".join(articles_formatted)
        panel = Panel(formatted, title="Today's Tech")
        console.print(panel)


except requests.exceptions.RequestException as e:
    console.print("an error occurred: " + str(e)) # 6.2/3
    sys.exit()