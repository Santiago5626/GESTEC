from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from database import get_db
from models.subscription import PushSubscription
from models.user import User
from services.push_service import get_public_key
import json

router = APIRouter(
    prefix="/api/notifications",
    tags=["notifications"]
)

class SubscriptionSchema(BaseModel):
    endpoint: str
    keys: dict

@router.get("/vapid-public-key")
async def get_vapid_key():
    key = get_public_key()
    if not key:
        raise HTTPException(status_code=500, detail="VAPID keys not configured")
    return {"publicKey": key}

@router.post("/subscribe")
async def subscribe(sub_data: SubscriptionSchema, x_user_email: str, db: AsyncSession = Depends(get_db)):
    """
    Guarda la suscripción push vinculada al usuario por su email.
    (El frontend debe enviar el email en un header o body, aquí simplificamos query param o header custom por ahora)
    """
    # Find user
    result = await db.execute(select(User).where(User.email == x_user_email))
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Check if exists
    result_sub = await db.execute(select(PushSubscription).where(PushSubscription.endpoint == sub_data.endpoint))
    existing = result_sub.scalars().first()

    if existing:
        # Update user link if changed?
        existing.user_id = user.id
        existing.technician_id = user.technician_id
    else:
        new_sub = PushSubscription(
            user_id=user.id,
            endpoint=sub_data.endpoint,
            p256dh=sub_data.keys.get('p256dh'),
            auth=sub_data.keys.get('auth'),
            technician_id=user.technician_id
        )
        db.add(new_sub)
    
    await db.commit()
    return {"message": "Suscripción exitosa"}
