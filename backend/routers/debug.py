from fastapi import APIRouter
import requests
import json
from services.helpdesk_service import API_URL, HEADERS

router = APIRouter(prefix="/api/debug")

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
