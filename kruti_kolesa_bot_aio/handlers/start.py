from aiogram import Router, F
import asyncio
from create_bot import bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile,ReplyKeyboardRemove,CallbackQuery
from keyboards.all_kb import main_kb,b_models,works_edit_kb,works_groups,return_works_kb,m_or_e_kb,edit_work,akb_menu,akb_start_kb
from aiogram.utils.chat_action import ChatActionSender
from validators.validators import name_validate,phone_validate,act_validate,model_validate,id_validate,iot_validate,\
    bycycle_type_validate,work_is_true
from datetime import timedelta
import pandas as pd
from utils.info import info
from db_handler import db_class
from create_bot import Form
from utils.message_utils import delete_message
from create_bot import users_collection
start_photo = FSInputFile('media/sticker.webm', filename='хуй')
client_work_keys = ['work_type','full_name','phone_number','act_id','b_model','b_id','iot_id']
client_work = ['','','Номер телефона: ','Акт №','Модель велосипеда: ','Номер велосипеда: ', 'IoT: ']


start  = Router()
questionnaire_router = Router()
works_router = Router()

df = pd.read_excel('works_norm.xlsx',names = ['work','time','type','sale','group'])
async def init_work(state,message):
    print('инициализя')
    await state.update_data(works=[], user_id=message.from_user.id)
    await state.update_data(works_count={}, user_id=message.from_user.id)
    await state.update_data(sum_norm_time=0, user_id=message.from_user.id)
    await state.update_data(a=[], user_id=message.from_user.id)
    await state.update_data(norm_time=[], user_id=message.from_user.id)
    await state.update_data(spares=[], user_id=message.from_user.id)
    await state.update_data(spares_types=[], user_id=message.from_user.id)
    await message.answer(await info(state), reply_markup=works_edit_kb())
    await state.set_state(Form.next_menu)

@questionnaire_router.message(F.text == "❌ Отмена",Form.getting_spare)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print('Отмена add_spare_')
    await message.answer(await(info(state)), reply_markup=works_edit_kb())

@questionnaire_router.message(F.text == "❌ Отмена",Form.remont_edit)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print('Отмена add_spare_')
    await message.answer(await(info(state)), reply_markup=works_edit_kb())
@questionnaire_router.message(F.text == "❌ Отмена",Form.getting_spare)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("Отмена getting_spare")
    await init_work(state,message)
@questionnaire_router.message(F.text == "Отменить ремонт ❌",Form.next_menu)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.clear()
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer_photo(photo=FSInputFile('media/1.jpg', filename='Снеговик'),
                                   caption='Привет я твой помощник по занесению ремонтов. Что будем делать?',
                                   reply_markup=main_kb(message.from_user.id))
    await state.set_state(Form.client_start)



@questionnaire_router.message(F.text == "Сохранить ремонт 💾",Form.next_menu)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("Сохранить ремонт next_menu")
    # await init_work(state, message)
    await message.answer("«Иногда самые важные данные мы храним не в базе, а в моменте. Давай сохраним этот момент, а за технической частью я потом вернусь».")
    # await state.clear()
    await state.update_data(end_time=(timedelta(hours=3) + message.date).strftime("%Y-%m-%d %H:%M:%S"))
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer_photo(photo=FSInputFile('media/1.jpg', filename='Снеговик'),
                                   caption='Привет я твой помощник по занесению ремонтов. Что будем делать?',
                                   reply_markup=main_kb(message.from_user.id))
    await state.set_state(Form.client_start)
    await db_class.save_remont(state)


@start.message(Command('start')) #НАЧАЛО
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("старт епта")
    await state.clear()
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer_photo(photo=FSInputFile('media/1.jpg', filename='Снеговик'),caption = 'Привет я твой помощник по занесению ремонтов. Что будем делать?', reply_markup=main_kb(message.from_user.id))
    await state.set_state(Form.client_start)

@start.message(F.text=='⚙️ Админ панель') #НАЧАЛО
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("админка")
    await bot.send_video(message.chat.id,open('media/prikol.mp4','rb'))
