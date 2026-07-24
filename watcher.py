import os
import smtplib
import requests
import yaml
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)


def get_instagram_caption(username):
    """
    Attempts to retrieve public Instagram page metadata.
    """
    url = f"https://www.instagram.com/{username}/"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/120 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Look for Open Graph description
    description = soup.find(
        "meta",
        property="og:description"
    )

    if description:
        return description.get("content", "")

    return None


def send_email(subject, body):
    username = os.environ["GMAIL_USERNAME"]
    password = os.environ["GMAIL_APP_PASSWORD"]
    recipient = os.environ["EMAIL_RECIPIENT"]

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

    instagram = config["restaurant"]["instagram_username"]

    caption = get_instagram_caption(instagram)

    if not caption:
        print("No Instagram caption found.")
        return

    # First version: send whatever Instagram exposes.
    # Later we will filter specifically for buffet posts.
    send_email(
        "IndeBlue Menu Update",
        caption
    )

    print("Email sent.")


if __name__ == "__main__":
    main()
