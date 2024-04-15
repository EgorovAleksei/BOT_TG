import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from database.engine import create_db, session_maker
from handlers.admin_private import admin_router
from handlers.user_group import user_group_router
from handlers.user_private import user_private_router
from middlewares.db import DataBaseSession

#from middlewares.db import CounterMiddleware


# from common.bot_cmds_list import private

#ALLOWED_UPDATES = ['message', 'edited_message', 'callback_query']

bot = Bot(token=os.getenv('TOKEN'), parse_mode=ParseMode.HTML)
bot.my_admins_list = []
dp = Dispatcher()

# Мидллвере которые срабатывает раньше всех. над всеми.
# https://youtu.be/osg6WUc1EN4?t=817
#dp.update.outer_middleware(CounterMiddleware())

#admin_router.message.middleware(CounterMiddleware())

dp.include_router(user_private_router)
dp.include_router(user_group_router)
dp.include_router(admin_router)


async def on_startup(bot):
    #await drop_db()
    await create_db()


async def on_shutdown(bot):
    print('бот прилег')


async def main():
    logging.basicConfig(level=logging.INFO)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    #await create_db()
    await bot.delete_webhook(drop_pending_updates=True)
    #await bot.set_my_commands(commands=private, scope=BotCommandScopeAllPrivateChats())
    #await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    #await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

asyncio.run(main())
