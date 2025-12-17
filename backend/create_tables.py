import asyncio
from database import engine, Base, AsyncSessionLocal
from models.user import User
from models.subscription import PushSubscription
from sqlalchemy.future import select

async def init_db():
    async with engine.begin() as conn:
        # Create tables
        print("Creating tables...")
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created.")

    async with AsyncSessionLocal() as session:
        # Check if users exist
        result = await session.execute(select(User).where(User.email == "admin@gesttec.com"))
        admin = result.scalars().first()

        if not admin:
            print("Creating Admin user...")
            admin_user = User(
                name="Juan Carlos Carvajal",
                email="admin@gesttec.com",
                hashed_password="123456", # In production use hashing!
                role="admin",
                technician_id=None
            )
            session.add(admin_user)
        
        result = await session.execute(select(User).where(User.email == "tecnico@gesttec.com"))
        tech = result.scalars().first()

        if not tech:
            print("Creating Technical user...")
            tech_user = User(
                name="Daniel Acosta",
                email="daniel@gesttec.com",
                hashed_password="123456",
                role="technical",
                technician_id="309901"
            )
            session.add(tech_user)

        # Check and create Jhon
        result = await session.execute(select(User).where(User.email == "jhon@gesttec.com"))
        jhon = result.scalars().first()

        if not jhon:
            print("Creating Jhon Barragan...")
            jhon_user = User(
                name="Jhon Carlos Barragan",
                email="jhon@gesttec.com",
                hashed_password="123456",
                role="technical",
                technician_id="326715"
            )
            session.add(jhon_user)

        # Check and create Andres
        result = await session.execute(select(User).where(User.email == "andres@gesttec.com"))
        andres = result.scalars().first()

        if not andres:
            print("Creating Andres Cobo...")
            andres_user = User(
                name="Andres Juan Cobo",
                email="andres@gesttec.com",
                hashed_password="123456",
                role="technical",
                technician_id="123903"
            )
            session.add(andres_user)
        
        await session.commit()
        print("Database initialized with users.")

if __name__ == "__main__":
    asyncio.run(init_db())
