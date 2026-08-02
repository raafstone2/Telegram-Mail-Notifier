import requests
from bs4 import BeautifulSoup
import os
import json
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


SOURCES = [

    {
        "title": "کانال ۱ تلگرام",
        "name": "v2raytun_kanfing",
        "url": "https://t.me/s/v2raytun_kanfing"
    },

    {
        "title": "گروه ۱ تلگرام",
        "name": "napsternetv",
        "url": "https://t.me/s/napsternetv"
    },

    {
        "title": "کانال ۳ تلگرام",
        "name": "config_NG",
        "url": "https://t.me/s/config_NG"
    },

    {
        "title": "کانال ۴ تلگرام",
        "name": "v2ray_dalghak",
        "url": "https://t.me/s/v2ray_dalghak"
    },

    {
        "title": "کانال ۵ تلگرام",
        "name": "v2ray_free_conf",
        "url": "https://t.me/s/v2ray_free_conf"
    },

    {
        "title": "کانال ۶ تلگرام",
        "name": "free1ss",
        "url": "https://t.me/s/free1ss"
    },

    {
        "title": "کانال ۷ تلگرام",
        "name": "BlanK_Vpn",
        "url": "https://t.me/s/BlanK_Vpn"
    },

    {
        "title": "کانال ۹ تلگرام",
        "name": "V2ghostvpn",
        "url": "https://t.me/s/V2ghostvpn"
    },

    {
        "title": "کانال ۱۰ تلگرام",
        "name": "WireguardV2rey",
        "url": "https://t.me/s/WireguardV2rey"
    },

    {
        "title": "کانال ۱۱ تلگرام",
        "name": "MI6VPN",
        "url": "https://t.me/s/MI6VPN"
    },

    {
        "title": "کانال ۱۲ تلگرام",
        "name": "BigSmoke_Config",
        "url": "https://t.me/s/BigSmoke_Config"
    },

    {
        "title": "کانال ۱۳ تلگرام",
        "name": "V2RAYNG_Outline_VPN",
        "url": "https://t.me/s/V2RAYNG_Outline_VPN"
    }

]


STATE_FILE = "last_message.json"


GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_TO = os.environ.get("GMAIL_TO")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


V2RAY_PROTOCOLS = [
    "vless://",
    "vmess://",
    "trojan://",
    "ss://",
    "ssr://",
    "hysteria://",
    "hy2://"
]
def load_state():

    if os.path.exists(STATE_FILE):

        with open(
            STATE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    return {}



def save_state(state):

    with open(
        STATE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            state,
            file,
            ensure_ascii=False,
            indent=2
        )



def check_v2ray(text):

    if not text:
        return False

    text = text.lower()

    for protocol in V2RAY_PROTOCOLS:

        if protocol in text:

            return True

    return False



def get_latest_message(source):

    response = requests.get(
        source["url"],
        headers=HEADERS,
        timeout=20
    )


    soup = BeautifulSoup(
        response.text,
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



def send_email(source, message):

    mail = MIMEMultipart()


    mail["From"] = GMAIL_USER

    mail["To"] = GMAIL_TO


    mail["Subject"] = (
        f'{source["title"]} '
        f'({source["name"]})'
    )


    body = f"""
منبع کانفیگ:

{source["title"]} ({source["name"]})


کانفیگ جدید V2Ray:

---------------------

{message}

"""


    mail.attach(
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
        mail.as_string()
    )


    server.quit()
    state = load_state()


email_sent = False



for source in SOURCES:

    try:

        message = get_latest_message(source)


        if message is None:

            print(
                f'پیامی از {source["name"]} دریافت نشد'
            )

            continue



        if not check_v2ray(message):

            print(
                f'پیام غیر کانفیگ از {source["name"]} رد شد'
            )

            continue



        old_message = state.get(
            source["name"],
            ""
        )



        if message != old_message:


            print(
                f'کانفیگ جدید از {source["name"]} پیدا شد'
            )


            send_email(
                source,
                message
            )


            state[source["name"]] = message


            email_sent = True



        else:

            print(
                f'کانفیگ جدیدی از {source["name"]} وجود ندارد'
            )



    except Exception as error:


        print(
            f'خطا در بررسی {source["name"]}:'
        )

        print(error)




save_state(state)



if email_sent:

    print(
        "ایمیل ارسال شد"
    )

else:

    print(
        "هیچ کانفیگ جدیدی پیدا نشد"
    )
