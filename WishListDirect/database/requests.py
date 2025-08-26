from WishListDirect.database.models import async_session
from WishListDirect.database.models import User, Category, Wish
from sqlalchemy import select, insert, text


async def set_user(tg_id) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def get_profile(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User.id).where(User.tg_id == tg_id))
        data = await session.scalar(select(User.reg_at).where(User.tg_id == tg_id))
    return user, data


async def get_id_from_tgId(tg_id):
    async with async_session() as session:
        id_us = await session.scalar(select(User.id).where(User.tg_id == tg_id))
    return id_us


async def get_categories(id_us):
    async with async_session() as session:
        categories = await session.scalars(select(Category).where(Category.user == id_us))
    if categories:
        return categories
    else:
        raise "К сожелению такого айди не существует"


async def add_category(name, id_user):
    async with async_session() as session:
        stmt = insert(Category).values(
            [
                {'name': f"{name}", 'user': f'{id_user}'}
            ]
        )
        await session.execute(stmt)
        await session.commit()


async def add_wish(name, cost, description, category):
    async with async_session() as session:
        stmt = insert(Wish).values(
            [
                {'name': f"{name}", 'cost': f'{cost}', 'description': f'{description}', 'category': f'{category}'}
            ]
        )
        await session.execute(stmt)
        await session.commit()


async def get_wishes(category_id):
    async with async_session() as session:
        wishes = await session.scalars(select(Wish).where(Wish.category == category_id))
    return wishes


async def delete_wish(id_wish):
    async with async_session() as session:
        await session.execute(text(f'DELETE FROM wishes WHERE id = {id_wish}'))
        await session.commit()


async def delete_category(id_category):
    async with async_session() as session:
        await session.execute(text(f'DELETE FROM wishes WHERE category = {id_category}'))
        await session.execute(text(f'DELETE FROM categories WHERE id = {id_category}'))
        await session.commit()
