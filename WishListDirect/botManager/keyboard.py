from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Профиль"), KeyboardButton(text="Посмотреть wishlist другого пользователя")],
    [KeyboardButton(text="Список желаний")]
], resize_keyboard=True, input_field_placeholder="Выберите пункт меню")


async def catigories(list_of_cat):
    all_cat = list_of_cat
    keyboard = InlineKeyboardBuilder()
    for cat in all_cat:
        keyboard.add(InlineKeyboardButton(text=cat.name, callback_data=f"category_{cat.id}"))
    keyboard.add(InlineKeyboardButton(text="Добавить категорию", callback_data="add_category"))
    keyboard.add(InlineKeyboardButton(text="Удалить категорию и все желания в ней", callback_data="delete_category"))
    keyboard.add(InlineKeyboardButton(text="На главную", callback_data="to_main"))
    return keyboard.adjust(1).as_markup()


add_categ = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить желание", callback_data="add_wish_call"), InlineKeyboardButton(text="Удалить желание", callback_data="delete_wish")],
    [InlineKeyboardButton(text="Главное меню", callback_data="to_main")]
])


add_categ_other = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Главное меню", callback_data="to_main")]
])


async def catigories_other(list_of_cat):
    all_cat = list_of_cat
    keyboard = InlineKeyboardBuilder()
    for cat in all_cat:
        keyboard.add(InlineKeyboardButton(text=cat.name, callback_data=f"categoryO_{cat.id}"))
    keyboard.add(InlineKeyboardButton(text="На главную", callback_data="to_main"))
    return keyboard.adjust(1).as_markup()


async def wish_get_list(get_lists):
    all_wishes = get_lists
    keyboard = InlineKeyboardBuilder()
    for w in all_wishes:
        keyboard.add(InlineKeyboardButton(text=f"{w.name}", callback_data=f"wish_{w.id}"))
    keyboard.add(InlineKeyboardButton(text="На главную", callback_data="to_main"))
    return keyboard.adjust(2).as_markup()


async def catigories_del(list_of_cat):
    all_cat = list_of_cat
    keyboard = InlineKeyboardBuilder()
    for cat in all_cat:
        keyboard.add(InlineKeyboardButton(text=cat.name, callback_data=f"categoryD_{cat.id}"))
    keyboard.add(InlineKeyboardButton(text="На главную", callback_data="to_main"))
    return keyboard.adjust(2).as_markup()
