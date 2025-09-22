import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from create_bot import users_collection
from pprint import pprint
async def test_connection():
    try:
        client = AsyncIOMotorClient('mongodb://localhost:27017/')
        await client.admin.command('ping')
        print("✅ MongoDB подключена успешно")
        return True
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

asyncio.run(test_connection())


async def save_remont(state):
    data = await state.get_data()
    data['sum_norm_time'] = sum(data['norm_time'])
    to_delete = ['works_count','spares_variant','a','last_group','norm_time']
    d = {}
    for i in data.keys():
        if i not in to_delete:
            d[i]=data[i]
    await users_collection.insert_one(d)