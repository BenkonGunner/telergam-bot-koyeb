from telegram import Update
from telegram.ext import Application, CommandHandler

# Замените на свой токен API, который вы получили от BotFather
API_KEY = 'your_telegram_bot_api_key'

# Функция, которая будет вызываться при отправке команды /start
async def start(update: Update, context):
    await update.message.reply_text("Привет! Добро пожаловать в наш бот! Как я могу помочь?")

def main():
    # Инициализация бота с твоим API-ключом
    application = Application.builder().token(API_KEY).build()

    # Настройка обработчика команды /start
    application.add_handler(CommandHandler("start", start))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
