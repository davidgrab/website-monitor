import os
import time
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("TARGET_URL", "https://lp.vp4.me/jzze")
CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS", "30"))
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# If any of these appears, we assume the coupon is still unavailable.
OUT_OF_STOCK_TEXTS = [
    text.strip()
    for text in os.getenv(
        "OUT_OF_STOCK_TEXTS",
        "המלאי אזל,אזל תוך זמן קצר,נעדכן בקרוב,הערכה טרם חזרה",
    ).split(",")
    if text.strip()
]

REQUEST_TIMEOUT_SECONDS = 15


def now_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def send_telegram(message: str) -> None:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram is not configured. Message was:", message, flush=True)
        return

    response = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        data={"chat_id": TELEGRAM_CHAT_ID, "text": message},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()


def fetch_page_text() -> str:
    response = requests.get(
        URL,
        headers={"User-Agent": "Mozilla/5.0 shilav-monitor/1.0"},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.text


def looks_available(page_text: str) -> bool:
    return not any(text in page_text for text in OUT_OF_STOCK_TEXTS)


def main() -> None:
    print(f"Starting monitor for {URL}", flush=True)
    print(f"Checking every {CHECK_INTERVAL_SECONDS} seconds", flush=True)
    print(f"Out-of-stock texts: {OUT_OF_STOCK_TEXTS}", flush=True)

    already_alerted = False

    while True:
        try:
            page_text = fetch_page_text()
            available = looks_available(page_text)
            print(f"{now_text()} | available={available}", flush=True)

            if available and not already_alerted:
                send_telegram(
                    "🚨 Shilav Monitor\n\n"
                    "נראה שהקופון/המלאי חזר או שהעמוד השתנה.\n\n"
                    f"🔗 {URL}\n"
                    f"🕒 {now_text()}\n\n"
                    "כדאי להיכנס עכשיו ולבדוק מהר."
                )
                already_alerted = True

            if not available:
                already_alerted = False

        except Exception as exc:
            print(f"{now_text()} | error={exc}", flush=True)

        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
