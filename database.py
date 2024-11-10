import random
import time
import uuid

import asyncpg
import asyncio

async def get_pool():
    # Создаем пул соединений
    pool = await asyncpg.create_pool(
        user='EcoShot',
        password='123123As',
        database='ecoshot_db',
        host='localhost',
        min_size=1,
        max_size=10
    )
    return pool

async def fetch_data(table):
    pool = await get_pool()
    async with pool.acquire() as conn:  # Берем соединение из пула
        rows = await conn.fetchrow(f"SELECT * FROM {table}")
        for row in rows:
            print(dict(row))
    await pool.close()  # Закрываем пул после использования

async def db_check_hwid(hwid):

    query = f'''SELECT * FROM users WHERE hwid_connected = $1'''
    pool = await get_pool()
    async with pool.acquire() as conn:
        result = await conn.fetchrow(query, hwid)
        print(result)
        return result if result else False

async def get_key_info(key):
    pass

async def db_add_user(hwid):
    user_id = random.randint(10000000000000, 99999999999999)
    query = f'''
    INSERT INTO users (user_id, hwid_connected, sub_until, keys_activated_count)
    VALUES ($1, $2, 0, 0)'''
    pool = await get_pool()
    if not await db_check_hwid(hwid):
        async with pool.acquire() as conn:
            await conn.execute(query, user_id, hwid)

            print("db_add_user_True")
            return True
    else:
        print("db_add_user_False", "уже существует хвид")
        return False
    #sub_until = get_key_info(key)["sub_days"]

async def add_key(key, sub_for_seconds, activations, activations_max, promo_type):
    query = f'''
INSERT INTO keys (key, sub_for_seconds, activations, activations_max, promo_type)
VALUES ($1, $2, $3, $4, $5)'''

    pool = await get_pool()
    # if not await db_check_hwid(hwid):
    try:
        async with pool.acquire() as conn:
            await conn.execute(query, key, sub_for_seconds, activations, activations_max, promo_type)

            print("key_added: ", key, sub_for_seconds, activations, activations_max, promo_type)

    finally:
        await pool.close()
    return key


async def db_get_key(key):
    query_key = f'''
    SELECT * FROM keys WHERE key = $1'''
    pool = await get_pool()
    try:
        async with pool.acquire() as conn:
            key_data = await conn.fetchrow(query_key, key)
            #print(key_data)
            #input()
    finally:
        await pool.close()
    return key_data if key_data else False


async def db_activate_key(key_data, hwid):
    if key_data["activations"] >= key_data["activations_max"]:
        return False

    pool = await get_pool()
    try:
        async with pool.acquire() as conn:
            async with conn.transaction():
                # Заблокировать строку ключа для предотвращения параллельного доступа
                query_lock = '''
                SELECT activations, activations_max FROM keys WHERE id = $1 FOR UPDATE;
                '''
                row = await conn.fetchrow(query_lock, key_data["id"])

                # Проверяем, можно ли еще активировать ключ
                if row["activations"] >= row["activations_max"]:
                    return False

                # Обновляем активность ключа и пользователя в одной транзакции
                query1 = '''
                UPDATE keys SET activations = activations + 1, activated_user_id = (
                    SELECT user_id FROM users WHERE hwid_connected = $2
                ), activated_hwid = $2 WHERE id = $1;
                '''
                query2 = '''
                UPDATE users SET sub_until = ($2::BIGINT + $3::BIGINT) WHERE hwid_connected = $1;
                '''

                # Выполняем оба обновления
                await conn.execute(query1, key_data["id"], hwid)
                await conn.execute(query2, hwid, int(time.time()), key_data["sub_for_seconds"])

    finally:
        await pool.close()

    #return key_data
    return await db_check_hwid(hwid)


async def main():
    key_data = await db_get_key("ae2d20a3-7443-4982-ae49-23c7524430a6")
    print(await db_activate_key(key_data, "testhwid"))


if __name__ == '__main__':
    asyncio.run(main())
