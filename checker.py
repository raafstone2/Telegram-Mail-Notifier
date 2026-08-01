import requests
from bs4 import BeautifulSoup
import os

CHANNEL_URL = "https://t.me/s/v2raytun_kanfing"
LAST_FILE = "last_message.txt"

headers = {
    "User-Agent": "Mozilla/5.0"
}


def get_last_message():
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


def load_old_message():
    if os.path.exists(LAST_FILE):
        with open(LAST_FILE, "r", encoding="utf-8") as f:
            return f.read()

    return ""


def save_message(message):
    with open(LAST_FILE, "w", encoding="utf-8") as f:
        f.write(message)


new_message = get_last_message()

if new_message:
    old_message = load_old_message()

    if new_message != old_message:
        print("پیام جدید پیدا شد:")
        print(new_message)

        save_message(new_message)

    else:
        print("پیام جدیدی وجود ندارد")

else:
    print("نتوانستم پیام کانال را دریافت کنم")
