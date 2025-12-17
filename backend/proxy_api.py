from fastapi import FastAPI, Request, Response
import requests
import uvicorn

# Configuración
TARGET_BASE_URL = "https://helpdesk.estrategias.co:9010"
PORT = 9999

app = FastAPI(title="Helpdesk Relay Proxy")

@app.get("/")
def health_check():
    print("✅ Health Check received!")
    return {"status": "Proxy is running", "target": TARGET_BASE_URL}

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def proxy_request(path: str, request: Request):
    """
    Recibe la petición desde Render y la reenvía a la API localmente.
    """
    target_url = f"{TARGET_BASE_URL}/{path}"
    
    print(f"⬇️ REQUEST RECEIVED")
    print(f"👉 Method: {request.method}")
    print(f"👉 Target: {target_url}")
    print(f"👉 Params: {dict(request.query_params)}")

    # 1. Preparar Headers (Limpiando Host para evitar errores SSL/Routing)
    headers = dict(request.headers)
    headers.pop("host", None)
    headers.pop("content-length", None)
    
    headers["User-Agent"] = "Mozilla/5.0 (Proxy Relay)"

    # 2. Leer Body
    body = await request.body()

    try:
        # 3. Forward Request
        resp = requests.request(
            method=request.method,
            url=target_url,
            params=dict(request.query_params),
            data=body,
            headers=headers,
            verify=False, 
            timeout=30
        )
        
        print(f"⬆️ RESPONSE FROM HELPDESK")
        print(f"👈 Status: {resp.status_code}")
        print(f"👈 Body Preview: {resp.text[:200]}...") # Print first 200 chars

        # 4. Retornar Respuesta
        
        # 4. Retornar Respuesta tal cual
        # Excluir headers problemáticos de hop-by-hop
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers_response = {
            k: v for k, v in resp.headers.items() 
            if k.lower() not in excluded_headers
        }

        return Response(
            content=resp.content,
            status_code=resp.status_code,
            headers=headers_response
        )

    except Exception as e:
        print(f"❌ Error en Proxy: {e}")
        return Response(content=f"Proxy Error: {str(e)}", status_code=502)

if __name__ == "__main__":
    print(f"🚀 Iniciando Proxy Relay en puerto {PORT}...")
    print(f"📡 Destino: {TARGET_BASE_URL}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
