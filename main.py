import personal, logging, os, asyncio, random    #_____________________________________________________________________________________________persional - Храню тут свои данные

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from gigachat import GigaChat
from apscheduler.schedulers.asyncio import AsyncIOScheduler


# Достаю нужные API из системы
API_TOKEN = os.getenv('API_TOKEN') 
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
    scheduler.add_job(daily_reminder, 'cron', day_of_week='mon-fri', hour=19, minute=29) #__________________________Вываолняет функцию в 12.00   по будням
    await message.reply(f"Привет, {message.from_user.full_name}! Буду присылать тебе статьи каждый рабочий день.")



async def create_article(): # Генерируем список статей на день

    with GigaChat(credentials=API_TOKEN, verify_ssl_certs=False) as giga:
                response = giga.chat(personal.prompt_for_list)
    #str_artcile = response.choices[0].message.content
    themes = response.choices[0].message.content.strip().split('-')

    # Просто уведомление об ошибке
    # if "|" not in str_artcile and "-" not in str_artcile:
    #     await bot.send_message(chat_id=ID_CHAT, text="Темы статей не разделены")
    #     await bot.send_message(chat_id=ID_CHAT, text=str_artcile)
    #     raise ValueError("Темы статей не разделены символом '|'")
    # theme_article = random.choice(str_artcile.split("-"))
    return themes


# Выбор случайной темы из списка
def choose_random_theme(themes):
    return random.choice(themes)


async def generate_article(theme):
    with GigaChat(credentials=API_TOKEN, verify_ssl_certs=False) as giga:
        response = giga.chat(f'Напиши статью на тему [{theme}]. {personal.prompt_for_article}')
    article = response.choices[0].message.content
    return article


# Ежедневная отправка сообщения
async def daily_reminder():
    try:
        themes = await create_article()
        chosen_theme = choose_random_theme(themes)
        article = await generate_article(chosen_theme)
        await bot.send_message(ID_CHAT, f'Сегодня статья на тему: **{chosen_theme}**\n\n{article}')
    except Exception as e:
        logging.error(f'Ошибка при выполнении задачи: {e}')
        await bot.send_message(ID_CHAT, f'Ошибув при выполнении задачи: {e}')

    # with GigaChat(credentials=API_TOKEN, verify_ssl_certs=False) as giga:
    #     selected_theme = await create_article()
    #     response = giga.chat(f'Я выбрал тему для статьи из твоих предложений: [{selected_theme}]. {personal.prompt_for_article}')
    #     article = response.choices[0].message.content
    #await bot.send_message(chat_id=ID_CHAT, text=article)





# if __name__ == '__main__':      
#     scheduler.start()
#     asyncio.run(dp.start_polling(bot))


# if __name__ == "__main__":#___________________________________________________________________________________Запуск бота и планировщик
#     async def run_bot_and_scheduler():
#         scheduler.start()
#         await dp.start_polling(bot)

#     asyncio.run(run_bot_and_scheduler())
if __name__ == "__main__":
    async def main():
        scheduler.start()
        await dp.start_polling(bot)

    asyncio.run(main())