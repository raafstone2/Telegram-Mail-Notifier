import requests
from bs4 import BeautifulSoup
import os
import json
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


CHANNELS = [
    {
        "type": "کانال ۱ تلگرام",
        "name": "v2raytun_kanfing",
        "url": "https://t.me/s/v2raytun_kanfing"
    },
    {
        "type": "گروه ۱ تلگرام",
        "name": "napsternetv",
        "url": "https://t.me/s/napsternetv"
    },
    {
        "type": "کانال ۳ تلگرام",
        "name": "config_NG",
        "url": "https://t.me/s/config_NG"
    },
    {
        "type": "کانال ۴ تلگرام",
        "name": "v2ray_dalghak",
        "url": "https://t.me/s/v2ray_dalghak"
    },
    {
        "type": "کانال ۵ تلگرام",
        "name": "v2ray_free_conf",
        "url": "https://t.me/s/v2ray_free_conf"
    },
    {
        "type": "کانال ۶ تلگرام",
        "name": "free1ss",
        "url": "https://t.me/s/free1ss"
    },
    {
        "type": "کانال ۷ تلگرام",
        "name": "BlanK_Vpn",
        "url": "https://t.me/s/BlanK_Vpn"
    },
    {
        "type": "کانال ۹ تلگرام",
        "name": "V2ghostvpn",
        "url": "https://t.me/s/V2ghostvpn"
    },
    {
        "type": "کانال ۱۰ تلگرام",
        "name": "WireguardV2rey",
        "url": "https://t.me/s/WireguardV2rey"
    },
    {
        "type": "کانال ۱۱ تلگرام",
        "name": "MI6VPN",
        "url": "https://t.me/s/MI6VPN"
    },
    {
        "type": "کانال ۱۲ تلگرام",
        "name": "BigSmoke_Config",
        "url": "https://t.me/s/BigSmoke_Config"
    },
    {
        "type": "کانال ۱۳ تلگرام",
        "name": "V2RAYNG_Outline_VPN",
        "url": "https://t.me/s/V2RAYNG_Outline_VPN"
    }
]


STATE_FILE = "last_message.json"


GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_TO = os.environ.get("GMAIL_TO")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")


headers = {
    "User-Agent": "Mozilla/5.0"
}


PROTOCOLS = [
    "vless://",
    "vmess://",
    "trojan://",
    "ss://",
    "ssr://",
    "hysteria://",
    "hy2://"
]
def is_v2ray_config(text):
    if not text:
        return False

    text_lower = text.lower()

    for protocol in PROTOCOLS:
        if protocol in text_lower:
            return True

    return False



def get_latest_message(channel):

    r = requests.get(
        channel["url"],
        headers=headers,
        timeout=20
    )

    soup = BeautifulSoup(
        r.text,
        "html.parser"
    )

    messages = soup.find_all(
        "div",
        class_="tgme_widget_message_text"
    )

    if messages:
        return messages[-1].get_text(
            "\n",
            strip=True
        )

    return None



def load_state():

    if os.path.exists(STATE_FILE):

        with open(
            STATE_FILE,
            "r",
            encoding="utf-8"
        ) as f:
            return json.load(f)

    return {}



def save_state(state):

    with open(
        STATE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            state,
            f,
            ensure_ascii=False,
            indent=2
        )



def send_email(channel, message):

    msg = MIMEMultipart()

    msg["From"] = GMAIL_USER
    msg["To"] = GMAIL_TO

    msg["Subject"] = (
        f'{channel["type"]} '
        f'({channel["name"]})'
    )


    body = f"""
منبع:

{channel["type"]} ({channel["name"]})


کانفیگ جدید V2Ray پیدا شد:


---------------------

{message}

"""


    msg.attach(
        MIMEText(
            body,
            "plain",
            "utf-8"
        )
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
    state = load_state()

new_found = False


for channel in CHANNELS:

    try:

        new_message = get_latest_message(channel)


        if new_message is None:
            continue


        if not is_v2ray_config(new_message):
            print(
                f'پیام غیر کانفیگ از {channel["name"]} رد شد'
            )
            continue



        old_message = state.get(
            channel["name"],
            ""
        )


        if new_message != old_message:


            print(
                f'پیام جدید از {channel["name"]} پیدا شد'
            )


            print(new_message)


            send_email(
                channel,
                new_message
            )


            state[channel["name"]] = new_message


            new_found = True


        else:

            print(
                f'پیام جدیدی از {channel["name"]} وجود ندارد'
            )


    except Exception as e:

        print(
            f'خطا در بررسی {channel["name"]}:'
        )

        print(e)



save_state(state)



if new_found:

    print(
        "ایمیل ارسال شد"
    )

else:

    print(
        "هیچ کانفیگ جدیدی پیدا نشد"
    )
