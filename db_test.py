import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

load_dotenv()
url = os.getenv('DATABASE_URL')
print(f'Testing: {url}')

async def test():
    engine = create_async_engine(url)
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text('SELECT 1 as ok'))
            print(f'Connected! Result: {result.scalar()}')
    except Exception as e:
        print(f'Failed: {e}')
    finally:
        await engine.dispose()

asyncio.run(test())