from aiogram import F, Router, types
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_to_cart, orm_add_user
from filters.chat_types import ChatTypeFilter
from handlers.menu_processing import get_menu_content
from kbds.inline import MenuCallBack
from kbds.reply import get_keyboard

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message, session: AsyncSession):
    media, reply_markup = await get_menu_content(session, level=0, menu_name='main')

    await message.answer_photo(media.media, caption=media.caption, reply_markup=reply_markup)


async def add_to_cart(callback: types.CallbackQuery, callback_data: MenuCallBack, session: AsyncSession):
    user = callback.from_user
    await orm_add_user(
        session,
        user_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=None,
    )
    await orm_add_to_cart(session, user_id=user.id, product_id=callback_data.product_id)
    await callback.answer('Товар добавлен в корзину.')


@user_private_router.callback_query(MenuCallBack.filter())
async def user_menu(callback: types.CallbackQuery, callback_data: MenuCallBack, session: AsyncSession):
    if callback_data.menu_name == 'add_to_cart':
        await add_to_cart(callback, callback_data, session)
        return

    media, reply_markup = await get_menu_content(
        session,
        level=callback_data.level,
        menu_name=callback_data.menu_name,
        category=callback_data.category,
        page=callback_data.page,
        product_id=callback_data.product_id,
        user_id=callback.from_user.id
    )

    await callback.message.edit_media(media=media, reply_markup=reply_markup)
    await callback.answer()


async def start_cmd(message: types.Message):
    await message.answer(
        text='This is command start!',
        reply_markup=get_keyboard(
            'Меню',
            'Отправить номер телефона',
            'Отправить локацию',
            placeholder='Что вас интересует?',
            request_contact=1,
            request_location=2,
        ),
    )


# @user_private_router.message(F.text.lower().contains('данные'))
# async def data_chat(message: types.Message):
#     data = message
#     chat_id = message.chat.id
#     print(data, '\n', 'chat_id = ', f'{chat_id}')
#
#     #await message.answer(str(data))
#     await message.answer(f'{message}')

# @user_private_router.callback_query(F.data.startswith('some_'))
# async def counter(callback: types.CallbackQuery):
#     number = int(callback.data.split('_')[-1])
#
#
#     await callback.message.edit_text(
#         text=f"Нажатий - {number}",
#         reply_markup=get_callback_btns(btns={
#             'Нажми еще раз': f'some_{number + 1}'
#         }))


# class MediaPhoto:
#     media_group_id = None
#     media_list = []
#
#
# @user_private_router.message(F.photo)
# async def echo_text(message: types.Message):
#
#     media_group_id = message.media_group_id
#     if message.media_group_id:
#         media_group_id = message.media_group_id
#         MediaPhoto.media_group_id = message.media_group_id
#
#         await message.answer('фото обработанно. ')
#     MediaPhoto.media_list.append(message.photo[-1].file_id)
#     return


# @user_private_router.message(CommandStart())
# async def start_cmd(message: types.Message):
#     await message.answer(
#         text='This is command start!',
#         reply_markup=get_keyboard(
#             'Меню',
#             'О магазине',
#             'Варианты оплаты',
#             'Варианты доставки',
#             placeholder='Что вас интересует?',
#             sizes=(2, 2)
#         ),
#     )


# #@user_private_router.message(F.text.lower().contains('купить'))
# @user_private_router.message(or_f(Command('menu'), (F.text.lower() == 'меню'), (F.text.lower().contains('купить'))))
# async def menu_cmd(message: types.Message, session: AsyncSession):
#     for product in await orm_get_products(session):
#         await message.answer_photo(
#             product.image,
#             caption=f"<strong>{product.name}\
#                     </strong>\n{product.description}\nСтоимость: {round(product.price, 2)}",
#         )
#     await message.answer('Вот меню')
#     # await message.answer(
#     #     text='Вот меню',
#     #     reply_markup=get_keyboard(
#     #         'Меню',
#     #         'О магазине',
#     #         'Варианты оплаты',
#     #         'Варианты доставки',
#     #         placeholder='Что вас интересует?',
#     #         sizes=(2, 2)
#     #     ),
#     # )


