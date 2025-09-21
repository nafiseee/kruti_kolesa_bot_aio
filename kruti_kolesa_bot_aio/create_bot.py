import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
#from aiogram.fsm.storage.redis import RedisStorage
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

# from db_handler.db_class import PostgresHandler
# pg_db = PostgresHandler(config('PG_LINK'))
scheduler = AsyncIOScheduler()
admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]

async_client = AsyncIOMotorClient('mongodb://localhost:27017/')
async_db = async_client.telegram_bot
users_collection = async_db.users
messages_collection = async_db.messages

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())