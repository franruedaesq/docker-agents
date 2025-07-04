from langchain_core.tools import tool
from api.myemailer.inbox_reader import read_inbox
from api.myemailer.sender import send_email
from api.ai.services import generate_email_message
from langchain_core.runnables import RunnableConfig

@tool
def research_email(query: str, config: RunnableConfig) -> str:
    """
    Generate an email message based on the provided query.

    Arguments:
    - query: str: The query to generate the email content from.

    Returns:
    A structured email message.
    """
    try:
        print("==> ", config)
        metadata = config.get("metadata", {})
        add_field = metadata.get("additional_field", None)
        print(f"==>: {add_field}")
        email_message = generate_email_message(query)
        msg = f"Subject: {email_message.subject}\nBody: {email_message.content}"
        return msg
    except Exception as e:
        return f"Failed to generate email message: {str(e)}"

@tool
def send_me_email(
    subject: str = "No subject provided",
    content: str = "No message provided"
) -> str:
    """
    Send an email to mself with a subject and content.

    Arguments:
    - subject: Subject of the email
    - content: Content of the email
    """
    try:
        send_email(subject=subject, content=content)
    except:
        return "Failed to send email. Please check your email configuration."
    return "Email sent successfully."


@tool
def get_unread_emails(hours_ago: int = 48):
    """
    Fetch unread emails from the last specified number of hours.

    Arguments:
    - hours_ago: int = 24: Number of hours to look back for unread emails

    Returns:
    A string of emails separated by a linea "---"
    """
    try:
        emails = read_inbox(hours_ago=hours_ago, verbose=False)
    except Exception as e:
        return f"Failed to fetch emails: {str(e)}"
    cleaned = []
    for email in emails:
        data = email.copy()
        if "html_body" in data:
            data.pop("html_body")
        msg = ""
        for k, v in data.items():
            msg += f"{k}: {v}\n"
        cleaned.append(msg)
    return "\n------\n".join(cleaned)[:500] if cleaned else "No unread emails"