from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
import WishListDirect.database.requests as rq
import WishListDirect.botManager.keyboard as kb

router = Router()
users = {}
users_cot = {}

@router.message(CommandStart())
async def start_c(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer("Добрый день, это бот, который записывает ваши желания!! Вы успешно зашли в свой профиль"
                         , reply_markup=kb.main)


@router.message(F.text == "Профиль")
async def profile(message: Message):
    id_user, data_user = await rq.get_profile(message.from_user.id)
    await message.answer(f"Профиль\nДата регистрации: {data_user} (по МСК -3) \nID: {id_user}")


@router.message(F.text == "Список желаний")
async def get_categ(message: Message):
    users[message.chat.id] = await rq.get_id_from_tgId(message.from_user.id)
    id_us = users[message.chat.id]
    categs = await rq.get_categories(id_us)
    await message.answer("Выберите или создайте категорию!", reply_markup=await kb.catigories(categs))


@router.callback_query(F.data == 'to_main')
async def to_main(callback: CallbackQuery):
    await callback.message.delete()


@router.callback_query(F.data.startswith("category_"))
async def get_wishes(callback: CallbackQuery):
    users_cot[users[callback.message.chat.id]] = int(callback.data.split('_')[1])
    wishes = await rq.get_wishes(int(callback.data.split('_')[1]))
    ret = ''
    for w in wishes:
        ret += f'Желание: {w.name}\nОписание: {w.description}\nСтоимость: {w.cost}\n\n'
    if len(ret) == 0:
        ret = "К сожелению желаний нету"
    await callback.message.edit_text(ret, reply_markup=kb.add_categ)


@router.callback_query(F.data == 'delete_wish')
async def wh_delete_wish(callback: CallbackQuery):
    await callback.message.edit_text("Какое желание вы хотите удалить? ",
                                     reply_markup=await kb.wish_get_list(await rq.get_wishes(users_cot[users[callback.message.chat.id]])))


@router.callback_query(F.data.startswith("wish_"))
async def delete_wish(callback: CallbackQuery):
    await rq.delete_wish(int(callback.data.split('_')[1]))
    await callback.message.edit_text("Желание успешно удалено")


@router.callback_query(F.data.startswith("categoryO_"))
async def get_wishes0(callback: CallbackQuery):
    wishes = await rq.get_wishes(int(callback.data.split('_')[1]))
    users_cot[users[callback.message.chat.id]] = int(callback.data.split('_')[1])
    ret = ''
    for w in wishes:
        ret += f'Желание: {w.name}\nОписание: {w.description}\nСтоимость: {w.cost}\n\n'
    if len(ret) == 0:
        ret = "К сожелению желаний нету"
    await callback.message.edit_text(ret, reply_markup=kb.add_categ_other)


@router.callback_query(F.data == 'delete_category')
async def wh_delete_categ(callback: CallbackQuery):
    await callback.message.edit_text("Какую категорию вы хотите удалить? ", reply_markup=await kb.catigories_del(
        await rq.get_categories(await rq.get_id_from_tgId(callback.from_user.id))))


@router.callback_query(F.data.startswith("categoryD_"))
async def delete_categ(callback: CallbackQuery):
    await rq.delete_category(int(callback.data.split("_")[1]))
    await callback.message.edit_text("Категория успешно удалена! ")
