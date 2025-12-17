import requests
import json


# Suppress stats warning
import warnings
from urllib.parse import urlencode

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

URL = "https://helpdesk.estrategias.co:9010/api/v3/requests"
TOKEN = "0A6475A1-D3A4-4B74-B608-01D75A14B307"

headers = {
    "TECHNICIAN_KEY": TOKEN,
    "Content-Type": "application/json"
}

# Configuración de paginación
ROW_COUNT = 100
start_index = 1
all_tickets = []

# Solicitar ID
default_id = "309901"
tech_input = input(f"Ingresa el ID del técnico (Default {default_id}): ").strip()
technician_id = tech_input if tech_input else default_id

print(f"Buscando tickets para técnico ID {technician_id}... (esto puede tomar un momento si hay muchos)")

while True:
    payload = {
        "list_info": {
            "row_count": ROW_COUNT,
            "start_index": start_index,
            "search_criteria": [
                {
                    "field": "technician.id",
                    "condition": "is",
                    "value": technician_id
                }
            ]
        }
    }

    try:
        response = requests.get(
            URL,
            headers=headers,
            params={"input_data": json.dumps(payload)},
            timeout=30,
            verify=False
        )
        response.raise_for_status()
        data = response.json()
        
        # Obtener tickets de la página actual
        current_page_tickets = data.get("requests", [])
        if not current_page_tickets:
            break
            
        all_tickets.extend(current_page_tickets)
        
        # Verificar si hay más páginas
        list_info = data.get("list_info", {})
        if list_info.get("has_more_rows", False):
            start_index += ROW_COUNT
            print(f" Cargando página siguiente (iniciando en {start_index})...")
        else:
            break

    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
        if 'response' in locals():
            print(f"Response Text: {response.text}")
        break # Salir del loop en error
    except Exception as e:
        print(f"Error: {e}")
        break

# Filtrado y visualización
tickets_filtrados = []

for req in all_tickets:
    status_name = req.get('status', {}).get('name', 'N/A')
    # Filtrar cerrados
    if status_name in ['Closed', 'Cerrado']:
        continue
    tickets_filtrados.append(req)

if not tickets_filtrados:
    print("No se encontraron tickets abiertos o en servicio.")
else:
    print(f"\nSe encontraron {len(tickets_filtrados)} tickets activos:\n")
    for req in tickets_filtrados:
        status_name = req.get('status', {}).get('name', 'N/A')
        print(
            f"ID: {req['id']} | "
            f"Asunto: {req['subject']} | "
            f"Técnico: {req.get('technician', {}).get('name', 'N/A')} | "
            f"Estado: {status_name}"
        )
