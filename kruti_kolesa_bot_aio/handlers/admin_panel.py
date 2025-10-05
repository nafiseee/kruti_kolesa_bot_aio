from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from keyboards.all_kb import main_kb, b_models, works_edit_kb, works_groups, return_works_kb, m_or_e_kb, \
    add_spares, spares_list_for_work, return_spares_group, return_spares, deleting_spares,admin_buttons
from aiogram.fsm.context import FSMContext
from db_handler.db_class import get_remonts
import pandas as pd
from utils.info import info,info_all_times
from utils.dataframes import df, df_spares
from create_bot import Form
from create_bot import bot
from db_handler.db_class import get_my_time,get_times_all,get_lost_spares
from aiogram.types.input_file import FSInputFile
admin_router = Router()


@admin_router.message(F.text=='⚙️ Админ панель') #НАЧАЛО
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    await message.answer("Что делаем?:", reply_markup=admin_buttons())
    await state.set_state(Form.admin)
@admin_router.message(F.text == 'Норма часы всех',Form.admin)  # НАЧАЛО
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    await message.answer(await info_all_times(await get_times_all()),reply_markup=main_kb(message.from_user.id))
    await state.set_state(Form.client_start)
@admin_router.message(F.text == 'Использованные зч',Form.admin)  # НАЧАЛО
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    if await get_lost_spares():
        await message.answer("Использованные запчасти:", reply_markup=main_kb(message.from_user.id))
        document = FSInputFile('temporary_folder/lost_spares1.xlsx')
        await bot.send_document(message.chat.id, document)
        document = FSInputFile('temporary_folder/lost_spares2.xlsx')
        await bot.send_document(message.chat.id, document)
    await state.set_state(Form.client_start)