@questionnaire_router.message(F.text=='🛠️ Техническое обслуживание',Form.client_start)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("ТОшка")
    await state.update_data(work_type=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await state.update_data(start_time = (timedelta(hours=3)+message.date).strftime("%Y-%m-%d %H:%M:%S"))
        await state.update_data(employer=message.from_user.full_name)
        await message.answer('Введи номер акта: ', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.act_id)
    await delete_message(message,state)

@questionnaire_router.message(F.text=='🔧 Клиентский ремонт',Form.client_start)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("Клиентский белэжт")
    await state.update_data(work_type=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await state.update_data(start_time=(message.date+timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"))
        await state.update_data(employer=message.from_user.full_name)
        await state.update_data(message_id = message.from_user.id+1)
        await message.answer('Введи ФИО:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.full_name)
@questionnaire_router.message(F.text=='🔋 Аккумулятор',Form.client_start)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("Акб")
    await state.set_state(Form.akb_start)
    await message.answer("Меню", reply_markup=akb_start_kb())

@questionnaire_router.message(F.text == '🎵 Музыка', Form.client_start)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("Музыка")
    audio_file1 = FSInputFile("media/1.mp3", "sigma1.mp3")
    audio_file2 = FSInputFile("media/2.mp3", "sigma2.mp3")
    audio_file3 = FSInputFile("media/3.mp3", "sigma3.mp3")
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer_audio(audio_file2)
@questionnaire_router.message(F.text,Form.full_name)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("Имя")
    if not name_validate(message.text):
        await message.reply("Пожалуйста, введите корректное ФИО в формате: Фамилия Имя:")
        return
    await state.update_data(full_name=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer('Введи номер телефона:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.phone_number)
@questionnaire_router.message(F.text,Form.phone_number)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("Номер телеофна")
    if not phone_validate(message.text):
        await message.reply("Пожалуйста введите номер в формате 8XXXXXXXXXX")
        return
    await state.update_data(phone_number=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer('Номер акта:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.act_id)
@questionnaire_router.message(F.text,Form.act_id)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("номер акта")
    if not act_validate(message.text):
        await message.reply("Некоректный номер акта. Попробуйте еще раз")
        return
    await state.update_data(act_id=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer('Выберите тип велоиспеда:', reply_markup=m_or_e_kb())
    await state.set_state(Form.b_or_e)
    await delete_message(message, state)
@questionnaire_router.message(F.text,Form.b_or_e)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print('Вид велика')
    if not bycycle_type_validate(message.text):
        await message.reply("Некоректный тип велосипеда. Попробуйте заново",reply_markup=m_or_e_kb())
        return
    await state.update_data(m_or_e=message.text.split(' ')[1], user_id=message.from_user.id)
    data = await state.get_data()
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer('Выберите модель велосипеда:', reply_markup=b_models(data['m_or_e']))
    await state.set_state(Form.b_model)
    await delete_message(message, state)
@questionnaire_router.message(F.text,Form.b_model)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("модель велика")
    data = await state.get_data()
    if not model_validate(message.text):
        await message.reply("Выберите модель из списка:",reply_markup=b_models(data['m_or_e']))
        return
@questionnaire_router.callback_query(F.data, Form.b_model)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    print("")
    await state.update_data(b_model=call.data)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer('Номер велосипеда:')
    await state.set_state(Form.b_id)
@questionnaire_router.message(F.text,Form.b_id)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print('номер велика')
    if not id_validate(message.text):
        await message.reply("Некоректный номер велика. Попробуйте еще раз")
        return
    await state.update_data(b_id=message.text, user_id=message.from_user.id)
    if await state.get_value('m_or_e') != 'Механика':
        await message.answer('Введите номер IoT модуля:', reply_markup=None)
        await state.set_state(Form.iot_id)
    else:
        await init_work(state,message)


@questionnaire_router.message(F.text,Form.iot_id)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("номер иот")
    if not iot_validate(message.text):
        await message.reply("Некоректный номер IoT. Попробуйте еще раз")
        return
    await state.update_data(iot_id=message.text, user_id=message.from_user.id)
    await init_work(state,message)

@questionnaire_router.message(F.text == "✏️Изменить ремонт")
async def start_questionnaire_process(message: Message, state: FSMContext):
    print('измененеие ремонта')
    await message.reply("Что делаем?:", reply_markup=edit_work())
    await state.set_state(Form.remont_edit)






