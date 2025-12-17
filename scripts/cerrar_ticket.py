import requests
import json
import warnings

# Suppress warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

API_URL = "https://helpdesk.estrategias.co:9010/api/v3/requests"
TOKEN = "0A6475A1-D3A4-4B74-B608-01D75A14B307"

headers = {
    "TECHNICIAN_KEY": TOKEN
}

def obtener_info_ticket(ticket_id):
    try:
        url = f"{API_URL}/{ticket_id}"
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            req = data.get("request", {})
            return {
                "exito": True,
                "asunto": req.get("subject", "Sin asunto"),
                "status": req.get("status", {}).get("name", "N/A"),
                "category": req.get("category"), # Puede ser None
                "subcategory": req.get("subcategory"),
                "item": req.get("item"),
                "udf_fields": req.get("udf_fields", {})
            }
        return {"exito": False}, {}
    except Exception as e:
        return {"exito": False, "error": str(e)}, {}

def cerrar_ticket(ticket_id, resolucion, info_actual):
    url = f"{API_URL}/{ticket_id}"
    
    # Construir payload base
    request_data = {
        "status": {
            "name": "Cerrado"
        },
        "resolution": {
            "content": resolucion
        }
    }

    # Reutilizar clasificación existente si la hay
    if info_actual.get("category"):
        request_data["category"] = {"name": info_actual["category"]["name"]}
    
    if info_actual.get("subcategory"):
        request_data["subcategory"] = {"name": info_actual["subcategory"]["name"]}

    if info_actual.get("item"):
        request_data["item"] = {"name": info_actual["item"]["name"]}

    # Manejar campos UDF específicos (Región)
    # Se intenta preservar lo que venga, específicamente udf_pick_2101 que suele ser obligatorio
    udf_actuales = info_actual.get("udf_fields", {})
    
    # Asegurar valor por defecto para udf_pick_2101
    if not udf_actuales.get("udf_pick_2101"):
        udf_actuales["udf_pick_2101"] = "CESAR"

    if udf_actuales:
         # Filtrar solo los que no sean nulos o vacíos para evitar problemas
         udf_limpios = {k: v for k, v in udf_actuales.items() if v is not None}
         if udf_limpios:
             request_data["udf_fields"] = udf_limpios

    payload = {
        "request": request_data
    }

    try:
        response = requests.put(
            url,
            headers=headers,
            data={"input_data": json.dumps(payload)},
            verify=False,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("response_status", {}).get("status") == "success":
                return True, "Ticket cerrado exitosamente."
            else:
                msgs = data.get("response_status", {}).get("messages", [])
                msg_text = msgs[0].get("message") if msgs else "Error desconocido de API"
                if msgs and "fields" in msgs[0]:
                    msg_text += f" Campos faltantes: {msgs[0]['fields']}"
                return False, f"API Error: {msg_text}"
        else:
            return False, f"HTTP Error {response.status_code}: {response.text}"

    except Exception as e:
        return False, f"Excepción: {e}"

# --- Main ---

print("=== CERRAR TICKET VIA API ===")
ticket_id = input("Ingresa el ID del ticket a cerrar: ").strip()

if not ticket_id:
    print("ID inválido.")
    exit()

# 1. Obtener y mostrar info actual
info = obtener_info_ticket(ticket_id)

if not info["exito"]:
    print(f" No se pudo leer el ticket {ticket_id}. Posible error de red o ID incorrecto.")
    exit()

print(f"\nTicket encontrado: {info['asunto']}")
print(f"Estado Actual: {info['status']}")
print(f"Clasificación Actual detectada:")
print(f" - Categoría: {info.get('category', {}).get('name', 'N/A') if info.get('category') else 'N/A'}")
print(f" - Subcategoría: {info.get('subcategory', {}).get('name', 'N/A') if info.get('subcategory') else 'N/A'}")
print(f" - Item: {info.get('item', {}).get('name', 'N/A') if info.get('item') else 'N/A'}")

estado_actual = info['status']
if estado_actual in ["Closed", "Cerrado", "Resolved", "Resuelto"]:
    print("  Este ticket ya parece estar cerrado.")
    if input("¿Continuar? (S/N): ").lower() != 's':
        exit()

# 2. Pedir Resolución
resolucion = input("\nIngresa la RESOLUCIÓN (obligatoria): ").strip()
if not resolucion:
    print(" La resolución es obligatoria.")
    exit()

# 3. Confirmar y Cerrar
confirmacion = input("\n¿Confirmar cierre reutilizando datos existentes? (S/N): ").lower()

if confirmacion == "s":
    exito, mensaje = cerrar_ticket(ticket_id, resolucion, info)
    
    if exito:
        print(f"\n {mensaje}")
    else:
        print(f"\n {mensaje}")
else:
    print("\nOperación cancelada.")
