from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from create_bot import admins
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from electro_works import electro_works
from mechanical_works import mechanical_works



def main_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="🔧 Клиентский ремонт"), KeyboardButton(text="🛠️ Техническое обслуживание")],
        [KeyboardButton(text="🔋 Аккумулятор"), KeyboardButton(text="☠️☠️☠️☠️")]
    ]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text="⚙️ Админ панель")])
    if user_telegram_id in [168604695,1003927607,933028899]:
        kb_list.append([KeyboardButton(text="🎵 Музыка")])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

def m_or_e_kb():
    kb_list = [
        [KeyboardButton(text="🔩 Механика")],
        [KeyboardButton(text="⚡ Электро")],
        [KeyboardButton(text="↩ Отмена")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard
def works_edit_kb():
    kb_list = [
        [KeyboardButton(text="➕ Добавить работу"),KeyboardButton(text="➕ Добавить запчасть")],
        [KeyboardButton(text="✏️Изменить ремонт")],
        [KeyboardButton(text="Сохранить ремонт 💾")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard
def akb_menu():
    kb_list = [
        [KeyboardButton(text="Добавить работу"),KeyboardButton(text="Добавить запчасть")],
        [KeyboardButton(text="Сохранить ремонт 💾")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard
def akb_works(df):
    kb = [[KeyboardButton(text=i)] for i in df[df['type']=="АКБ"].works.unique()]
    kb.append([KeyboardButton(text='❌ Отмена')])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard
def akb_start_kb():
    kb_list = [
        [KeyboardButton(text="Начать работу")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard
def b_models(a):
    kb_list = [
        [InlineKeyboardButton(text="Шаркусь монстр 15", callback_data='Шаркусь монстр 15')],
        [InlineKeyboardButton(text="Шаркусь монстр 20", callback_data='Шаркусь монстр 20')],
        [InlineKeyboardButton(text="Мингто монстр 20", callback_data='Мингто монстр 20')],
        [InlineKeyboardButton(text="Монстр про", callback_data='Монстр про')],
        [InlineKeyboardButton(text="Крути 15", callback_data='Крути 15')]]
    kb_list2 = [[InlineKeyboardButton(text="Forward 27.5", callback_data='Forward 27.5')],
                [InlineKeyboardButton(text="Forward 29", callback_data='Forward 29')],
                [InlineKeyboardButton(text="Kruti 27.5", callback_data='Kruti 27.5')],
                [InlineKeyboardButton(text="Kruti 29", callback_data='Kruti 29')]
                ]
    if a=='Механика':
        return InlineKeyboardMarkup(inline_keyboard=kb_list2)
    else:
        return InlineKeyboardMarkup(inline_keyboard=kb_list)
#dict_keys(['accumulator', 'electronics', 'braking_system', 'drive_train', 'frame_and_wheels', 'body_and_cosmetic', 'lighting', 'other'])
def works_groups(data,df):
    kb = [[KeyboardButton(text=i)] for i in df[df['type']==data['m_or_e']]['group'].unique()]
    kb.append([KeyboardButton(text='❌ Отмена')])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

def add_spares(a):
    kb_list = [[KeyboardButton(text=i)] for i in a]
    kb_list.append([KeyboardButton(text="❌ Отмена ")])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard
def spares_list_for_work():
    kb_list = [
        [KeyboardButton(text="Добавить запчасть")],
        [KeyboardButton(text="Добавить б/у запчасть")],
        [KeyboardButton(text="Запчасти не использовались")]
    ]
    kb_list.append([KeyboardButton(text="❌ Отмена")])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard


def return_works_kb(data,df):
    kb = [[KeyboardButton(text=i)] for i in df.loc[((df['group']==data['last_group'])&(df['type']==data['m_or_e']))]['works'].unique()]
    kb.append([KeyboardButton(text="❌ Отмена")])
    keyboard = ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder="Воспользуйтесь меню:"
        )
    for i in kb:
        print(i)
    return keyboard
def return_spares_group(df,data):
    kb = [[KeyboardButton(text=i)] for i in df[df['type']==data['m_or_e']].group.unique()]
    kb.append([KeyboardButton(text="❌ Отмена")])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard
def return_spares(df,data):
    kb = [[KeyboardButton(text=i)] for i in df.loc[((df['group']==data['last_spare_group'])&(df['type']==data['m_or_e']))]['spares'].unique()]
    kb.append([KeyboardButton(text="❌ Отмена")])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

def edit_work():
    kb_list = [
        [KeyboardButton(text="🗑 Удалить работу")],
        [KeyboardButton(text="🗑 Удалить запчасть")],
        [KeyboardButton(text="❌ Отмена")],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard
def deleting_works(data):
    print(data)
    kb = []
    for q in range(len(data['works'])):
        kb.append([KeyboardButton(text=f"{str(q)}| {data['works'][q]}")])
    kb.append([KeyboardButton(text="❌ Отмена")])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    print(data['works'])
    return keyboard
def deleting_spares(data):
    print(data)
    kb = []
    for q in range(len(data['spares'])):
        kb.append([KeyboardButton(text=f"{str(q)}| {data['spares'][q]}")])
    kb.append([KeyboardButton(text="❌ Отмена")])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    print(data['works'])
    return keyboard
def to_delete_work(data,df):
    kb = [[KeyboardButton(text=i)] for i in data['works']]
    kb.append([KeyboardButton(text='Отмена')])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    for i in kb:
        print(i)
    return keyboard