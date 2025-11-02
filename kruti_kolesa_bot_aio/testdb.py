import asyncio
from motor.motor_asyncio import AsyncIOMotorClient


async def test_both_connections():
    # Тест локального подключения
    local_client = AsyncIOMotorClient('mongodb://185.119.59.184:27017/botdb?authSource=admin')

    # Тест подключения с аутентификацией
    auth_client = AsyncIOMotorClient('mongodb://botuser:securepassword123@your_server_ip:27017/botdb?authSource=admin')

    try:
        await local_client.admin.command('ping')
        print("✅ Локальное подключение работает")
    except Exception as e:
        print(f"❌ Локальное подключение: {e}")

    try:
        await auth_client.admin.command('ping')
        print("✅ Подключение с аутентификацией работает")
    except Exception as e:
        print(f"❌ Подключение с аутентификацией: {e}")


asyncio.run(test_both_connections())