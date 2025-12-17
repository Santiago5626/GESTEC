import asyncio
from database import AsyncSessionLocal
from models.user import User
from sqlalchemy.future import select

async def update_admin_id():
    async with AsyncSessionLocal() as session:
        print("Updating Juan Carlos Carvajal ID...")
        result = await session.execute(select(User).where(User.email == "admin@gesttec.com"))
        user = result.scalars().first()
        
        if user:
            user.technician_id = "60633"
            await session.commit()
            print("✅ Admin ID updated to 60633")
        else:
            print("❌ Admin User not found")

if __name__ == "__main__":
    asyncio.run(update_admin_id())
