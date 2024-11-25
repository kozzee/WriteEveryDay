import personal      #_____________________________________________________________________________________________Храню тут свои данные
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
import logging       #_____________________________________________________________________________________________Буду логировать все ошибки
import asyncio
import os            #_____________________________________________________________________________________________Прячу свои токены

API_TOKEN = os.getenv('API_TOKEN') #_______________________________________________________________________________Достаю токены из своей системы
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Настройка логирования
logging.basicConfig(level=logging.INFO)
# Токен вашего бота
API_TOKEN = personal.BOT_TOKEN

# Создание объектов Bot и Dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())     #__________________________________________________________________________________Ответ на команду /start
async def start_command(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}! Буду делать статьи для тебя раз в день!")

if __name__ == '__main__':      #___________________________________________________________________________________Запуск бота
    asyncio.run(dp.start_polling(bot))

