from fastapi import APIRouter, HTTPException, Depends
from services.helpdesk_service import get_ticket_details
from pydantic import BaseModel
from typing import Optional

router = APIRouter(
    prefix="/api/tickets",
    tags=["tickets"]
)

class TicketDetail(BaseModel):
    id: str | int
    subject: str
    status: str
    priority: str
    requester: str
    technician: str
    group: str
    created_time: str
    description: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    item: Optional[str] = None

@router.get("/{ticket_id}", response_model=TicketDetail)
def get_ticket(ticket_id: str):
    ticket = get_ticket_details(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return ticket
