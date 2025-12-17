from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from services.helpdesk_service import find_technician_id_by_name
import requests
import json
from services.helpdesk_service import API_URL, HEADERS

router = APIRouter(prefix="/api/debug")

@router.get("/refresh-ids")
async def refresh_technician_ids(db: Session = Depends(get_db)):
    """
    Fuerza la búsqueda y actualización de IDs de técnicos para todos los usuarios.
    Útil si el seed inicial falló por bloqueo de firewall.
    """
    users = db.query(User).all()
    updated = []
    errors = []

    print("🔄 Starting manual ID refresh...")
    
    for user in users:
        try:
            print(f"Checking user: {user.name}")
            # Force search even if they have one? Maybe yes to be sure.
            # Or only if None? Let's try to update all just in case.
            tech_id = await find_technician_id_by_name(user.name)
            
            if tech_id:
                user.technician_id = tech_id
                updated.append(f"{user.name} -> {tech_id}")
            else:
                errors.append(f"{user.name}: Not found in Helpdesk API")
        except Exception as e:
            errors.append(f"{user.name}: Error {str(e)}")
            
    try:
        db.commit()
    except Exception as e:
        return {"status": "error", "message": str(e)}

    return {
        "status": "completed",
        "updated_users": updated,
        "not_found_or_error": errors
    }

@router.get("/connectivity")
async def check_connectivity():
    try:
        # Headers fake browser
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
            # Include custom auth headers if needed by API logic, but here we test connection mainly
        }
        # Merge with API Keys if exist
        if HEADERS:
            headers.update(HEADERS)

        print(f"Testing connection to {API_URL} with Browser Headers...")
        
        # Increased timeout to 25s
        response = requests.get(
            API_URL, 
            headers=headers, 
            params={"input_data": json.dumps({"list_info": {"row_count": 1}})},
            verify=False,
            timeout=25 
        )
        return {
            "status": "success" if response.status_code == 200 else "error",
            "http_code": response.status_code,
            "url": API_URL,
            "latency": response.elapsed.total_seconds(),
            "headers_sent": dict(response.request.headers),
            "response_snippet": response.text[:200]
        }
    except Exception as e:
        return {
            "status": "exception",
            "error": str(e),
            "url": API_URL
        }
