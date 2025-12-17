import json
import os
import base64
from pywebpush import webpush, WebPushException
from typing import Dict, Any
from sqlalchemy.future import select
from models.subscription import PushSubscription
from database import AsyncSessionLocal

VAPID_FILE = "vapid_config.json"
VAPID_CLAIMS = {"sub": "mailto:admin@gesttec.com"}

def get_vapid_keys():
    if os.path.exists(VAPID_FILE):
        with open(VAPID_FILE, "r") as f:
            return json.load(f)
    else:
        # Generate new keys
        print("Generando nuevas claves VAPID...")
        try:
            # Intentar usar libreria cryptography si está disponible (preferido)
            from cryptography.hazmat.primitives.asymmetric import ec
            private_key = ec.generate_private_key(ec.SECP256R1())
            private_val = private_key.private_numbers().private_value
            private_b64 = base64.urlsafe_b64encode(private_val.to_bytes(32, 'big')).decode('utf-8').rstrip('=')
            
            public_val = private_key.public_key().public_numbers()
            public_bytes = b'\x04' + public_val.x.to_bytes(32, 'big') + public_val.y.to_bytes(32, 'big')
            public_b64 = base64.urlsafe_b64encode(public_bytes).decode('utf-8').rstrip('=')
            
            keys = {"privateKey": private_b64, "publicKey": public_b64}
        except ImportError:
             # Fallback inseguro o error
             print("Error: cryptography module not found. Install pywebpush[dependencies]")
             return None

        with open(VAPID_FILE, "w") as f:
            json.dump(keys, f)
        return keys

# Load keys globally
VAPID_KEYS = get_vapid_keys()

def get_public_key():
    if VAPID_KEYS:
        return VAPID_KEYS["publicKey"]
    return None

async def send_push_to_user(user_id: int, message: str, url: str = "/"):
    """
    Envía una notificación push a todas las suscripciones de un usuario.
    """
    if not VAPID_KEYS:
        print("VAPID keys not configured. Cannot send push.")
        return

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(PushSubscription).where(PushSubscription.user_id == user_id))
        subscriptions = result.scalars().all()
        
        if not subscriptions:
            print(f"No subscriptions found for user {user_id}")
            return

        payload = json.dumps({
            "title": "GestTec Alerta",
            "body": message,
            "url": url,
            "icon": "/pwa-192x192.png"
        })

        for sub in subscriptions:
            try:
                subscription_info = {
                    "endpoint": sub.endpoint,
                    "keys": {
                        "p256dh": sub.p256dh,
                        "auth": sub.auth
                    }
                }
                
                webpush(
                    subscription_info=subscription_info,
                    data=payload,
                    vapid_private_key=VAPID_KEYS["privateKey"],
                    vapid_claims=VAPID_CLAIMS
                )
                print(f"Push sent to {user_id}")
            except WebPushException as ex:
                print(f"WebPush Error: {ex}")
                # Si es 410 Gone, borrar suscripción
                if ex.response and ex.response.status_code == 410:
                    await session.delete(sub)
                    await session.commit()
            except Exception as e:
                print(f"Push Error: {e}")

# In-memory record of last check time per technician to avoid notifying old tickets
LAST_CHECK_TIME = {}

async def check_new_tickets_job():
    """
    Tarea periódica para verificar tickets nuevos y enviar notificaciones.
    """
    import services.helpdesk_service as helpdesk
    from datetime import datetime, timedelta
    
    print("Running scheduled ticket check...")
    
    async with AsyncSessionLocal() as session:
        # Get all technicians with subscriptions
        result = await session.execute(select(PushSubscription.technician_id, PushSubscription.user_id).distinct())
        techs = result.all() # [(tech_id, user_id)]
        
        for tech_id, user_id in techs:
            if not tech_id: continue
            
            try:
                # 1. Fetch recent tickets (SYNC CALL in THREAD)
                # Como get_tickets_for_technician ahora es sincrono (bloqueante),
                # debemos correrlo en un thread para no bloquear el loop de APScheduler.
                import asyncio
                loop = asyncio.get_running_loop()
                
                tickets = await loop.run_in_executor(None, helpdesk.get_tickets_for_technician, tech_id)
                
                # 2. Filter new tickets (created/assigned recently)
                # ...
                
                # Check top ticket
                if not tickets: continue
                
                latest_ticket = tickets[0]
                ticket_id = latest_ticket['id']
                subject = latest_ticket['title']
                
                # Key for tracking: TECH_ID
                last_seen_id = LAST_CHECK_TIME.get(tech_id)
                
                if last_seen_id != ticket_id:
                    # New top ticket detected!
                    
                    # Avoid notifying on first run (boot)
                    if tech_id not in LAST_CHECK_TIME:
                        LAST_CHECK_TIME[tech_id] = ticket_id
                        continue
                        
                    LAST_CHECK_TIME[tech_id] = ticket_id
                    print(f"New ticket detected for {tech_id}: {ticket_id}")
                    
                    await send_push_to_user(
                        user_id, 
                        f"Nuevo Ticket Asignado: {subject}",
                        f"/ticket/{ticket_id}"
                    )
                    
            except Exception as e:
                print(f"Error checking tickets for {tech_id}: {e}")
