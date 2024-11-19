import requests
import schedule
import time
from telegram import Bot

# Settings
TELEGRAM_BOT_TOKEN = '7417257593:AAE75GK41akngDHtBbR8c8MciVwPlKMg6yQ'
CHAT_ID = '@QJyC8NbFDbhkYTk6'  # Channel link provided
CRYPTO_API_URL = 'https://api.coingecko.com/api/v3/coins/markets'
BTC_DOMINANCE_URL = 'https://api.coingecko.com/api/v3/global'
PARAMS = {
    'vs_currency': 'usd',
    'order': 'market_cap_desc',
    'per_page': 20,
    'page': 1,
}

# Function to get crypto data
def get_crypto_data():
    response = requests.get(CRYPTO_API_URL, params=PARAMS)
    if response.status_code == 200:
        return response.json()
    return []

# Function to get Bitcoin dominance
def get_btc_dominance():
    response = requests.get(BTC_DOMINANCE_URL)
    if response.status_code == 200:
        return response.json()['data']['market_cap_percentage']['btc']
    return None

# Function to send updates to Telegram
def send_crypto_update():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    crypto_data = get_crypto_data()
    btc_dominance = get_btc_dominance()

    if crypto_data and btc_dominance is not None:
        message = f"🌍 Bitcoin Dominance: {btc_dominance:.2f}%\n\nTop 20 Cryptocurrencies:\n"
        for coin in crypto_data:
            message += f"{coin['symbol'].upper()} ({coin['name']}): ${coin['current_price']:.2f}\n"
        bot.send_message(chat_id=CHAT_ID, text=message)
    else:
        bot.send_message(chat_id=CHAT_ID, text="Failed to fetch cryptocurrency data.")

# Schedule the task
schedule.every().day.at("10:00").do(send_crypto_update)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
