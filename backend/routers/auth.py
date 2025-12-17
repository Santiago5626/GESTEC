from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models.user import User
from services.helpdesk_service import find_technician_id_by_name

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)

class LoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    name: str
    email: str
    role: str
    technician_id: str | None = None

class LoginResponse(BaseModel):
    token: str
    user: UserResponse

@router.post("/login", response_model=LoginResponse)
async def login(credentials: LoginRequest, db: AsyncSession = Depends(get_db)):
    
    # Query Database
    result = await db.execute(select(User).where(User.email == credentials.email))
    user = result.scalars().first()

    if not user or user.hashed_password != credentials.password:
         raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    # Check if technician_id is missing and try to fetch it dynamically if it's a tech
    # This is a fallback/sync mechanism to keep DB updated with external API ID
    if user.role == 'technical' and not user.technician_id:
         print(f"Technician ID missing for {user.name}, fetching from API...")
         # Run sync api call in thread to avoid blocking main loop
         import asyncio
         loop = asyncio.get_running_loop()
         try:
            tech_id_api = await loop.run_in_executor(None, find_technician_id_by_name, user.name)
            if tech_id_api:
                user.technician_id = tech_id_api
                await db.commit() # Save for future login
         except Exception as e:
            print(f"Error fetching tech id on login: {e}")

    return {
        "token": f"token-{user.role}-{user.id}",
        "user": {
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "technician_id": user.technician_id
        }
    }
