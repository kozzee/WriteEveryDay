from aiogram.types import KeyboardButton, ReplyKeyboardMarkup



def main_kb():
    kb = [
        [KeyboardButton(text="Запустить отправку статей")], 
        [KeyboardButton(text='Получить количество оставшихся токенов')]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return kb

