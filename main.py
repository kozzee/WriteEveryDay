import personal, logging, os, asyncio, schedule, time, random      #_____________________________________________________________________________________________persional - Храню тут свои данные
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from gigachat import GigaChat
from apscheduler.schedulers.asyncio import AsyncIOScheduler



API_TOKEN = os.getenv('API_TOKEN') #_______________________________________________________________________________Достаю токены из своей локальной системы
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Настройка логирования
logging.basicConfig(level=logging.INFO)
# Создание объектов Bot и Dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher() 
scheduler = AsyncIOScheduler()


def create_article():
    with GigaChat(credentials=API_TOKEN, verify_ssl_certs=False) as giga:
                response = giga.chat(f'{personal.prompt_for_list}')
    str_artcile = response.choices[0].message.content
    if "|" not in str_artcile:
        raise ValueError("Темы статей не разделены символом '|'")
    theme_article = random.choice(str_artcile.split("|"))
    return theme_article


async def daily_reminder():
    with GigaChat(credentials=API_TOKEN, verify_ssl_certs=False) as giga:
                response = giga.chat(f'Я выбрал тему для статьи из твоих предложений: [{create_article}]". {personal.prompt_for_article}')
                article = response.choices[0].message.content
    await bot.send_message(chat_id="@kozee_qrinder", text=article)




@dp.message(CommandStart())     #__________________________________________________________________________________Ответ на команду /start
async def start_command(message: Message):
    scheduler.add_job(daily_reminder, 'cron', day_of_week='mon-fri', hour=12, minute=0) #__________________________Вываолняет функцию в 12.00   по будням
    await message.answer(f"Привет, {message.from_user.first_name}! Буду делать статьи для тебя раз в день!")

# if __name__ == '__main__':      
#     scheduler.start()
#     asyncio.run(dp.start_polling(bot))


if __name__ == "__main__":#___________________________________________________________________________________Запуск бота и планировщик
    async def run_bot_and_scheduler():
        scheduler.start()
        await dp.start_polling(bot)

    asyncio.run(run_bot_and_scheduler())