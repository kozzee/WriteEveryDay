from gigachat import GigaChat
import os, random

API_TOKEN = os.getenv('API_TOKEN')

prompt_for_list = ('Предложи несколько уникальных, интересных и актуальных тем для статей на Яндекс.Дзен, '
 'связанных с геймингом, кино, наукой, технологиями. Можно добавлять различные подборки приложений, кино и игр.'
 'Все темы должны быть представлены в одной строке, разделенной символом "|". '
 'Например: "тема1|тема2|тема3|тема4|тема5". Не добавляй никаких лишних слов, строго только темы.')

prompt_for_article = "Вот несколько пожеланий к статье: Объем: Около 3000-4000 символов. Стиль: Неформальный, conversational, но грамотный. Структура: Введение, основная часть (разделенная на подзаголовки), заключение. Визуальный контент: Предложи несколько идей для иллюстраций (фото, скриншоты, гифки). Ссылки: Добавь ссылки на достоверные источники информации, если это необходимо. Не забудь сделать статью увлекательной и заставить читателей хотеть узнать больше! "


async def create_article(): # Генерируем список статей на день

    with GigaChat(credentials=API_TOKEN, verify_ssl_certs=False) as giga:
                response = giga.chat(prompt_for_list)
    themes = response.choices[0].message.content.strip().split('-')
    return themes


def choose_random_theme(themes):
    return random.choice(themes)


async def generate_article(theme):
    with GigaChat(credentials=API_TOKEN, verify_ssl_certs=False) as giga:
        response = giga.chat(f'Напиши статью на тему [{theme}]. {prompt_for_article}')
    article = response.choices[0].message.content
    return article
