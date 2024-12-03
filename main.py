import logging, os, asyncio   #_____________________________________________________________________________________________persional - Храню тут свои промпты

from Giga import generate_article, create_article, choose_random_theme 
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from gigachat import GigaChat
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from UI_keyboard import main_kb


# Достаю нужные API из системы 
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Настройка логирования
logging.basicConfig(level=logging.INFO)


# Создание объектов Bot и Dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher() 
scheduler = AsyncIOScheduler()



# Обработка /start
@dp.message(CommandStart())
async def start_command(message: Message):
    global ID_CHAT #сделал глобальной, чтобы достать из других функций
    ID_CHAT = message.from_user.id
    scheduler.add_job(daily_reminder, 'cron', day_of_week='mon-fri', hour=12, minute=00) #____________________________________Выполняет функцию в 12.00   по будням
    await message.answer(f"Привет, {message.from_user.full_name}! Буду присылать тебе статьи каждый рабочий день.", reply_markup=main_kb())


# Ежедневная отправка сообщения
async def daily_reminder():
    try:
        themes = await create_article()
        chosen_theme = choose_random_theme(themes)
        article = await generate_article(chosen_theme)
        await bot.send_message(ID_CHAT, f'Сегодня статья на тему: **{chosen_theme}**\n\n{article}')
    except Exception as e:
        logging.error(f'Ошибка при выполнении задачи: {e}')
        await bot.send_message(ID_CHAT, f'Ошибка при выполнении задачи: {e}')


if __name__ == "__main__":
    async def main():
        scheduler.start()
        await dp.start_polling(bot)

    asyncio.run(main())