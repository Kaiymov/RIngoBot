from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from db.sqlite import get_users, delete_user, check_id, get_user
from config import ADMIN

from keyboard.inline_kb import yes_no_user
from keyboard.reply_kb import admin_table, cancel_save


# DELETE USER STATE
class DeleteUserStateGroup(StatesGroup):
    user_id = State()


# commands=['get_users']
async def cmd_get_users(message: types.Message):
    if message.from_user.id in ADMIN:
        try:
            await message.answer(text=await get_users(), parse_mode='HTML')
            await message.delete()
        except:
            await message.answer(text='Нет запросов')


# commands=['delete_user']
async def cmd_delete_user(message: types.Message):
    if message.from_user.id in ADMIN:
        await message.answer(text='Готов к удалению укажите user_id\n\n'
                                  f'{await get_users()}',
                             reply_markup=cancel_save(), parse_mode='HTML')
        await DeleteUserStateGroup.user_id.set()


# STATE=DeleteUserStateGroup.user_id
async def state_delete_user(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        user_id = int(message.text)
        if user_id in await check_id():
            async with state.proxy() as data:
                data['id'] = user_id

            user_info = await get_user(data['id'])

            await message.answer(text=f'Вы уверены что хотите удалить?\n\n'
                                      f'{user_info}', reply_markup=yes_no_user(), parse_mode='HTML')

        else:
            await message.reply('Нет в БД', reply_markup=admin_table())
            await state.finish()
    else:
        await message.reply(text='Number mal')


# CALLBACK DELETE USER YES OR NO
async def callback_delete(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'yes':
        async with state.proxy() as data:
            user_id = data['id']

        await delete_user(user_id)

        await state.finish()
        await callback.answer(text='Успешно удален')
        await callback.message.answer(text='АДМИНКА!', reply_markup=admin_table())
    elif callback.data == 'no':
        await state.finish()
        await callback.answer(text='Прервали удаление')
        await callback.message.answer(text='АДМИНКА!', reply_markup=admin_table())


# IMPORT MAIN
def admin_handler(dp: Dispatcher):
    # ADMIN COMMAND
    dp.register_message_handler(cmd_get_users, commands=['get_users'])
    dp.register_message_handler(cmd_delete_user, commands='delete_user')
    dp.register_message_handler(state_delete_user, state=DeleteUserStateGroup.user_id)
    # CALLBACK
    dp.register_callback_query_handler(callback_delete, state=DeleteUserStateGroup.user_id)
