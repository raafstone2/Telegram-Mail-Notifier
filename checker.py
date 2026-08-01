import requests
from bs4 import BeautifulSoup

url = "https://t.me/s/v2raytun_kanfing"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(url, headers=headers, timeout=20)

soup = BeautifulSoup(r.text, "html.parser")

messages = soup.find_all("div", class_="tgme_widget_message_text")

print("تعداد پیام پیدا شده:", len(messages))

if messages:
    last_message = messages[-1].get_text("\n", strip=True)
    print("آخرین پیام کانال:")
    print(last_message)
else:
    print("پیامی پیدا نشد")
