from fastapi import APIRouter
import requests
import json
from services.helpdesk_service import API_URL, HEADERS

router = APIRouter(prefix="/api/debug")

@router.get("/connectivity")
async def check_connectivity():
    try:
        # Intento de conexión simple (ping o list tickets minimal)
        print(f"Testing connection to {API_URL}...")
        response = requests.get(
            API_URL, 
            headers=HEADERS, 
            params={"input_data": json.dumps({"list_info": {"row_count": 1}})},
            verify=False,
            timeout=10
        )
        return {
            "status": "success" if response.status_code == 200 else "error",
            "http_code": response.status_code,
            "url": API_URL,
            "response_snippet": response.text[:200]
        }
    except Exception as e:
        return {
            "status": "exception",
            "error": str(e),
            "url": API_URL
        }
