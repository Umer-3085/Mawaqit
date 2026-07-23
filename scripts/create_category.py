import asyncio
from mawaqit.database import get_db_context
from mawaqit.models.category import Category

async def seed():
    async with get_db_context() as db:
        categories = [
            Category(title="Quran", description="Quran related content"),
            Category(title="Hadith", description="Hadith collections"),
            Category(title="Fiqh", description="Islamic jurisprudence"),
        ]
        db.add_all(categories)
        await db.commit()
        for c in categories:
            await db.refresh(c)
            print(f"Created: {c.title} (id={c.id})")

if __name__ == "__main__":
    asyncio.run(seed())