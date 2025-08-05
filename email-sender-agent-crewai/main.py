from agent.email_sender import EmailAgent

if __name__ == "__main__":
    email_agent = EmailAgent()

    news = "- OpenAI released a new model\n- LangChain raised $20M\n- AI Act passed in Europe"
    recipients = ["khushi.s-external@synergetics.ai"]

    result = email_agent.run(news, recipients)

    print("\n--- RESULT ---")
    print(result)
