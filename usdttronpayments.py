import telegram
import pandas as pd
from pytron import Tron
from pytron.exceptions import TronException

# Устанавливаем параметры для подключения к Telegram API
bot_token = 'YOUR_BOT_TOKEN'
bot_chatID = 'YOUR_CHAT_ID'
allowed_contact = 'ALLOWED_CONTACT_USERNAME'

# Устанавливаем параметры для подключения к сети Tron
tron = Tron()
tron.private_key = 'YOUR_PRIVATE_KEY'
tron.default_address = 'YOUR_DEFAULT_ADDRESS'
fee_limit = 10000000 # Устанавливаем лимит комиссии

# Загружаем данные из CSV-файла
data = pd.read_csv('wallets.csv')

# Создаем Telegram-бота
bot = telegram.Bot(token=bot_token)

# Функция для проверки контакта
def is_allowed_contact(update):
    return update.message.chat.username == allowed_contact

# Обрабатываем входящие сообщения от определенного контакта
def handle_message(update, context):
    if not is_allowed_contact(update):
        return

    # Отправляем транзакцию USDT на каждый кошелек из таблицы
    for index, row in data.iterrows():
        try:
            # Отправляем транзакцию USDT
            tx_hash = tron.trx.transfer(row['address'], row['amount'], 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t', fee_limit=fee_limit)

            # Отправляем сообщение о транзакции в Telegram
            message = f"Transaction sent to {row['address']} for {row['amount']} USDT. Tx hash: {tx_hash}"
            bot.send_message(chat_id=bot_chatID, text=message)

        except TronException as e:
            # Если произошла ошибка при отправке транзакции, отправляем сообщение об ошибке в Telegram
            message = f"Error sending transaction to {row['address']}. Error message: {e}"
            bot.send_message(chat_id=bot_chatID, text=message)

# Создаем обработчик входящих сообщений
updater = telegram.ext.Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

# Регистрируем функцию обработки входящих сообщений
dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))

# Запускаем бота
updater.start_polling()
updater.idle()