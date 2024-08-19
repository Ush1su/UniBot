from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

spec = ["Computer Science", "Engineering", "Business", "Biology", "Arts", "Medicine"]
regions = ["USA", "UK", "Europe", "ASIA", "AUSTRALIA"]
after = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Advise more universities")], [KeyboardButton(text="Back to first choice", )]], resize_keyboard=True)


async def reply_spec():
    keyboard = ReplyKeyboardBuilder()
    for x in spec:
        keyboard.add(KeyboardButton(text=x, callback_data=x))
    keyboard.adjust(3).as_markup()
    markup = ReplyKeyboardMarkup(keyboard=keyboard.export(), resize_keyboard=True,
                                 input_field_placeholder="Choose specialisation you want to study",
                                 one_time_keyboard=True)
    return markup


async def reply_reg():
    keyboard = ReplyKeyboardBuilder()
    for x in regions:
        keyboard.add(KeyboardButton(text=x, callback_data=x))
    keyboard.adjust(3).as_markup()
    markup = ReplyKeyboardMarkup(keyboard=keyboard.export(), resize_keyboard=True,
                                 input_field_placeholder="Choose region where you wanna study",
                                 one_time_keyboard=True)
    return markup

sch = ["Necessary", "Not matter"]
get_scholarship = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Necessary"),
                                                 KeyboardButton(text="Not matter")]],
                                      resize_keyboard=True, input_field_placeholder="Importance of scholarship", one_time_keyboard=True)
