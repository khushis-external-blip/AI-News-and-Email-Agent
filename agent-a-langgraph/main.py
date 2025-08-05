import os

from langgraph.graph import StateGraph, END
from typing import TypedDict, List
import time
import requests
from dotenv import load_dotenv

load_dotenv()


class NewsState(TypedDict):
    topic: str
    results: List[dict]


# Node Logic - fetch news
def fetch_news(state: NewsState) -> NewsState:
    topic = state['topic']
    api_key = os.getenv("NEWS_API_KEY")
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={topic}&"
        f"language=en&"
        f"sortBy=publishedAt&"
        f"pageSize=5&"
        f"apiKey={api_key}"
    )
    print(f" Fetching live news for topic: {topic}")
    try:
        response = requests.get(url)
        articles = response.json().get("articles", [])
        results = []

        for article in articles:
            results.append({
                "title": article["title"],
                "summary": article["description"] or "No summary available."
            })

        return {
            "topic": topic,
            "results": results
        }
    except Exception as e:
        print(" Failed to fetch news:", e)
        return {
            "topic": topic,
            "results": [{"title": "Error", "summary": str(e)}]
        }


# graph setup
builder = StateGraph(NewsState)
builder.add_node("get_news", fetch_news)
builder.set_entry_point("get_news")
builder.set_finish_point("get_news")

graph = builder.compile()

# run agent
if __name__ == "__main__":
    input_state = {"topic": "AI"}
    output = graph.invoke(input_state)
    print("\n Aggregated News Results:")
    for news in output["results"]:
        print(f"- {news['title']}: {news['summary']}")
