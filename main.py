import os
from dotenv import load_dotenv
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Загружаем переменные окружения
load_dotenv()

# Инициализация бота
API_KEY = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))
form_url = "https://airtable.com/app20FIZVkuqrfYCG/pagi3f25jJR4rmWeg/form"
webhook_url = "certain-ardelis-novagroup-1a591a04.koyeb.app/"  # замените на свой URL из Koyeb

# Устанавливаем webhook
bot = Bot(token=API_KEY)
bot.set_webhook(url=webhook_url)

# 📌 Команда /start
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
    # Создаем приложение для бота
    application = Application.builder().token(API_KEY).build()
    application.add_handler(CommandHandler("start", start))

    # Запускаем webhook для получения обновлений
    application.run_webhook(listen="0.0.0.0", port=443, url_path='YOUR_URL')

if __name__ == '__main__':
    main()
