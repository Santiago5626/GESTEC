import requests
import json
import warnings

# Suppress warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

API_URL = "https://helpdesk.estrategias.co:9010/api/v3/requests"
TOKEN = "0A6475A1-D3A4-4B74-B608-01D75A14B307"

def buscar_tecnicos_en_tickets_recientes(nombre_busqueda):
    print("⚠️  Tu usuario no tiene permisos para listar técnicos directamente.")
    LIMIT = 1500
    print(f"🔍 Buscando técnicos analizando los últimos {LIMIT} tickets globales...")

    headers = {
        "TECHNICIAN_KEY": TOKEN,
        "Content-Type": "application/json"
    }

    tecnicos_encontrados = {}
    
    start_index = 1
    chunk_size = 100
    total_processed = 0

    while total_processed < LIMIT:
        # Calcular el tamaño del lote actual (por si faltan menos de 100 para llegar a 500)
        current_row_count = min(chunk_size, LIMIT - total_processed)
        
        print(f"   -> Descargando lote {start_index} a {start_index + current_row_count - 1}...")

        payload = {
            "list_info": {
                "row_count": current_row_count,
                "start_index": start_index,
                "search_criteria": [
                    {
                        "field": "status.name",
                        "condition": "is_not",
                        "value": "Closed"
                    }
                ]
            }
        }

        try:
            response = requests.get(
                API_URL,
                headers=headers,
                params={"input_data": json.dumps(payload)},
                timeout=30,
                verify=False
            )
            response.raise_for_status()
            data = response.json()
            
            requests_list = data.get("requests", [])
            
            if not requests_list:
                break

            # Procesar el lote
            for req in requests_list:
                tech = req.get('technician')
                if tech and 'id' in tech and 'name' in tech:
                    t_id = tech['id']
                    t_name = tech['name']
                    tecnicos_encontrados[t_id] = t_name

            count_in_batch = len(requests_list)
            total_processed += count_in_batch
            
            # Verificar si hay más en el servidor
            list_info = data.get("list_info", {})
            if not list_info.get("has_more_rows", False):
                break
                
            start_index += count_in_batch

        except Exception as e:
            print(f"❌ Error al analizar tickets en el lote {start_index}: {e}")
            break

    # Filtrar por búsqueda
    resultados = []
    for t_id, t_name in tecnicos_encontrados.items():
        if nombre_busqueda in t_name.lower():
            resultados.append({"id": t_id, "name": t_name})
    
    return resultados

if __name__ == "__main__":
    print("=== BUSCAR TÉCNICO EN TICKETS RECIENTES ===")
    nombre = input("Ingresa el nombre del técnico a buscar: ").strip().lower()

    if not nombre:
        print("Debes ingresar un nombre.")
        exit()

    encontrados = buscar_tecnicos_en_tickets_recientes(nombre)

    if encontrados:
        print(f"\n✅ Se encontraron {len(encontrados)} técnicos coinciden con '{nombre}':\n")
        for t in encontrados:
            print(f"ID: {t['id']} | Nombre: {t['name']}")
        print("\n(Nota: Solo se muestran técnicos que tengan tickets activos recientes)")
    else:
        print(f"\n❌ No se encontraron técnicos con ese nombre en los tickets analizados.")
