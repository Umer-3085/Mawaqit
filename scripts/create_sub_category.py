import asyncio
from mawaqit.database import get_db_context
from mawaqit.models.category import Category
from mawaqit.models.subcategory import SubCategory
from sqlalchemy import select

async def seed():
    async with get_db_context() as db:
        # Fetch categories (must exist first)
        result = await db.execute(select(Category))
        categories = list(result.scalars().all())
        if not categories:
            print("No categories found. Run seed_category.py first.")
            return
        
        cat_map = {c.title: c.id for c in categories}
        
        subcategories = [
            SubCategory(title="Tafseer", category_id=cat_map["Quran"], description="Quran exegesis"),
            SubCategory(title="Translation", category_id=cat_map["Quran"], description="Quran translations"),
            SubCategory(title="Sahih Bukhari", category_id=cat_map["Hadith"], description="Bukhari collection"),
            SubCategory(title="Fiqh Basics", category_id=cat_map["Fiqh"], description="Basic fiqh"),
        ]
        db.add_all(subcategories)
        await db.commit()
        for s in subcategories:
            await db.refresh(s)
            print(f"Created: {s.title} (id={s.id}, cat={s.category_id})")

if __name__ == "__main__":
    asyncio.run(seed())