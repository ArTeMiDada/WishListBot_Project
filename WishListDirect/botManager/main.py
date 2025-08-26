from config import TOKEN
from aiogram import Dispatcher, Bot
from asyncio import run
from handlers import router
from WishListDirect.database.models import async_main
from FSM_con import router1
from aiogram.fsm.storage.memory import MemoryStorage

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


async def main():
    await async_main()
    dp.include_routers(router, router1)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
    except RuntimeError:
        print("Соеденение разорвано")
