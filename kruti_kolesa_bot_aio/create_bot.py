import logging
from aiogram import Bot, Dispatcher,types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
#from aiogram.fsm.storage.redis import RedisStorage
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from aiogram.fsm.state import State, StatesGroup
class Form(StatesGroup):
    get_name_employer = State()
    client_start = State()
    full_name = State()
    phone_number = State()
    act_id = State()
    b_or_e = State()
    b_model = State()
    b_id = State()
    iot_id = State()
    find_works = State()
    find_work = State()
    add_work = State()
    find_spare = State()
    find_spare_ = State()
    add_spare = State()
    add_spare_ = State()
    find_spares = State()
    wait = State()
    getting_spare = State()
    getting_spare_ = State()
    remont_edit = State()
    deleting_spares = State()
    next_menu = State()
    akb_menu = State()
    akb_start = State()
    deleting_work = State()
    getting_akb_spare = State()
    getting_akb_spare_ = State()
    set_akb_work = State()
    find_akb_work = State()
    add_akb_work = State()
    act_akb_id = State()
    akb_id = State()
    add_akb_spare = ()
    find_akb_spare = State()
    add_akb_spare_ = State()
    admin = State()
    saved_remont_edit = State()
    akb_remont_edit = State()
    akb_deleting_spares = State()
    get_capacity = State()
    getting_spare_for_work = State()



# from db_handler.db_class import PostgresHandler
# pg_db = PostgresHandler(config('PG_LINK'))
scheduler = AsyncIOScheduler()
admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]

async_client = AsyncIOMotorClient('mongodb://localhost:27017/')
async_db = async_client.telegram_bot
electro = async_db.electro
mechanical = async_db.mechanical
akb = async_db.akb
users = async_db.users
messages = async_db.messages



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())