from langchain_core.tools import tool
from dotenv import load_dotenv
import os
load_dotenv()
from langchain_community.tools.tavily_search import TavilySearchResults
from typing import List, Dict
from rich import print
from bs4 import BeautifulSoup
import requests

tavily_api_key = os.getenv("TAVILY_API_KEY")

tavily_search_tool = TavilySearchResults(api_key=tavily_api_key,max_results=5)

@tool
def search_results(topic:str)->str:
    
    """Searches the web using Tavily API to fetch top relevant search results only current year most updated results
    """
    updated_query = f"{topic} latest news updates 2026"
    tavily_result = tavily_search_tool.invoke({"query": updated_query})

    results = []
    for result in tavily_result:
        results.append({
            "title": result.get("title"),
            "url": result.get("url"),
            "content": result.get("content")[:200]
        })

    return results



#result= search_results.invoke({"topic":"what are the current affairs btw usa and pakistan?"})

#print(result[0]["url"])


@tool
def get_webpage_content(url:str)->str:
    """Fetches the content of a webpage given its URL using BeautifulSoup.
    """
    try:
        headers={"User-Agent":"Mozilla/5.0"}
        response = requests.get(url,headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        targeted_data = soup.find_all(["h1", "h2", "h3", "p"])
        scrapped_text = "\n".join([element.get_text() for element in targeted_data])
        return scrapped_text
    except Exception as e:
        return f"An error occurred while fetching the webpage: {e}"


#print(get_webpage_content.invoke({"url":"https://www.bbc.com/news/articles/cvgy8q4z0n4o"}))