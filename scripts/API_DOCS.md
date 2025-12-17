# Documentación Técnica API ManageEngine ServiceDesk Plus

Este documento describe los detalles técnicos para interactuar con la API de ServiceDesk Plus observados en este repositorio.

## Configuración General

*   **URL Base:** `https://helpdesk.estrategias.co:9010`
*   **Seguridad:**
    *   Se requiere deshabilitar la verificación SSL (`verify=False`) en las peticiones debido al certificado autofirmado o interno.
    *   **Autenticación:** Se realiza mediante headers.

### Autenticación
Todas las peticiones deben incluir la clave de técnico en el header:

```python
headers = {
    "TECHNICIAN_KEY": "TU-TOKEN-AQUI"
}
```

## API V3 (Rest Moderno)

La versión 3 de la API utiliza JSON y sigue principios RESTful. Es la preferida para nuevas implementaciones.

### Endpoints Identificados

#### 1. Obtener Técnico Actual
*   **Método:** `GET`
*   **Endpoint:** `/api/v3/technicians/me`
*   **Descripción:** Retorna la información del técnico autenticado.

#### 2. Listar Técnicos
*   **Método:** `POST`
*   **Endpoint:** `/api/v3/technicians`
*   **Body (Form Data):**
    *   `input_data`: JSON string vacío `{}` para listar todos.
*   **Paginación:** La respuesta incluye `list_info.has_more_rows` para iterar páginas.

#### 3. Obtener Detalle de Ticket (Request)
*   **Método:** `GET`
*   **Endpoint:** `/api/v3/requests/{request_id}`
*   **Descripción:** Obtiene toda la información de un ticket por su ID.

#### 4. Listar Tickets (Requests) con Filtros
*   **Método:** `GET`
*   **Endpoint:** `/api/v3/requests`
*   **Parámetros:**
    *   `input_data`: JSON string con criterios de filtrado y paginación.
    ```json
    {
        "list_info": {
            "row_count": 50,
            "search_criteria": [
                {
                    "field": "status.name",
                    "condition": "is_not",
                    "value": "Closed"
                }
            ]
        }
    }
    ```

#### 5. Buscar Tareas (Tasks)
*   **Método:** `POST`
*   **Endpoint:** `/api/v3/tasks`
*   **Headers:** `Content-Type: application/json`
*   **Body (JSON):**
    ```json
    {
        "input_data": {
            "list_info": { "row_count": 25, "start_index": 1 },
            "search_fields": { "owner.id": "ID_DEL_TECNICO" },
            "fields_required": ["id", "title", "status"]
        }
    }
    ```

---

## API Legacy (XML)

Método antiguo utilizado para ciertas operaciones complejas o reportes específicos.

*   **Endpoint Base:** `/sdpapi/request`
*   **Método:** `GET` / `POST`

### Parámetros Requeridos
La API Legacy espera los parámetros como query params o form-data:

1.  `AUTHTOKEN`: Tu clave de técnico.
2.  `OPERATION_NAME`: Acción a realizar (ej. `GET_REQUESTS`).
3.  `INPUT_DATA`: XML con los filtros.

### Ejemplo de Filtro XML
Para filtrar tickets por ID de técnico:

```xml
<operation>
    <details>
        <list_info>
            <start_index>1</start_index>
            <row_count>1000</row_count>
            <filter_by>
                <field>technician.id</field>
                <criteria>is</criteria>
                <value>ID_TECNICO</value>
            </filter_by>
        </list_info>
    </details>
</operation>
```

---
*Generado automáticamente por Antigravity*
