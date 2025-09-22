from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from keyboards.all_kb import main_kb,b_models,works_edit_kb,works_groups,return_works_kb,m_or_e_kb,add_spares,spares_list_for_work,to_delete_work,edit_work,deleting_works
from aiogram.fsm.context import FSMContext
import pandas as pd
from utils.info import info
from utils.dataframes import df
from .start import init_work
from create_bot import Form

works_router = Router()

@works_router.message(F.text == "➕ Добавить работу")
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("Добавление работы")
    await state.set_state(Form.find_work)
    await message.reply("Выбери вид работы:", reply_markup=works_groups(await state.get_data(), df))
    await state.set_state(Form.find_work)
@works_router.message(F.text=="🗑 Удалить работу",Form.remont_edit)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("Удалить работу")
    data = await state.get_data()
    if message.text == '❌ Отмена':
        await init_work(state, message)
        return
    if len(data['works']):
        await message.reply("Что удалить?", reply_markup=deleting_works(await state.get_data()))
        await state.set_state(Form.deleting_work)
    else:
        await message.answer('Работ и так нет.')
        await state.set_state(Form.remont_edit)
        await message.answer(await info(state), reply_markup=works_edit_kb())

@works_router.message(F.text,Form.deleting_work)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("Удаление ремонта")
    data = await state.get_data()
    if '| 'in message.text and  message.text.split('| ')[1] in  data['works']:
        data['works'].remove(message.text.split('| ')[1])
        await message.answer(await info(state), reply_markup=works_edit_kb())
        await state.set_state(Form.next_menu)
    else:
        await message.answer('Нет такой работы')
        await state.set_state(Form.remont_edit)
        await message.answer(await info(state), reply_markup=works_edit_kb())

@works_router.message(F.text,Form.find_work)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("поиск работы")
    if message.text=='❌ Отмена':
        await state.set_state(Form.next_menu)
        await message.answer('хих',reply_markup=works_edit_kb())
        return
    if message.text in df[df['type']==await state.get_value('m_or_e')].group.unique():
        await state.update_data(last_group=message.text)
        await state.set_state(Form.add_work)
        await message.reply("Выбери работу:",reply_markup=return_works_kb(await state.get_data(),df))
    else:
        await message.reply("Выбери вид работы:", reply_markup=works_groups(await state.get_data(),df))
        await state.set_state(Form.find_work)
#ДОБАВЛЕНИЕ РАБОТЫ
@works_router.message(F.text,Form.add_work)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("добавление работы")
    data = await state.get_data()
    if message.text in df.loc[((df['group']==data['last_group'])&(df['type']==data['m_or_e']))]['works'].unique():
        data['works'].append(message.text)
        data['norm_time'].append(float(
            df.loc[((df['group']==data['last_group'])&
                    (df['type']==data['m_or_e'])&
                    (df['works']==message.text))]['time'].iloc[0]))
        await state.update_data(data=data)
        await state.set_state(Form.getting_spare)
        await message.answer("Введи зч", reply_markup=spares_list_for_work())
    else:
        await message.reply("Выбери вид работы:", reply_markup=works_groups(data,df))
        await state.set_state(Form.find_work)