# @user_private_router.message((F.text.lower().contains('нас')) | (F.text.lower() == 'о нас') | (F.text.lower() == 'о магазине'))
# @user_private_router.message(Command('about'))
# async def about_cmd(message: types.Message):
#     await message.answer(
#         text='О нас: ',
#         reply_markup=get_keyboard(
#             'Меню',
#             'О магазине',
#             'Варианты оплаты',
#             'Варианты доставки',
#             placeholder='Что вас интересует?',
#             sizes=(2, 2)
#         ),
#     )
#
#
# @user_private_router.message((F.text.lower().contains('оплат')) | (F.text.lower() == 'варианты оплаты'))
# @user_private_router.message(Command('payment'))
# async def payment_cmd(message: types.Message):
#     text = as_marked_section(
#         Bold('Варианты оплаты:'),
#         "Картой в боте",
#         'При получении карта/нал',
#         'В заведении',
#         marker='✅☢ '
#     )
#     await message.answer(
#         text.as_html(),
#         reply_markup=get_keyboard(
#             'Меню',
#             'О магазине',
#             'Варианты оплаты',
#             'Варианты доставки',
#             placeholder='Что вас интересует?',
#             sizes=(2, 2)
#         ),
#     )
#
#
#
#
# @user_private_router.message((F.text.lower().contains('доставк')) | (F.text.lower() == 'варианты доставки'))
# @user_private_router.message(Command('shipping'))
# async def menu_cmd(message: types.Message):
#     text = as_list(
#         as_marked_section(
#             Bold('Варианты доставки/заказа:'),
#             "Курьер",
#             'Самовывоз (сейчас прибегу заберу)',
#             'Покушаю у вас (сейчас прибегу)',
#             marker='✅ '
#     ),
#         as_marked_section(
#             Bold('Нельзя:'),
#             "Почта",
#             'Голуби',
#             marker='❌ '
#         ),
#         sep='\n----------------------------------------\n'
#
#     )
#
#     await message.answer(
#         text.as_html(),
#         reply_markup=get_keyboard(
#             'Меню',
#             'О магазине',
#             'Варианты оплаты',
#             'Варианты доставки',
#             placeholder='Что вас интересует?',
#             sizes=(2, 2)
#         ),
#     )
#


# @user_private_router.message(F.text)
# async def echo(message: types.Message):
#     #print(message.photo)
#     print(message.from_user.id, message.from_user.first_name)
#     #print(message)
#
#     # if message.from_user.id == 699474992:
#     #     await message.answer(
#     #         f'Текст от пользователя ID:{message.from_user.id} имя: {message.from_user.first_name} сообщение: {message.text}'
#     #     )
#     #     # await message.answer(f'Дима ты послал {message.text}, а на самом деле на сервера ушло {message}')
#     # else:
#     #     await message.answer(
#     #         f'Текст от пользователя ID:{message.from_user.id} имя: {message.from_user.first_name} сообщение: {message.text}'
#     #     )
#         #await message.answer(f'Дима ты послал {message.text}, а на самом деле на сервера ушло {message}')
#     #await message.reply(message.photo)


# @user_private_router.message(F.text)
# async def echo_text(message: types.Message, bot):
#     await message.answer('echo_text')


# Сохранение стикера который прислали, отправка случайного стикера в ответ на стикер.
# @user_private_router.message(F.sticker)
# async def echo(message: types.Message, bot):
#     print(message.from_user.first_name)
#     sticker = message.sticker.file_id
#     #file_info = await bot.get_file(sticker)
#     #print(file_info, sticker)
#     # urllib.request.urlretrieve(f'http://api.telegram.org/file/bot{os.getenv('TOKEN')}/{file_info.file_path}',
#     #                            file_info.file_path)
#
#     async with aiofiles.open('stickers/sticker_id.txt', 'a', encoding='utf-8') as f:
#         await f.write(f"{sticker}\n")
#
#     # async with aiohttp.ClientSession() as session:
#     #     async with session.get(f'http://api.telegram.org/file/bot{os.getenv('TOKEN')}/{file_info.file_path}') as r:
#     #         content = await r.read()
#     # async with aiofiles.open(file_info.file_path, 'wb') as f:
#     #     await f.write(content)
#
#     async with aiofiles.open('stickers/sticker_id.txt', 'r', encoding='utf-8') as f:
#         stickers_id_list = await f.readlines()
#         stickers_id = [x[-16:] for x in stickers_id_list]
#         count = 0
#         # print(len(stickers_id_list))
#         # print(len(set(stickers_id_list)))
#         for i in set(stickers_id):
#             count += 1
#             print(stickers_id_list.count(i), i)
#         print(count)
#         # print('stickers_file', stickers_file)
#
#     if message.from_user.id == 699474992:
#         print(message.from_user.first_name, message.from_user.username)
#         await message.answer(message.from_user.first_name)
#         await message.answer_sticker(stickers_id_list[random.randint(0, len(stickers_id_list) - 1)].strip())
#
#     if message.from_user.id == 865805900:
#         await message.answer('Дима зацени мой стикер!!!')
#         await message.answer_sticker(stickers_id_list[random.randint(0, len(stickers_id_list) - 1)].strip())
#
#     if message.from_user.username == 'ELENAVETRE':
#         print(message)
#         await message.answer('❤❤❤Леночка!!! Ты прекрасна!!!😘😘😘😘 твой стикер великолепен!!!! Лови мой!')
#         await message.answer_sticker(stickers_id_list[random.randint(0, len(stickers_id_list) - 1)].strip())
#
#     if message.from_user.username == 'Plyuh_a':
#         await message.answer('❤❤❤Леночка!!! Ты прекрасна!!!😘😘😘😘 твой стикер великолепен!!!! Лови мой!')
#         await message.answer_sticker(stickers_id_list[random.randint(0, len(stickers_id_list) - 1)].strip())

# await bot.send_sticker(sticker_id)


@user_private_router.message(F.contact)
async def get_contact(message: types.Message):
    print(message.contact)
    await message.answer(f'Номер получен')
    await message.answer(str(message.contact))


@user_private_router.message(F.location)
async def get_location(message: types.Message):
    print(message.location)
    print(message)
    await message.answer(f'локация получена')
    await message.answer(str(message.location))
