import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from flask import Flask
import threading
import asyncio

# Загрузка переменных окружения
load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return "OK"

def run_flask():
    print("Flask сервер запущен на http://0.0.0.0:8000")
    app.run(host="0.0.0.0", port=8000, use_reloader=False)  # Убираем reloader для работы на Koyeb

# Запуск Flask в отдельном потоке
threading.Thread(target=run_flask, daemon=True).start()

# Твой API-ключ от BotFather
API_KEY = os.getenv("BOT_TOKEN")

# ID группы, в которой бот разрешен
GROUP_ID = int(os.getenv("GROUP_ID"))

# Ссылка на форму Airtable
form_url = "https://airtable.com/app20FIZVkuqrfYCG/pagi3f25jJR4rmWeg/form"

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

def main():
    application = Application.builder().token(API_KEY).build()

    # Добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Запуск polling в асинхронном режиме
    asyncio.run(application.run_polling())

if __name__ == '__main__':
    print("Запуск приложения")
    # Запускаем Telegram-бота и Flask в отдельных потоках
    threading.Thread(target=main, daemon=True).start()
