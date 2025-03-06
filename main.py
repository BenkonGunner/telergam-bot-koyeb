import os
import logging
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from flask import Flask, request
import threading

# Загружаем переменные окружения
load_dotenv()

# Инициализация Flask
app = Flask(__name__)

# Инициализация Telegram бота
API_KEY = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))
form_url = "https://airtable.com/app20FIZVkuqrfYCG/pagi3f25jJR4rmWeg/form"

# Настройка логирования для Telegram
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Устанавливаем Webhook
@app.route('/' + API_KEY, methods=["POST"])
def webhook():
    json_str = request.get_data(as_text=True)
    update = Update.de_json(json_str, application.bot)
    application.process_update(update)
    return "OK", 200

# Запуск Flask в отдельном потоке
def run_flask():
    app.run(host="0.0.0.0", port=8000)

threading.Thread(target=run_flask, daemon=True).start()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if not chat:
        print("❌ Ошибка: update.effective_chat = None")
        return

    chat_id = chat.id
    chat_type = chat.type  # Тип чата (group, supergroup, private)

    print(f"📌 Бот получил команду в чате {chat_id} (тип: {chat_type})")

    if chat_type in ["group", "supergroup"]:
        if chat_id == GROUP_ID:
            print("✅ Доступ разрешён!")
            keyboard = [[InlineKeyboardButton("Заполнить форму о рейсе", url=form_url)]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await context.bot.send_message(
                chat_id=chat_id,
                text="✅ Привет, член группы! Для заполнения формы нажмите кнопку ниже:",
                reply_markup=reply_markup
            )
        else:
            print(f"🚫 Доступ запрещён! (Чат ID: {chat_id} не совпадает с {GROUP_ID})")
            await context.bot.send_message(chat_id=chat_id, text="❌ У вас нет доступа к этому боту.")
    else:
        print(f"🚫 Бот получил команду в ЛИЧНОМ чате (ID: {chat_id}). ОТКАЗАНО!")
        await context.bot.send_message(chat_id=chat_id, text="❌ Используйте бота только в группе!")

# Функция для запуска приложения
def main():
    # Создаем приложение для бота
    global application
    application = Application.builder().token(API_KEY).build()

    application.add_handler(CommandHandler("start", start))

    # Устанавливаем webhook
    application.bot.set_webhook(f"certain-ardelis-novagroup-1a591a04.koyeb.app/{API_KEY}")

    # Запускаем Flask сервер (обработку webhook)
    run_flask()

if __name__ == '__main__':
    main()
