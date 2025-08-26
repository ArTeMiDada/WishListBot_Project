from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import WishListDirect.botManager.keyboard as kb
import WishListDirect.database.requests as rq
from handlers import users_cot
router1 = Router()

categsId = []

class Id_of_other_user(StatesGroup):
    id_user = State()


class create_category(StatesGroup):
    name = State()


class create_wish(StatesGroup):
    name = State()
    cost = State()
    description = State()



@router1.message(F.text == 'Посмотреть wishlist другого пользователя')
async def get_other_id(message: Message, state: FSMContext):
    await state.set_state(Id_of_other_user.id_user)
    await message.answer("Введите ID пользователя, wishlist которого хотите посмотреть")


@router1.message(Id_of_other_user.id_user)
async def get_other_id2(message: Message, state: FSMContext):
    await state.update_data(id_user=message.text)
    data = await state.get_data()
    try:
        await message.answer("Выберите категорию ",
                             reply_markup=await kb.catigories_other(await rq.get_categories(data['id_user'])))
    except:
        await message.answer("К сожелению такого айди не существует")


@router1.callback_query(F.data == "add_category")
async def add_category(callback: CallbackQuery, state: FSMContext):
    await state.set_state(create_category.name)
    await callback.answer("Вы должны ввести название категории")
    await callback.message.answer("Введите название категории")


@router1.message(create_category.name)
async def add_category2(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    some = await rq.add_category(data['name'], id_user=await rq.get_id_from_tgId(message.from_user.id))
    await message.answer("Категория создана", reply_markup=await kb.catigories(await rq.get_categories(
        await rq.get_id_from_tgId(message.from_user.id))))


@router1.callback_query(F.data == 'add_wish_call')
async def add_wish(callback: CallbackQuery, state: FSMContext):
    await state.set_state(create_wish.name)
    await callback.answer('Введите нужное имя')
    await callback.message.answer("Введите заголовок желания")


@router1.message(create_wish.name)
async def add_wish2(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(create_wish.description)
    await message.answer("Введите описание желания")


@router1.message(create_wish.description)
async def add_wish3(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(create_wish.cost)
    await message.answer("Введите стоимость желания")


@router1.message(create_wish.cost)
async def add_wish4(message: Message, state: FSMContext):
    await state.update_data(cost=message.text)
    data = await state.get_data()
    print(users_cot)
    id_us = await rq.get_id_from_tgId(message.from_user.id)
    await rq.add_wish(name=data['name'], cost=data['cost'], description=data['description'],
                      category=users_cot[id_us])
    users_cot.pop(id_us)
    await message.answer("Ваше желание успешно добавлено, выберите категорию", reply_markup=await kb.catigories(await rq.get_categories(id_us)))
