import requests

url = "https://t.me/s/v2raytun_kanfing"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(url, headers=headers, timeout=20)

print("Status:", r.status_code)
print(r.text[:1000])
