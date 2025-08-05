from crewai import Agent, Task, Crew
from crewai.tools import tool
from dotenv import load_dotenv
import os
import smtplib
from email.message import EmailMessage

load_dotenv()


@tool("Send Email Tool")
def send_email_tool(subject: str, body: str, recipients: list) -> str:
    """
    Sends an email using SMTP. Input includes 'subject', 'body', and 'recipients' (list).
    """
    try:
        subject = subject.replace('\n', '').replace('\r', '')
        body = body or "No content provided."
        recipients = [r.strip().replace('\n', '').replace('\r', '') for r in recipients]

        if not recipients:
            return "No recipients provided."
        if any("@" not in r or "." not in r for r in recipients):
            return "Invalid email address detected."

        sender = os.getenv("EMAIL_USERNAME", "").strip().replace('\n', '').replace('\r', '')
        password = os.getenv("EMAIL_PASSWORD")
        host = os.getenv("EMAIL_HOST")
        port = os.getenv("EMAIL_PORT")

        if not all([sender, password, host, port]):
            return "Missing SMTP environment variables."

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        msg.set_content(body)

        with smtplib.SMTP(host, int(port)) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)

        return f" Email sent successfully to: {msg['To']}"

    except Exception as e:
        return f"Failed to send email: {str(e)}"


class EmailAgent:
    def __init__(self):
        self.agent = Agent(
            role="Email Sender",
            goal="Send an email summarizing AI news to the given recipients",
            backstory="You are a reliable assistant that formats and sends AI news updates via email.",
            verbose=True,
            allow_delegation=False,
            tools=[send_email_tool],
        )

    def run(self, news_summary: str, recipients: list):
        subject = "Daily AI News Update"
        body = f"Hello,\n\nHere's your AI news summary:\n{news_summary}\n\nThanks,\nYour AI Assistant"

        task = Task(
            description=(
                "Use the 'Send Email Tool' to send an email with the following arguments: "
                f"subject: {subject}, body: {body}, recipients: {recipients}. "
                "Call the tool using these exact inputs."
            ),
            expected_output="Confirmation that the email was sent successfully.",
            agent=self.agent
        )

        crew = Crew(agents=[self.agent], tasks=[task])
        print("[DEBUG] Kicking off with input:", subject, recipients)
        result = crew.kickoff()
        return result
