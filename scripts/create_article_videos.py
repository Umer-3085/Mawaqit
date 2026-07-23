import asyncio
from mawaqit.database import get_db_context
from mawaqit.models.category import Category
from mawaqit.models.subcategory import SubCategory
from mawaqit.models.article_videos import ArticleVideo
from sqlalchemy import select

async def seed():
    async with get_db_context() as db:
        # Fetch existing categories & subcategories
        cats_result = await db.execute(select(Category))
        categories = {c.title: c.id for c in cats_result.scalars().all()}
        
        subs_result = await db.execute(select(SubCategory))
        subcategories = {s.title: s.id for s in subs_result.scalars().all()}
        
        if not categories:
            print("No categories found. Run seed_category.py first.")
            return
        
        items = [
            # Articles (link=None)
            ArticleVideo(title="Surah Al-Fatiha Tafseer", detail="Detailed tafseer...", category_id=categories["Quran"], subcategory_id=subcategories.get("Tafseer"), link=None),
            ArticleVideo(title="Quran Translation Comparison", detail="Comparing translations...", category_id=categories["Quran"], subcategory_id=subcategories.get("Translation"), link=None),
            ArticleVideo(title="Hadith on Prayer", detail="Sahih Bukhari hadith...", category_id=categories["Hadith"], subcategory_id=subcategories.get("Sahih Bukhari"), link=None),
            ArticleVideo(title="Wudu Tutorial Article", detail="Step by step...", category_id=categories["Fiqh"], subcategory_id=subcategories.get("Fiqh Basics"), link=None),
            ArticleVideo(title="Prayer Times Calculation Article", detail="How to calculate...", category_id=categories["Fiqh"], subcategory_id=None, link=None),
            
            # Videos (link provided)
            ArticleVideo(title="Surah Al-Fatiha Video", detail="Video tafseer...", category_id=categories["Quran"], subcategory_id=subcategories.get("Tafseer"), link="https://youtube.com/watch?v=abc123"),
            ArticleVideo(title="Wudu Tutorial Video", detail="Video guide...", category_id=categories["Fiqh"], subcategory_id=subcategories.get("Fiqh Basics"), link="https://youtube.com/watch?v=def456"),
        ]
        
        db.add_all(items)
        await db.commit()
        for item in items:
            await db.refresh(item)
            ctype = "Video" if item.link else "Article"
            print(f"Created: {item.title} [{ctype}] (id={item.id}, cat={item.category_id}, subcat={item.subcategory_id})")

if __name__ == "__main__":
    asyncio.run(seed())