import telegram
import pandas as pd
from pytron import Tron
from pytron.exceptions import TronException

# Устанавливаем параметры для подключения к Telegram API
bot_token = 'YOUR_BOT_TOKEN'
bot_chatID = 'YOUR_CHAT_ID'

# Устанавливаем параметры для подключения к сети Tron
tron = Tron()
tron.private_key = 'YOUR_PRIVATE_KEY'
tron.default_address = 'YOUR_DEFAULT_ADDRESS'

# Загружаем данные из CSV-файла
data = pd.read_csv('wallets.csv')

# Создаем Telegram-бота
bot = telegram.Bot(token=bot_token)

# Отправляем транзакцию USDT на каждый кошелек из таблицы
for index, row in data.iterrows():
    try:
        # Отправляем транзакцию USDT
        tx_hash = tron.trx.transfer(row['address'], row['amount'], 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t')
        
        # Отправляем сообщение о транзакции в Telegram
        message = f"Transaction sent to {row['address']} for {row['amount']} USDT. Tx hash: {tx_hash}"
        bot.send_message(chat_id=bot_chatID, text=message)
        
    except TronException as e:
        # Если произошла ошибка при отправке транзакции, отправляем сообщение об ошибке в Telegram
        message = f"Error sending transaction to {row['address']}. Error message: {e}"
        bot.send_message(chat_id=bot_chatID, text=message)
