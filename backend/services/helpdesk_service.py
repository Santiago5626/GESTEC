import requests
import json
import warnings
from typing import Optional, Dict, List

import os

# Suppress warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# Default to original, but verify if ENV VAR is set (useful for proxy/tunnel)
DEFAULT_URL = "https://helpdesk.estrategias.co:9010/api/v3/requests"
API_URL = os.getenv("HELPDESK_API_URL", DEFAULT_URL)

TOKEN = "0A6475A1-D3A4-4B74-B608-01D75A14B307"

HEADERS = {
    "TECHNICIAN_KEY": TOKEN,
    "Content-Type": "application/json",
    # Bypass LocalTunnel reminder page
    "Bypass-Tunnel-Reminder": "true" 
}

# Simple in-memory cache for technician IDs to avoid repeated slow searches
# Pre-populated with known IDs if available, or empty
TECHNICIAN_CACHE = {
    "juan carlos carvajal": "60633", 
    "daniel acosta": "309901"
}

async def find_technician_id_by_name(name: str) -> Optional[str]:
    """
    Busca el ID de un técnico por su nombre escaneando tickets recientes.
    Retorna el ID si lo encuentra, o None.
    """
    name_lower = name.lower()
    
    # Check cache first
    if name_lower in TECHNICIAN_CACHE and TECHNICIAN_CACHE[name_lower]:
        return TECHNICIAN_CACHE[name_lower]

    print(f"Searching API for technician: {name}")
    
    # Logic adapted from scripts/buscar_tecnico.py
    limit = 1500
    chunk_size = 100
    start_index = 1
    total_processed = 0
    
    while total_processed < limit:
        current_row_count = min(chunk_size, limit - total_processed)
        
        payload = {
            "list_info": {
                "row_count": current_row_count,
                "start_index": start_index,
                "search_criteria": [
                    {"field": "status.name", "condition": "is_not", "value": "Closed"}
                ]
            }
        }
        
        try:
            response = requests.get(
                API_URL, 
                headers=HEADERS, 
                params={"input_data": json.dumps(payload)}, 
                verify=False,
                timeout=10
            )
            if response.status_code != 200:
                print(f"API Error: {response.status_code}")
                break
                
            data = response.json()
            requests_list = data.get("requests", [])
            
            if not requests_list:
                break
                
            for req in requests_list:
                tech = req.get('technician')
                if tech and 'id' in tech and 'name' in tech:
                    t_name = tech['name'].lower()
                    t_id = tech['id']
                    
                    # Update cache opportunistically
                    if t_name not in TECHNICIAN_CACHE:
                        TECHNICIAN_CACHE[t_name] = t_id
                    
                    # Fuzzy match
                    if name_lower in t_name:
                        TECHNICIAN_CACHE[name_lower] = t_id # Cache specific query
                        return t_id
            
            if not data.get("list_info", {}).get("has_more_rows", False):
                break
                
            start_index += len(requests_list)
            total_processed += len(requests_list)
            
        except Exception as e:
            print(f"Error searching technician: {e}")
            break
            
    return None

async def get_tickets_for_technician(technician_id: str) -> List[Dict]:
    """
    Obtiene los tickets abiertos/en servicio para un ID de técnico específico.
    Utiliza caché en memoria (TTL 5 min) para optimizar.
    """
    
    # Simple Dictionary Cache: {tech_id: {'timestamp': time, 'data': []}}
    # Nota: En una app real usar Redis. Aquí usamos variable global por simplicidad.
    if not hasattr(get_tickets_for_technician, "cache"):
        get_tickets_for_technician.cache = {}
        
    import time
    CACHE_TTL = 300 # 5 minutos
    
    now = time.time()
    cached = get_tickets_for_technician.cache.get(technician_id)
    
    if cached and (now - cached['timestamp'] < CACHE_TTL):
        print(f"DEBUG: Returning cached tickets for {technician_id}")
        return cached['data']
    if not technician_id:
        return []

    print(f"Fetching tickets for ID: {technician_id}")
    all_tickets = []
    start_index = 1
    row_count = 50 
    
    # Limit to 100 tickets max for dashboard performance
    max_tickets = 100 
    
    while len(all_tickets) < max_tickets:
        payload = {
            "list_info": {
                "row_count": row_count,
                "start_index": start_index,
                "sort_field": "created_time",
                "sort_order": "desc",
                "search_criteria": [
                    {"field": "technician.id", "condition": "is", "value": technician_id}
                ]
            }
        }

        try:
            response = requests.get(
                API_URL,
                headers=HEADERS,
                params={"input_data": json.dumps(payload)},
                verify=False,
                timeout=20
            )
            
            if response.status_code != 200:
                print(f"DEBUG: API returned {response.status_code}")
                break
                
            data = response.json()
            requests_list = data.get("requests", [])
            print(f"DEBUG: Found {len(requests_list)} tickets in page starting {start_index} for tech {technician_id}")
            
            if not requests_list:
                break
                
            # Filter Closed just in case api returns them (though search criteria should handle it if specificied)
            # API docs say request search criteria works.
            
            for req in requests_list:
                status = req.get('status', {}).get('name', 'N/A')
                if status not in ['Closed', 'Cerrado', 'Resolved', 'Resuelto']:
                     all_tickets.append({
                        "id": req.get("id"),
                        "title": req.get("subject"),
                        "status": status,
                        "priority": req.get("priority", {}).get("name", "Media"),
                        "date": req.get("created_time", {}).get("display_value", "N/A"),
                        "user_role": req.get("requester", {}).get("name", "Desconocido") # Using requester as secondary info line
                     })

            if not data.get("list_info", {}).get("has_more_rows", False):
                break
                
            start_index += len(requests_list)
            
        except Exception as e:
            print(f"Error fetching tickets: {e}")
            break

    # Save to cache
    get_tickets_for_technician.cache[technician_id] = {
        'timestamp': time.time(),
        'data': all_tickets
    }
    
    return all_tickets

async def get_ticket_details(ticket_id: str) -> Optional[Dict]:
    """
    Obtiene los detalles completos de un ticket específico.
    """
    url = f"{API_URL}/{ticket_id}"
    print(f"Fetching details for ticket: {ticket_id}")
    
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            verify=False,
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"Error fetching ticket details: {response.status_code}")
            return None
            
        data = response.json()
        req = data.get("request", {})
        
        if not req:
            return None
            
        return {
            "id": req.get("id"),
            "subject": req.get("subject"),
            "status": (req.get("status") or {}).get("name"),
            "priority": (req.get("priority") or {}).get("name", "Baja"),
            "requester": (req.get("requester") or {}).get("name", "Desconocido"),
            "technician": (req.get("technician") or {}).get("name", "Sin asignar"),
            "group": (req.get("group") or {}).get("name", "General"),
            "created_time": (req.get("created_time") or {}).get("display_value"),
            "description": req.get("description", "Sin descripción"),
            "category": (req.get("category") or {}).get("name"),
            "subcategory": (req.get("subcategory") or {}).get("name"),
            "item": (req.get("item") or {}).get("name"),
        }
        
    except Exception as e:
        print(f"Exception fetching ticket details: {e}")
        return None
