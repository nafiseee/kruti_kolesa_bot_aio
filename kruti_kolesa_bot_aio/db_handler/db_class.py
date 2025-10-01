import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from create_bot import electro,mechanical,akb,users
from pprint import pprint
from pymongo import MongoClient, DESCENDING
import pandas as pd
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

async def check_sub(i):

    a = [dict(i) for i in await users.find().to_list()]
    print(a)
    for q in a:
        if q['tg_id']==i:
            return True
    return False
async def add_user(tg_id,name):
    await users.insert_one({"tg_id": tg_id, "name": name})
async def get_user_name(tg_id):
    return dict(await users.find_one({"tg_id": tg_id}))['name']

async def save_remont(state):
    data = await state.get_data()
    data['sum_norm_time'] = sum(data['norm_time'])
    to_delete = ['works_count','spares_variant','a','last_group','norm_time']
    d = {}
    for i in data.keys():
        if i not in to_delete:
            d[i]=data[i]
    if 'm_or_e' in data:
        if data['m_or_e']=="Электро":
            await electro.insert_one(d)

        if data['m_or_e'] == "Механика":
            await mechanical.insert_one(d)

    if 'akb' in data:
        await akb.insert_one(d)
async def get_remonts():
    q = electro.find()
    cursor = q.sort('_id', -1).limit(10)
    records = await cursor.to_list(length=10)
    records.reverse()  # Правильный порядок
    return records

async def get_my_time(id):
    e_sum = sum([i['sum_norm_time'] for i in await electro.find({"emploer_id": id}).to_list()])
    m_sum = sum([i['sum_norm_time'] for i in await mechanical.find({"emploer_id": id}).to_list()])
    akb_sum = sum([i['sum_norm_time'] for i in await akb.find({"emploer_id": id}).to_list()])
    return e_sum+m_sum+akb_sum

async def get_times_all():
    all_employers = [dict(i) for i in await users.find().to_list()]
    print(all_employers)
    a = {}
    for empl in all_employers:
        a[await get_user_name(empl['tg_id'])] = await get_my_time(empl['tg_id'])
    print(a)
    return a

async def get_lost_spares():
    all_spares = []
    a = [dict(i)['spares'] for i in await electro.find().to_list()]
    b = [dict(i)['spares'] for i in await mechanical.find().to_list()]
    c = [dict(i)['spares'] for i in await akb.find().to_list()]
    for i in a:
        for ii in i:
            all_spares.append(ii)
    for i in b:
        for ii in i:
            all_spares.append(ii)
    for i in c:
        for ii in i:
            all_spares.append(ii)
    all_spares_df = pd.DataFrame(all_spares,columns=['Запчасти'])
    all_spares_df.to_excel('temporary_folder/lost_spares1.xlsx',index=False)

    a = {}
    for i in all_spares:
        if i in a:
            a[i] += 1
        else:
            a[i] = 1
    print(a)
    all_spares = pd.DataFrame({'Запчасти': a.keys(),'Количество': a.values()})
    all_spares.to_excel('temporary_folder/lost_spares2.xlsx', index=False)
    print(all_spares)
    print()
    return True