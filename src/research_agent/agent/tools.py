import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
from research_agent.utils.config import settings


tavily_client = TavilyClient(api_key =settings.tavily_api_key)

def search_web(query:str) -> list[dict]:
    tavily_response = tavily_client.search(query=query,max_results=settings.max_search_results)
    return tavily_response.get('results',[])

def scrape_page(url: str) -> str:
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text,"html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        lines = [line.strip() for line in soup.get_text(separator="\n").split("\n") if len(line.strip()) > 30]
        clean_text = "\n".join(lines)
        return clean_text[:3000]

    except Exception as e:
        return f"Could not scrape {url}. Reason: {str(e)}"

