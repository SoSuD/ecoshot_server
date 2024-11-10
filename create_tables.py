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
        rows = await conn.fetch(f"SELECT * FROM {table}")
        for row in rows:
            print(dict(row))
    await pool.close()  # Закрываем пул после использования


async def create_table_users():

    query = '''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        user_id INT NOT NULL,
        hwid_connected VARCHAR(128),
        sub_until INT,
        keys_activated_count INT
    );
    '''
    query = '''
    CREATE TABLE IF NOT EXISTS keys (
        id SERIAL PRIMARY KEY,
        key VARCHAR(128),
        activated_user_id INT,
        activated_hwid VARCHAR(128),
        sub_for_seconds INT,
        activations INT,
        activations_max INT,
        promo_type INT
        
    );
    '''

    activations_query = '''
    CREATE TABLE IF NOT EXISTS activations (
        id SERIAL PRIMARY KEY,
        activated_user_id INT,
        activated_hwid VARCHAR(128),
        key VARCHAR(128)
    );
    '''

    edit_table = '''
    ALTER TABLE users ALTER COLUMN sub_until TYPE bigint USING sub_until::bigint;
    '''
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(edit_table)
        #await conn.execute(activations_query)

    await pool.close()

asyncio.run(create_table_users())