import os
import yaml
import feedparser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)


def get_latest_post(feed_url):
    feed = feedparser.parse(feed_url)

    if not feed.entries:
        return None

    return feed.entries[0]


def is_buffet_post(post, keywords):
    text = (
        post.get("title", "")
        + " "
        + post.get("summary", "")
    ).lower()

    return any(word.lower() in text for word in keywords)


def send_email(subject, body, recipient):
    username = os.environ["GMAIL_USERNAME"]
    password = os.environ["GMAIL_APP_PASSWORD"]

    msg = MIMEMultipart()
    msg["From"] = username
    msg["To"] = recipient
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(username, password)
        server.send_message(msg)


def main():
    config = load_config()

    post = get_latest_post(config["rss"]["url"])

    if not post:
        print("No posts found.")
        return

    if not is_buffet_post(post, config["filter"]["keywords"]):
        print("Latest post does not appear to be buffet-related.")
        return

    body = f"""
{post.title}

{post.summary}

Link:
{post.link}
"""

    send_email(
        "IndeBlue Lunch Buffet Update",
        body,
        config["email"]["recipient"]
    )

    print("Email sent.")


if __name__ == "__main__":
    main()
