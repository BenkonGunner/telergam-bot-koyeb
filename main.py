import os
from dotenv import load_dotenv

load_dotenv()

from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

# 🔑 Твой API-ключ от BotFather
API_KEY = os.getenv("BOT_TOKEN")

# 🔒 ID группы, в которой бот разрешен (замени на ID своей группы)
GROUP_ID = int(os.getenv("GROUP_ID"))  # Укажи реальный ID группы

# 📌 Ссылка на форму Airtable (замени на свою ссылку)
form_url = "https://airtable.com/app20FIZVkuqrfYCG/pagi3f25jJR4rmWeg/form"

# 📩 Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if not chat:
        print("❌ Ошибка: update.effective_chat = None")
        return

    chat_id = chat.id
    chat_type = chat.type  # Тип чата (group, supergroup, private)

    print(f"📌 Бот получил команду в чате {chat_id} (тип: {chat_type})")

    # Проверяем, является ли чат группой
    if chat_type in ["group", "supergroup"]:
        if chat_id == ALLOWED_GROUP_ID:
            print("✅ Доступ разрешён!")
            keyboard = [[InlineKeyboardButton("Заполнить форму о рейсе", url=form_url)]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await context.bot.send_message(
                chat_id=chat_id,
                text="✅ Привет, член группы! Для заполнения формы нажмите кнопку ниже:",
                reply_markup=reply_markup
            )
        else:
            print(f"🚫 Доступ запрещён! (Чат ID: {chat_id} не совпадает с {ALLOWED_GROUP_ID})")
            await context.bot.send_message(chat_id=chat_id, text="❌ У вас нет доступа к этому боту.")

    else:
        print(f"🚫 Бот получил команду в ЛИЧНОМ чате (ID: {chat_id}). ОТКАЗАНО!")
        await context.bot.send_message(chat_id=chat_id, text="❌ Используйте бота только в группе!")

# 📌 Команда /get_id (проверяем, какой ID бот видит)
async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat:
        await context.bot.send_message(chat_id=chat.id, text=f"📌 ID этой группы: {chat.id}")
        print(f"✅ Получен ID группы: {chat.id}")  # Лог в консоль Replit

def main():
    application = Application.builder().token(API_KEY).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_id", get_id))

    application.run_polling()

if __name__ == '__main__':
    main()
