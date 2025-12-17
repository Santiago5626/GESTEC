from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import dashboard, auth, tickets

app = FastAPI(title="Helpdesk API", version="1.0.0")

# Configuración CORS
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "*" # Permitir todo para producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
from routers import dashboard, auth, tickets, notifications, debug

app.include_router(dashboard.router)
app.include_router(auth.router)
app.include_router(tickets.router)
app.include_router(notifications.router)
app.include_router(debug.router)

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.push_service import check_new_tickets_job

@app.on_event("startup")
async def start_scheduler():
    scheduler = AsyncIOScheduler()
    # Check every 5 minutes (300 seconds)
    scheduler.add_job(check_new_tickets_job, "interval", seconds=300)
    scheduler.start()
    print("Scheduler started for ticket polling.")

@app.get("/")
async def root():
    return {"message": "Helpdesk API is running"}
