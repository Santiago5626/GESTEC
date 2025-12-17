import requests
import json
import re

API_URL = "https://helpdesk.estrategias.co:9010/api/v3/requests"
TOKEN = "0A6475A1-D3A4-4B74-B608-01D75A14B307"

def obtener_detalle_ticket(ticket_id):
    url = f"{API_URL}/{ticket_id}"

    headers = {
        "TECHNICIAN_KEY": TOKEN
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f" Error {response.status_code}: {response.text}")
        return None

    data = response.json()
    ticket = data.get("request", {})

    return ticket

# Solicitar el ID del ticket
ticket_id = input("Ingresa el número del ticket del que deseas obtener información completa: ")

detalle = obtener_detalle_ticket(ticket_id)

if detalle:
    print(f"\n Detalle del ticket #{ticket_id}:\n")

    # Información básica
    print("--- Información Básica ---")
    print(f"ID: {detalle.get('id', 'N/A')}")
    print(f"Asunto: {detalle.get('subject', 'N/A')}")
    # Limpiar HTML de la descripción
    descripcion_html = detalle.get('description', 'N/A')
    descripcion_limpia = re.sub(r'<[^>]+>', '', descripcion_html).strip()
    print(f"Descripción: {descripcion_limpia}")
    print(f"Creado por: {detalle.get('created_by', {}).get('name', 'N/A')} ({detalle.get('created_time', {}).get('display_value', 'N/A')})")
    print(f"Última actualización: {detalle.get('last_updated_time', {}).get('display_value', 'N/A')}")

    # Solicitante
    print("\n--- Solicitante ---")
    requester = detalle.get('requester', {})
    print(f"Nombre: {requester.get('name', 'N/A')}")
    print(f"Email: {requester.get('email_id', 'N/A')}")
    print(f"Departamento: {requester.get('department', {}).get('name', 'N/A') if requester.get('department') else 'N/A'}")

    # Técnico asignado
    print("\n--- Técnico Asignado ---")
    technician = detalle.get('technician', {})
    print(f"Nombre: {technician.get('name', 'N/A')}")
    print(f"Email: {technician.get('email_id', 'N/A')}")
    print(f"Grupo: {detalle.get('group', {}).get('name', 'N/A')}")

    # Estado y Prioridad
    print("\n--- Estado y Prioridad ---")
    print(f"Estado: {detalle.get('status', {}).get('name', 'N/A')}")
    print(f"Prioridad: {detalle.get('priority', {}).get('name', 'N/A')}")
    print(f"Nivel: {detalle.get('level', {}).get('name', 'N/A')}")

    # Categorías
    print("\n--- Categorías ---")
    print(f"Categoría: {(detalle.get('category') or {}).get('name', 'N/A')}")
    print(f"Subcategoría: {(detalle.get('subcategory') or {}).get('name', 'N/A')}")
    print(f"Servicio: {(detalle.get('service_category') or {}).get('name', 'N/A')}")
    print(f"Item: {(detalle.get('item') or {}).get('name', 'N/A')}")

    # Tiempos
    print("\n--- Tiempos ---")
    print(f"Tiempo de respuesta inicial: {detalle.get('first_response_due_by_time', {}).get('display_value', 'N/A')}")
    print(f"Vencimiento: {detalle.get('due_by_time', {}).get('display_value', 'N/A')}")
    print(f"SLA: {detalle.get('sla', {}).get('name', 'N/A')}")

    # Campos personalizados
    udf = detalle.get('udf_fields', {})
    if udf:
        print("\n--- Campos Personalizados ---")
        for key, value in udf.items():
            print(f"{key}: {value}")

    # Adjuntos y notas
    print("\n--- Adjuntos y Notas ---")
    print(f"Tiene adjuntos: {detalle.get('has_attachments', False)}")
    print(f"Tiene notas: {detalle.get('has_notes', False)}")
    print(f"Tiene resolución: {bool(detalle.get('resolution', {}).get('content'))}")

else:
    print("⚠️ No se pudo obtener el detalle del ticket.")
