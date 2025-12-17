from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from typing import List, Optional
from services.helpdesk_service import get_tickets_for_technician

router = APIRouter(
    prefix="/api/dashboard",
    tags=["dashboard"]
)

# Schemas
class StatData(BaseModel):
    completed: int
    in_service: int
    open: int
    this_month: int

class RecentTicket(BaseModel):
    id: str | int
    status: str
    title: str
    user_role: str
    date: str
    priority: str

class DashboardResponse(BaseModel):
    user_name: str
    open_tickets_count: int
    stats: StatData
    recent_tickets: List[RecentTicket]

# Helper para "decodificar" el usuario del token (Mock)
async def get_current_user_id(technician_key: Optional[str] = Header(None, alias="X-Technician-ID")):
    # En una app real, decodificaríamos el JWT para sacar el ID.
    # Aquí confiamos en que el frontend nos envíe el ID que le dimos en el login
    # O, si no lo envía, no podemos mostrar datos reales.
    return technician_key

@router.get("/stats", response_model=DashboardResponse)
async def get_dashboard_stats(
    tech_id: Optional[str] = Header(None, alias="X-Technician-ID"), 
    user_name: Optional[str] = Header("Usuario", alias="X-User-Name")
):
    print(f"DEBUG: Dashboard Request - Tech ID: {tech_id}")
    
    tickets = []
    if tech_id and tech_id != "None":
         try:
            tickets = await get_tickets_for_technician(tech_id)
            print(f"DEBUG: Tickets found: {len(tickets)}")
         except Exception as e:
            print(f"DEBUG: Error fetching tickets: {e}")
    else:
        print("DEBUG: No Tech ID provided or is None")
    
    # Calcular estadísticas básicas basadas en los tickets obtenidos
    open_count = len([t for t in tickets if t['status'] in ['Open', 'Abierto']])
    in_service_count = len([t for t in tickets if t['status'] not in ['Open', 'Abierto', 'Closed', 'Cerrado']])
    
    # Mockeamos "Completed" y "This Month"
    completed_mock = 57 
    this_month_mock = len(tickets) + 3 
    
    return {
        "user_name": user_name, # Return the header passed or default
        "open_tickets_count": len(tickets),
        "stats": {
            "completed": completed_mock,
            "in_service": in_service_count,
            "open": open_count,
            "this_month": this_month_mock
        },
        "recent_tickets": tickets[:10] # Top 10 recent
    }
