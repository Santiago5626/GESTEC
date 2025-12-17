# Documentación API Helpdesk

Este repositorio contiene una colección de scripts en Python diseñados para interactuar con la API v3 de ManageEngine ServiceDesk Plus (Helpdesk). Los scripts permiten realizar consultas sobre técnicos, tickets y tareas para facilitar la administración y el monitoreo.

## Requisitos

- Python 3.x
- Librería `requests`

Para instalar las dependencias:
```bash
pip install requests
```

## Configuración

Los scripts utilizan una variable `TOKEN` o `TECHNICIAN_KEY` para autenticarse. Asegúrate de que esta clave sea válida y tenga los permisos necesarios en la instancia de Helpdesk.

> **Nota:** La URL base configurada en los scripts es `https://helpdesk.estrategias.co:9010`.

Para detalles técnicos sobre los endpoints y la autenticación, consulta [API_DOCS.md](API_DOCS.md).

## Descripción de los Scripts

A continuación se detalla la funcionalidad de cada script incluido en el repositorio:

### 1. `inspect_ticket.py`
**Propósito:** Realiza una inspección rápida de un ticket específico.
- **Funcionamiento:** Consulta la API por un ID de ticket predefinido en el código (`5939449`) y muestra la respuesta JSON completa.
- **Uso:** Útil para depuración y para ver la estructura cruda de un ticket.

### 2. `pruebatecnico.py`
**Propósito:** Verificar la identidad y conexión del técnico actual.
- **Funcionamiento:** Consulta el endpoint `/technicians/me` usando el token configurado.
- **Salida:** Imprime el código de estado HTTP y la respuesta con los datos del técnico asociado al token.

### 3. `buscar_tecnico.py`
**Propósito:** Buscar el ID de un técnico por su nombre (Método Indirecto).
- **Limitación:** El usuario actual no tiene permisos para listar técnicos directamente.
- **Solución:** El script analiza los últimos 500 tickets globales para "descubrir" técnicos activos.
- **Uso:** Ejecutar y escribir el nombre. *Nota: Solo encontrará técnicos que tengan tickets activos recientes.*

### 5. `test_api.py`
**Propósito:** Pruebas generales de búsqueda de tareas.
- **Funcionamiento:** Envía una petición `POST` para buscar tareas asociadas a un `owner.id` específico (`333630`).
- **Campos solicitados:** ID, título, estado, prioridad, grupo, propietario, fecha programada.

### 6. `ticket_detalle.py`
**Propósito:** Consultar información detallada de un ticket específico ingresado por el usuario.
- **Funcionamiento:**
  - Solicita al usuario el ID del ticket.
  - Muestra información organizada: Básica, Solicitante, Técnico, Estado, Categorías, Tiempos, Campos personalizados y Adjuntos.
  - Limpia el formato HTML de la descripción para una lectura más clara.

### 7. `tickets_abiertos.py`
**Propósito:** Buscar tickets abiertos asignados a un técnico (método XML).
- **Funcionamiento:**
  - Utiliza el endpoint antiguo `/sdpapi/request` con formato XML.
  - Solicita el ID numérico del técnico.
  - Filtra los tickets para mostrar solo los que tienen estado "Abierto".

### 8. `tickets_abiertos_por_id.py`
**Propósito:** Buscar tickets abiertos asignados a un técnico (método JSON API v3).
- **Funcionamiento:**
  - Utiliza el endpoint `/api/v3/requests`.
  - Filtra en la API los tickets que **no** están cerrados ("Closed").
  - Realiza un filtrado adicional en el cliente para mostrar solo los del técnico ID `309901`.
  - Intenta mostrar ID, Asunto, Técnico y Estado.

### 9. `cerrar_ticket.py`
**Propósito:** Cerrar un ticket existente de forma inteligente.
- **Problema:** La API rechaza el cierre si no se envían nuevamente los datos de clasificación (Categoría, Subcategoría, Item, Región).
- **Solución Inteligente:**
  - El script primero consulta (GET) los datos actuales del ticket.
  - Detecta automáticamente la clasificación existente.
  - Solicita la resolución al usuario.
  - Envía la petición de cierre (PUT) reutilizando los datos de clasificación originales para evitar errores de validación.
- **Uso:** Ejecutar, ingresar ID y resolución. El script se encarga de los campos técnicos.

---
