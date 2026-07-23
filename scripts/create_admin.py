import asyncio
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from mawaqit.config import settings
from mawaqit.models.admin import Admin

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

async def create_admin(username: str, password: str):
    engine = create_async_engine(settings.database_url)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        hashed = pwd_context.hash(password)
        admin = Admin(username=username, password_hash=hashed)
        session.add(admin)
        await session.commit()
        print(f"Admin '{username}' created with hashed password")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python scripts/create_admin.py <username> <password>")
        sys.exit(1)
    asyncio.run(create_admin(sys.argv[1], sys.argv[2]))