from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from keyboards.all_kb import main_kb, b_models, works_edit_kb, works_groups, return_works_kb, m_or_e_kb,\
    add_spares,spares_list_for_work,return_spares_group,return_spares,deleting_spares,akb_menu,akb_works
from aiogram.fsm.context import FSMContext
import pandas as pd
from utils.info import info
from utils.dataframes import df,df_spares



class Form(StatesGroup):
    client_start = State()
    akb_menu = State()
    set_akb_work = State()
    akb_start = State()


akb_router = Router()
async def akb_work_init(state):
    await state.update_data(akb_works = {})
    await state.update_data(akb_work2424s={})
async  def akb_info(state):
    data = await state.get_data()
    s = f"Всего АКБ: {sum(data['akb_works'].values())}\n"
    s+= 'Работы\n'
    for i in data['akb_works'].keys():
        if data['akb_works'][i]!=0:
            s+=f"{i}: {data['akb_works'][i]}\n"
            s+=f"{'-'*20}\n"
    return s

@akb_router.message(F.text=="Начать работу",Form.akb_start)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await akb_work_init(state)
    await message.answer("Что будем делать?:", reply_markup=akb_menu())
    await state.set_state(Form.akb_menu)


@akb_router.message(F.text=="Добавить работу",Form.akb_menu)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await message.answer("Выбери работу:", reply_markup=akb_works(df))
    await state.set_state(Form.set_akb_work)

@akb_router.message(F.text,Form.set_akb_work)
async def start_questionnaire_process(message: Message, state: FSMContext):
    if message.text in df[df['type']=="АКБ"].works.unique():
        data = await state.get_data()
        if message.text not in data['akb_works']:
            data['akb_works'][message.text] = 1
        else:
            data['akb_works'][message.text]+=1
        await state.update_data(data)
        await state.set_state(Form.akb_menu)
        await message.answer(await akb_info(state), reply_markup=akb_menu())
    else:
        await message.answer('Такой работы нет. Выбери из списка:',reply_markup=akb_works(df))
        await state.set_state(Form.set_akb_work)