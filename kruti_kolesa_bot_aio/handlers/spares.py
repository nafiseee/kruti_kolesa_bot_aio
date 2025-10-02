from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from keyboards.all_kb import main_kb, b_models, works_edit_kb, works_groups, return_works_kb, m_or_e_kb,\
    add_spares,spares_list_for_work,return_spares_group,return_spares,deleting_spares
from aiogram.fsm.context import FSMContext
import pandas as pd
from utils.info import info
from utils.dataframes import df,df_spares
from create_bot import Form



spares_router = Router()


@spares_router.message(F.text=='➕ Добавить запчасть',Form.next_menu)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("Добавить зч")
    await state.set_state(Form.getting_spare_)
    await message.answer("Введи зч", reply_markup=spares_list_for_work())

@spares_router.message(F.text=="🗑 Удалить запчасть",Form.remont_edit)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("удалить запчасть")
    data = await state.get_data()
    if len(data['spares']):
        await message.reply("Что удалить?", reply_markup=deleting_spares(await state.get_data()))
        await state.set_state(Form.deleting_spares)
    else:
        await message.answer('Запчастей и так нет.')
        await state.set_state(Form.remont_edit)
        await message.answer(await info(state), reply_markup=works_edit_kb())

@spares_router.message(F.text,Form.deleting_spares)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("удаление запчастей")
    data = await state.get_data()
    if '| 'in message.text and  message.text.split('| ')[1] in  data['spares']:
        data['spares'].remove(message.text.split('| ')[1])
        await message.answer(await info(state), reply_markup=works_edit_kb())
        await state.set_state(Form.next_menu)
    else:
        await message.answer('Нет такой запчасти')
        await state.set_state(Form.remont_edit)
        await message.answer(await info(state), reply_markup=works_edit_kb())

@spares_router.message(F.text.contains("Запчасти не использовались"))
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("ЗАпвчасти не использовались")
    await state.set_state(Form.next_menu)
    await message.answer(await(info(state)), reply_markup=works_edit_kb())
@spares_router.message(F.text,Form.getting_spare_)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("Получение запчастей_")
    data = await state.get_data()
    if message.text == "❌ Отмена":
        await message.reply(await info(state), reply_markup=works_edit_kb())
        await state.set_state(Form.next_menu)
        return
    elif 'б/у' in message.text:
        data['spares_types'].append('б/у')
    else:
        data['spares_types'].append('Новый')
    await message.reply("Выбери группу запчастей:", reply_markup=return_spares_group(df_spares, await state.get_data()))
    await state.set_state(Form.find_spare_)
@spares_router.message(F.text,Form.find_spare_)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("поиск зч_")
    data = await state.get_data()
    if message.text == 'Назад':
        await state.set_state(Form.client_start)
        await message.answer('хих', reply_markup=works_edit_kb())
        return
    if message.text in df_spares[df_spares['type'] == data['m_or_e']].group.unique():
        await state.update_data(last_spare_group=message.text)
        await state.set_state(Form.add_spare_)
        await message.reply("Выбери запчасть:", reply_markup=return_spares(df_spares, await state.get_data()))
    else:
        await message.reply("Выбери группу запчастей:",
                            reply_markup=return_spares_group(df_spares, await state.get_data()))
        await state.set_state(Form.find_spare)
@spares_router.message(F.text,Form.add_spare_)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("добавление запчасти_")
    data = await state.get_data()
    v_spares = df_spares.loc[((df_spares['group'] == data['last_spare_group']) & (df_spares['type'] == data['m_or_e']))]['spares'].unique()
    if message.text in v_spares:
        data['spares'].append(message.text)
        await state.update_data(data=data)
        await message.answer(await(info(state)),reply_markup=works_edit_kb())
        await state.set_state(Form.next_menu)
    else:
        await message.answer("Введи зч", reply_markup=spares_list_for_work())
@spares_router.message(F.text,Form.find_spare)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("Поиск запчасти")
    data = await state.get_data()
    if message.text=='❌ Отмена':
        await state.set_state(Form.client_start)
        await message.answer('хих',reply_markup=works_edit_kb())
        return
    if message.text in df_spares[df_spares['type']==data['m_or_e']].group.unique():
        await state.update_data(last_spare_group=message.text)
        await state.set_state(Form.add_spare_)
        await message.reply("Выбери запчасть:",reply_markup=return_spares(df_spares,await state.get_data()))
    else:
        await message.reply("Выбери группу запчастей:",
                            reply_markup=return_spares_group(df_spares, await state.get_data()))
        await state.set_state(Form.find_spare)
#=======================================================================================================================
@spares_router.message(F.text,Form.getting_spare)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("получение запчасти")
    data = await state.get_data()
    v_spares = df[df['works']==data['works'][-1]]['spares'].unique()
    if 'б/у' in message.text:
        data['spares_types'].append('б/у')
    elif '❌ Отмена' == message.text:
        await message.reply(await info(state), reply_markup=works_edit_kb())
        await state.set_state(Form.next_menu)
        print('ddddddddddddddddddddddddddddddddddddd')
        return
    else:
        data['spares_types'].append('Новый')
    await message.reply("Запчасти:", reply_markup=add_spares(v_spares))
    await state.set_state(Form.add_spare)
    await state.update_data(spares_variant=v_spares)
@spares_router.message(F.text,Form.add_spare)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("добавление запччасти")
    data = await state.get_data()
    if message.text in list(data['spares_variant']):
        data['spares'].append(message.text)
        await state.update_data(data=data)
        await message.answer(await info(state), reply_markup=works_edit_kb())
        await state.set_state(Form.next_menu)
    else:
        await message.answer("Введи зч", reply_markup=spares_list_for_work())
        await state.set_state(Form.find_spare)