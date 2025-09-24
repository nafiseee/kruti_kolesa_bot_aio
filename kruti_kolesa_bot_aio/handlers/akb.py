from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from keyboards.all_kb import main_kb, b_models, works_edit_kb, works_groups, return_works_kb, m_or_e_kb,\
    add_spares,spares_list_for_work,return_spares_group,return_spares,deleting_spares,akb_menu,akb_works,return_akb_works_kb
from aiogram.fsm.context import FSMContext
import pandas as pd
from utils.info import info
from utils.dataframes import df,df_spares
from create_bot import Form
from validators.validators import act_validate,akb_id_validate
from aiogram.types import FSInputFile,ReplyKeyboardRemove,CallbackQuery
from datetime import timedelta
async def init_akb_work(state,message):
    print('инициализя')
    await state.update_data(works=[], user_id=message.from_user.id)
    await state.update_data(works_count={}, user_id=message.from_user.id)
    await state.update_data(sum_norm_time=0, user_id=message.from_user.id)
    await state.update_data(a=[], user_id=message.from_user.id)
    await state.update_data(norm_time=[], user_id=message.from_user.id)
    await state.update_data(spares=[], user_id=message.from_user.id)
    await state.update_data(spares_types=[], user_id=message.from_user.id)
    await message.answer(await info(state), reply_markup=works_edit_kb())
    await state.set_state(Form.akb_menu)

akb_router = Router()

@akb_router.message(F.text,Form.act_akb_id)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("номер акта")
    if not act_validate(message.text):
        await message.reply("Некоректный номер акта. Попробуйте еще раз")
        return
    await state.update_data(act_akb_id=message.text, user_id=message.from_user.id)
    await message.answer('Номер акб:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.akb_id)

@akb_router.message(F.text,Form.akb_id)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print('номер велика')
    if not akb_id_validate(message.text):
        await message.reply("Некоректный номер акб. Попробуйте еще раз")
        return
    await state.update_data(akb_id=message.text, user_id=message.from_user.id)
    await state.update_data(start_time=(message.date + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"))
    await state.update_data(employer=message.from_user.full_name)
    await init_akb_work(state,message)

@akb_router.message(F.text=='➕ Добавить запчасть',Form.akb_menu)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("Добавить зч")
    await state.set_state(Form.getting_akb_spare)
    await message.answer("Введи зч", reply_markup=spares_list_for_work())

@akb_router.message(F.text == "➕ Добавить работу",Form.akb_menu)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("Добавление работы")
    await state.set_state(Form.find_akb_work)
    await message.reply("Выбери вид работы:", reply_markup=return_akb_works_kb(await state.get_data(), df))
    await state.set_state(Form.add_akb_work)

@akb_router.message(F.text,Form.add_akb_work)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("добавление работы")
    data = await state.get_data()
    if message.text in df.loc[(df['type']=="АКБ")]['works'].unique():
        data['works'].append(message.text)
        data['norm_time'].append(df.loc[(df['works']==message.text)]['time'].iloc[0])
        await state.update_data(data=data)
        await state.set_state(Form.getting_akb_spare)
        await message.answer("Введи тип зч", reply_markup=spares_list_for_work())
    else:
        await message.answer(await(info(state)), reply_markup=works_edit_kb())
        await state.set_state(Form.akb_menu)


@akb_router.message(F.text,Form.getting_akb_spare)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("получение запчасти")
    data = await state.get_data()
    v_spares = df[df['type']=='АКБ'].spares.unique()
    if 'б/у' in message.text:
        data['spares_types'].append('б/у')
    elif message.text == "Добавить запчасть":
        data['spares_types'].append('Новый')
    else:
        await state.set_state(Form.akb_menu)
        await message.answer(await(info(state)), reply_markup=works_edit_kb())
        return
    await message.reply("Запчасти:", reply_markup=add_spares(v_spares))
    await state.set_state(Form.add_akb_spare_)
    await state.update_data(spares_variant=v_spares)




@akb_router.message(F.text,Form.add_akb_spare_)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("добавление запчасти_")
    data = await state.get_data()
    if message.text in df.loc[(df['type']=="АКБ")]['spares'].unique():
        data['spares'].append(message.text)
        await state.update_data(data=data)
        await message.answer(await(info(state)),reply_markup=works_edit_kb())
        await state.set_state(Form.akb_menu)
    else:
        await message.answer("Введи зч", reply_markup=spares_list_for_work())



@akb_router.message(F.text=="🗑 Удалить запчасть",Form.remont_edit)
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

@akb_router.message(F.text,Form.deleting_spares)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("удаление запчастей")
    data = await state.get_data()
    if '| 'in message.text and  message.text.split('| ')[1] in  data['spares']:
        print(int(message.text.split('| ')[0]))
        data['spares'].pop(int(message.text.split('| ')[0])-1)
        data['spares_types'].pop(int(message.text.split('| ')[0])-1)
        await message.answer(await info(state), reply_markup=works_edit_kb())
        await state.set_state(Form.akb_menu)
    else:
        await message.answer('Нет такой запчасти')
        await state.set_state(Form.remont_edit)
        await message.answer(await info(state), reply_markup=works_edit_kb())

@akb_router.message(F.text.contains("Запчасти не использовались"))
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("ЗАпвчасти не использовались")
    await state.set_state(Form.akb_menu)
    await message.answer(await(info(state)), reply_markup=works_edit_kb())
@akb_router.message(F.text,Form.getting_akb_spare_)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("Получение запчастей_")
    data = await state.get_data()
    v_spares = df[df['type'] == 'АКБ'].spares.unique()
    if message.text == "❌ Отмена":
        await message.reply(await info(state), reply_markup=works_edit_kb())
        await state.set_state(Form.akb_menu)
        return
    elif 'б/у' in message.text:
        data['spares_types'].append('б/у')
    else:
        data['spares_types'].append('Новый')
    await message.reply("Запчасти:", reply_markup=add_spares(v_spares))
    await state.set_state(Form.add_akb_spare_)
    await state.update_data(spares_variant=v_spares)


@akb_router.message(F.text,Form.find_spare)
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

# @akb_router.message(F.text,Form.add_akb_spare)
# async def start1_questionnaire_process(message: Message, state: FSMContext):
#     print("добавление запччасти")
#     data = await state.get_data()
#     if message.text in list(data['spares_variant']):
#         data['spares'].append(message.text)
#         await state.update_data(data=data)
#         await message.answer(await info(state), reply_markup=works_edit_kb())
#         await state.set_state(Form.akb_menu)
#     else:
#         await message.answer("Введи зч", reply_markup=spares_list_for_work())
#         await state.set_state(Form.find_spare)