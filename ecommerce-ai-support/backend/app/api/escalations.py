from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.schemas import EscalationRequest, EscalationResponse
from app.models.database import get_db
from app.services.escalation_manager import EscalationManager
from app.utils.logger import logger

router = APIRouter()

@router.post("/tickets", response_model=EscalationResponse)
async def create_escalation_ticket(request: EscalationRequest, db: Session = Depends(get_db)):
    """
    Create escalation ticket for complex issues
    """
    try:
        ticket_id = EscalationManager.create_escalation_ticket(
            db=db,
            conversation_id=request.conversation_id,
            customer_id=request.customer_id,
            reason=request.reason,
            priority=request.priority
        )
        
        if not ticket_id:
            raise HTTPException(status_code=500, detail="Failed to create escalation ticket")
        
        ticket_data = EscalationManager.get_ticket(db, ticket_id)
        
        logger.info(f"Escalation ticket created: {ticket_id}")
        
        return EscalationResponse(
            ticket_id=ticket_data["ticket_id"],
            conversation_id=ticket_data["conversation_id"],
            customer_id=ticket_data["customer_id"],
            reason=ticket_data["reason"],
            priority=ticket_data["priority"],
            status=ticket_data["status"],
            created_at=ticket_data["created_at"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating escalation ticket: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tickets/{ticket_id}")
async def get_escalation_ticket(ticket_id: str, db: Session = Depends(get_db)):
    """
    Get escalation ticket details
    """
    try:
        ticket = EscalationManager.get_ticket(db, ticket_id)
        
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        return ticket
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving ticket: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/tickets/{ticket_id}/status")
async def update_ticket_status(
    ticket_id: str,
    new_status: str,
    resolution: str = None,
    db: Session = Depends(get_db)
):
    """
    Update ticket status
    """
    try:
        success = EscalationManager.update_ticket_status(
            db=db,
            ticket_id=ticket_id,
            new_status=new_status,
            resolution=resolution
        )
        
        if not success:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        return {
            "ticket_id": ticket_id,
            "status": new_status,
            "message": "Ticket status updated successfully"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating ticket status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/tickets/{ticket_id}/assign")
async def assign_ticket(ticket_id: str, agent_id: str, db: Session = Depends(get_db)):
    """
    Assign ticket to support agent
    """
    try:
        success = EscalationManager.assign_ticket(db, ticket_id, agent_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        return {
            "ticket_id": ticket_id,
            "assigned_to": agent_id,
            "message": "Ticket assigned successfully"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error assigning ticket: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pending")
async def get_pending_tickets(priority: str = None, limit: int = 10, db: Session = Depends(get_db)):
    """
    Get pending escalation tickets
    """
    try:
        tickets = EscalationManager.get_pending_tickets(db, priority, limit)
        
        return {
            "tickets": tickets,
            "count": len(tickets)
        }
    
    except Exception as e:
        logger.error(f"Error retrieving pending tickets: {e}")
        raise HTTPException(status_code=500, detail=str(e))
