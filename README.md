# Shilav Monitor

A tiny Railway worker that checks a target landing page every few seconds and sends a Telegram alert when the page no longer contains the configured out-of-stock texts.

## Local run

```bash
cp .env.example .env
pip install -r requirements.txt
python app.py
```

## Railway setup

1. Push this repo to GitHub.
2. In Railway, create a new project from the GitHub repo.
3. Add these variables in the service Variables tab:
   - `TARGET_URL`
   - `CHECK_INTERVAL_SECONDS`
   - `ALERT_REPEAT_INTERVAL_SECONDS`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
   - `OUT_OF_STOCK_TEXTS`
4. Deploy.

Do not commit a real `.env` file.
