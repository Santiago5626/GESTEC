from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db_sync # Use sync db

router = APIRouter(prefix="/api/debug")

@router.get("/refresh-ids")
def refresh_technician_ids(
    db: Session = Depends(get_db_sync), # Sync session 
    target_user: str = None, # Opcional: refrescar solo a "Juan"
    force_all: bool = False  # Opcional: forzar re-scan de todos
):
    """
    Actualiza IDs de técnicos. 
    Por defecto solo actualiza los que tienen technician_id nulo.
    """
    query = db.query(User)
    if target_user:
        query = query.filter(User.name.ilike(f"%{target_user}%"))
    
    users = query.all()
    updated = []
    errors = []
    skipped = []

    print(f"🔄 Starting ID refresh. Candidates: {len(users)}")
    
    count_processed = 0
    MAX_PROCESS = 3 # Evitar timeout de Render (30s) procesando max 3 usuarios a la vez

    for user in users:
        if count_processed >= MAX_PROCESS:
            errors.append("Batch limit reached (max 3). Run again.")
            break

        # Skip si ya tiene ID y no forzamos
        if user.technician_id and not force_all and not target_user:
            skipped.append(user.name)
            continue
            
        try:
            print(f"🔍 Searching ID for: {user.name}")
            count_processed += 1
            
            tech_id = find_technician_id_by_name(user.name)
            
            if tech_id:
                user.technician_id = tech_id
                updated.append(f"{user.name} -> {tech_id}")
            else:
                errors.append(f"{user.name}: Not found in active tickets scan")
        except Exception as e:
            errors.append(f"{user.name}: Error {str(e)}")
            
    try:
        db.commit()
    except Exception as e:
        return {"status": "error", "message": f"DB Commit Error: {str(e)}"}

    return {
        "status": "completed",
        "processed_count": count_processed,
        "updated_users": updated,
        "skipped_already_set": skipped,
        "errors_or_not_found": errors
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
