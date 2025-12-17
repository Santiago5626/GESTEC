from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import dashboard, auth

app = FastAPI(title="Helpdesk API", version="1.0.0")

# Configuración CORS
origins = [
    "http://localhost:5173", # Vite default
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(dashboard.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Helpdesk API is running"}
