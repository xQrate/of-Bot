import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Укажите токен вашего бота
TELEGRAM_BOT_TOKEN = '' #пример апи
# Укажите ваш идентификатор пользователя
AUTHORIZED_USER_ID =   # Замените на ваш ID

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Команда для выключения ПК
async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id

    # Проверка авторизации
    if user_id != AUTHORIZED_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="У вас нет прав для выполнения этой команды.")
        logger.warning(f"Unauthorized shutdown attempt by user ID: {user_id}.")
        return

    logger.info(f"Received shutdown command from {update.message.from_user.username}.")

    # Подтверждение действия пользователю
    await context.bot.send_message(chat_id=chat_id, text="Выключаю компьютер...")

    # Выключение компьютера в зависимости от ОС
    try:
        if os.name == 'nt':  # Для Windows
            os.system("shutdown /s /t 1")
        else:  # Для Linux и macOS
            os.system("sudo shutdown -h now")
    except Exception as e:
        logger.error(f"Ошибка при попытке выключить ПК: {e}")
        await context.bot.send_message(chat_id=chat_id, text=f"Произошла ошибка: {e}")

# Команда для начала работы бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    logger.info(f"Bot started by {update.message.from_user.username}.")
    await context.bot.send_message(chat_id=chat_id, text="Привет! Я бот для выключения компьютера. Отправьте /shutdown, чтобы выключить ПК.")

# Основная функция для запуска бота
async def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("shutdown", shutdown))

    # Запускаем бота
    print("Бот запущен. Нажмите Ctrl+C для завершения.")
    await application.run_polling()

if __name__ == '__main__':
    import asyncio

    # Запускаем основной цикл событий
    asyncio.run(main())
