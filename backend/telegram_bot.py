import requests

# REPLACE WITH YOUR DATA!
BOT_TOKEN = "8944532359:AAGWwZ6jUKQjNkUFmTKEsqeZX_cDzmgAlB0"  # Must be new and working
CHAT_ID = "-1003699364569"  # Must be correct (starts with -100)


def send_to_telegram(ad):
    message = f"""
📢 NEW AD!

🏷️ Title: {ad.title}
💰 Price: {ad.price} RUB
📂 Category: {ad.category}
📝 Description: {ad.description}
📞 Contact: {ad.contact}
    """

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, json=payload)
        print("✅ Sent to Telegram!")
        print(response.json())
        return response.json()
    except Exception as e:
        print(f"❌ Error sending to Telegram: {e}")
        return None