import asyncio
from database import AsyncSessionLocal
from models.user import User
from sqlalchemy.future import select

async def update_tech_id():
    async with AsyncSessionLocal() as session:
        print("Updating Daniel Acosta's ID...")
        result = await session.execute(select(User).where(User.email == "tecnico@gesttec.com"))
        user = result.scalars().first()
        
        if user:
            user.technician_id = "309901"
            await session.commit()
            print("✅ ID updated to 309901")
        else:
            print("❌ User not found")

if __name__ == "__main__":
    asyncio.run(update_tech_id())
