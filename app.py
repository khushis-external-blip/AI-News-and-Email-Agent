import os
import sys
import streamlit as st

# add  subfolders to path
sys.path.append(os.path.join(os.path.dirname(__file__), "agent-a-langgraph"))
sys.path.append(os.path.join(os.path.dirname(__file__), "email-sender-agent-crewai"))

from main import graph  # LangGraph news agent
from agent.email_sender import EmailAgent  # CrewAI email sender


# format news
def format_news_for_email(news_items):
    lines = []
    for item in news_items:
        lines.append(f"- {item['title']}\n  {item['summary']}")
    return "\n\n".join(lines)


# Streamlit UI
st.title("🗞️ AI News Email Sender")

topic = st.text_input("Enter news topic", value="AI")
recipient_input = st.text_area("Enter recipient emails (comma separated)", value="you@example.com")

if st.button("Fetch News and Send Email"):
    with st.spinner("Fetching news..."):
        # fetch news from LangGraph agent
        input_state = {"topic": topic}
        news_state = graph.invoke(input_state)

        # format news for email
        formatted_news = format_news_for_email(news_state["results"])

    st.success("News fetched successfully!")
    st.subheader("📰 News Summary")
    st.text(formatted_news)

    # send email
    recipients = [email.strip() for email in recipient_input.split(",") if email.strip()]
    email_agent = EmailAgent()

    with st.spinner("Sending email..."):
        result = email_agent.run(formatted_news, recipients)

    st.success(" Email sent!")
    st.subheader(" Email Result")
    st.text(result)
