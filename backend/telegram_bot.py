import os
import requests

# Read credentials from environment variables (set in Amvera)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_to_telegram(ad):
    """Send ad to Telegram channel"""

    # Check if credentials are available
    if not BOT_TOKEN or not CHAT_ID:
        print("❌ Error: BOT_TOKEN or CHAT_ID not set in environment variables")
        return None

    # Format the message
    message = f"""
📢 NEW AD!

🏷️ Title: {ad.title}
💰 Price: {ad.price} RUB
📂 Category: {ad.category}
📝 Description: {ad.description}
📞 Contact: {ad.contact}
    """

    # Telegram API URL
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    # Payload to send
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ Sent to Telegram!")
        else:
            print(f"⚠️ Telegram API returned: {response.status_code}")
        return response.json()
    except Exception as e:
        print(f"❌ Error sending to Telegram: {e}")
        return None