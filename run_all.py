
import sys
import os

# add both folders to sys.path so Python can find them
sys.path.append(os.path.join(os.path.dirname(__file__), "agent-a-langgraph"))
sys.path.append(os.path.join(os.path.dirname(__file__), "email-sender-agent-crewai"))

from main import graph
from agent.email_sender import EmailAgent


def format_news_for_email(news_items):
    lines = []
    for item in news_items:
        lines.append(f"- {item['title']}\n  {item['summary']}")
    return "\n\n".join(lines)


if __name__ == "__main__":
    topic = "AI"


    input_state = {"topic": topic}
    news_state = graph.invoke(input_state)

    # format results
    formatted_news = format_news_for_email(news_state["results"])

    # send email
    email_agent = EmailAgent()
    recipients = ["khushi.s-external@synergetics.ai"]
    result = email_agent.run(formatted_news, recipients)

    print("\n--- EMAIL SEND RESULT ---")
    print(result)
