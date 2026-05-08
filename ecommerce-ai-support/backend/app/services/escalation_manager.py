from typing import Optional
from sqlalchemy.orm import Session
from app.models.database import EscalationTicket, Conversation
from app.utils.logger import logger
import uuid
from datetime import datetime

class EscalationManager:
    """Manage escalation workflows"""
    
    @staticmethod
    def create_escalation_ticket(
        db: Session,
        conversation_id: str,
        customer_id: str,
        reason: str,
        priority: str = "medium"
    ) -> Optional[str]:
        """Create escalation ticket"""
        try:
            ticket_id = str(uuid.uuid4())
            ticket = EscalationTicket(
                ticket_id=ticket_id,
                conversation_id=conversation_id,
                customer_id=customer_id,
                reason=reason,
                priority=priority,
                status="open"
            )
            db.add(ticket)
            
            # Update conversation
            conversation = db.query(Conversation).filter(
                Conversation.conversation_id == conversation_id
            ).first()
            if conversation:
                conversation.escalated = True
                conversation.escalation_ticket_id = ticket_id
            
            db.commit()
            logger.info(f"Escalation ticket {ticket_id} created")
            return ticket_id
        except Exception as e:
            logger.error(f"Error creating escalation ticket: {e}")
            db.rollback()
            return None
    
    @staticmethod
    def get_ticket(db: Session, ticket_id: str) -> Optional[dict]:
        """Get escalation ticket details"""
        try:
            ticket = db.query(EscalationTicket).filter(
                EscalationTicket.ticket_id == ticket_id
            ).first()
            
            if not ticket:
                return None
            
            return {
                "ticket_id": ticket.ticket_id,
                "conversation_id": ticket.conversation_id,
                "customer_id": ticket.customer_id,
                "reason": ticket.reason,
                "priority": ticket.priority,
                "status": ticket.status,
                "assigned_to": ticket.assigned_to,
                "resolution": ticket.resolution,
                "created_at": ticket.created_at,
                "resolved_at": ticket.resolved_at
            }
        except Exception as e:
            logger.error(f"Error retrieving ticket {ticket_id}: {e}")
            return None
    
    @staticmethod
    def update_ticket_status(
        db: Session,
        ticket_id: str,
        new_status: str,
        resolution: Optional[str] = None
    ) -> bool:
        """Update ticket status"""
        try:
            ticket = db.query(EscalationTicket).filter(
                EscalationTicket.ticket_id == ticket_id
            ).first()
            
            if ticket:
                ticket.status = new_status
                if resolution:
                    ticket.resolution = resolution
                    ticket.resolved_at = datetime.utcnow()
                
                db.commit()
                logger.info(f"Ticket {ticket_id} status updated to {new_status}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error updating ticket {ticket_id}: {e}")
            db.rollback()
            return False
    
    @staticmethod
    def assign_ticket(db: Session, ticket_id: str, agent_id: str) -> bool:
        """Assign ticket to support agent"""
        try:
            ticket = db.query(EscalationTicket).filter(
                EscalationTicket.ticket_id == ticket_id
            ).first()
            
            if ticket:
                ticket.assigned_to = agent_id
                db.commit()
                logger.info(f"Ticket {ticket_id} assigned to {agent_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error assigning ticket {ticket_id}: {e}")
            db.rollback()
            return False
    
    @staticmethod
    def get_pending_tickets(db: Session, priority: Optional[str] = None, limit: int = 10) -> list:
        """Get pending escalation tickets"""
        try:
            query = db.query(EscalationTicket).filter(
                EscalationTicket.status == "open"
            )
            
            if priority:
                query = query.filter(EscalationTicket.priority == priority)
            
            tickets = query.order_by(EscalationTicket.created_at).limit(limit).all()
            
            return [
                {
                    "ticket_id": ticket.ticket_id,
                    "customer_id": ticket.customer_id,
                    "priority": ticket.priority,
                    "reason": ticket.reason,
                    "created_at": ticket.created_at
                }
                for ticket in tickets
            ]
        except Exception as e:
            logger.error(f"Error retrieving pending tickets: {e}")
            return []
