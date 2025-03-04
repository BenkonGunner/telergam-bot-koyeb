from telegram.ext import Application, CommandHandler, ContextTypes

# Замените на свой токен API, который вы получили от BotFather
API_KEY = '8160940951:AAHJh1V2oTrXrnD-dezCR1Zp27ktAaU5X3Y'

# Функция, которая будет вызываться при отправке команды /start
async def start(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! С помощью этого бота можно внести информацию о рейсах!")

def main():
    # Инициализация бота с твоим API-ключом
    application = Application.builder().token(API_KEY).build()

    # Настройка обработчика команды /start
    application.add_handler(CommandHandler("start", start))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
