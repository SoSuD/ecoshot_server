import random
import uuid

import asyncpg
import asyncio

from database import get_pool


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
        #return True
    finally:
        await pool.close()


async def main():
    key = str(uuid.uuid4())
    sub_days = 1 * 24 * 60 * 60
    activations = 0
    activations_max = 2
    promo_type = 7327
    await add_key(key, sub_days, activations, activations_max, promo_type)

# Only call asyncio.run() in the main entry point of the program
if __name__ == "__main__":
    asyncio.run(main())
