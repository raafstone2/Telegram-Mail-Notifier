import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


CHANNEL_URL = "https://t.me/s/v2raytun_kanfing"
LAST_FILE = "last_message.txt"

GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_TO = os.environ.get("GMAIL_TO")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")


headers = {
    "User-Agent": "Mozilla/5.0"
}


def get_latest_message():
    r = requests.get(
        CHANNEL_URL,
        headers=headers,
        timeout=20
    )

    soup = BeautifulSoup(r.text, "html.parser")

    messages = soup.find_all(
        "div",
        class_="tgme_widget_message_text"
    )

    if messages:
        return messages[-1].get_text("\n", strip=True)

    return None


def read_old_message():
    if os.path.exists(LAST_FILE):
        with open(LAST_FILE, "r", encoding="utf-8") as f:
            return f.read()

    return ""


def save_message(message):
    with open(LAST_FILE, "w", encoding="utf-8") as f:
        f.write(message)


def send_email(message):

    msg = MIMEMultipart()

    msg["From"] = GMAIL_USER
    msg["To"] = GMAIL_TO
    msg["Subject"] = "کانفیگ جدید V2Ray از تلگرام"

    body = """
کانفیگ جدید در کانال تلگرام پیدا شد:

---------------------

""" + message

    msg.attach(
        MIMEText(body, "plain", "utf-8")
    )

    server = smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    )

    server.login(
        GMAIL_USER,
        GMAIL_APP_PASSWORD
    )

    server.sendmail(
        GMAIL_USER,
        GMAIL_TO,
        msg.as_string()
    )

    server.quit()


new_message = get_latest_message()


if new_message is None:
    print("خطا در دریافت پیام کانال")
    exit()


old_message = read_old_message()


if new_message != old_message:

    print("پیام جدید پیدا شد:")
    print(new_message)

    save_message(new_message)

    send_email(new_message)

    print("ایمیل ارسال شد")


else:

    print("پیام جدیدی وجود ندارد")
