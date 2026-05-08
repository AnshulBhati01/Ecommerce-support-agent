from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.schemas import (
    ChatRequest, ChatResponse, ConversationStart, ConversationResponse, MessageHistory
)
from app.models.database import get_db, Conversation, Message
from app.services.intent_classifier import IntentClassifier
from app.services.rag_pipeline import RAGSystem
from app.services.order_manager import OrderManager
from app.utils.logger import logger
from app.utils.cache import cache
from datetime import datetime
import uuid

router = APIRouter()

@router.post("/message", response_model=ChatResponse)
async def send_message(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Process customer message and generate AI response
    """
    try:
        # Initialize services
        intent_classifier = IntentClassifier()
        rag_system = RAGSystem()
        
        # Classify intent
        intent, confidence = intent_classifier.classify_intent(request.message)
        
        # Extract entities
        entities = intent_classifier.extract_entities(request.message)
        
        # Get order context if available
        order_data = None
        if "order_id" in entities:
            order_data = OrderManager.get_order_by_id(db, entities["order_id"])
        
        # Generate response using RAG
        response_data = rag_system.generate_response(
            query=request.message,
            intent=intent,
            order_data=order_data
        )
        
        # Store message in database
        message_id = str(uuid.uuid4())
        message = Message(
            message_id=message_id,
            conversation_id=request.conversation_id,
            sender_type="customer",
            message_text=request.message,
            intent=intent,
            entities=entities
        )
        db.add(message)
        
        # Store AI response
        ai_message_id = str(uuid.uuid4())
        ai_message = Message(
            message_id=ai_message_id,
            conversation_id=request.conversation_id,
            sender_type="ai",
            message_text=response_data["response"],
            intent=intent
        )
        db.add(ai_message)
        db.commit()
        
        # Determine if escalation is needed
        requires_escalation = confidence < 0.6 or intent == "escalation"
        
        logger.info(f"Message processed: intent={intent}, confidence={confidence:.2f}")
        
        return ChatResponse(
            message_id=ai_message_id,
            response=response_data["response"],
            intent=intent,
            requires_escalation=requires_escalation,
            context_used=response_data["context_used"]
        )
    
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/conversation/start", response_model=ConversationResponse)
async def start_conversation(request: ConversationStart, db: Session = Depends(get_db)):
    """
    Start a new conversation
    """
    try:
        conversation_id = str(uuid.uuid4())
        conversation = Conversation(
            conversation_id=conversation_id,
            customer_id=request.customer_id,
            status="active"
        )
        db.add(conversation)
        db.commit()
        
        logger.info(f"Conversation {conversation_id} started for customer {request.customer_id}")
        
        return ConversationResponse(
            conversation_id=conversation_id,
            customer_id=request.customer_id,
            status="active",
            started_at=conversation.started_at
        )
    
    except Exception as e:
        logger.error(f"Error starting conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversation/{conversation_id}")
async def get_conversation(conversation_id: str, db: Session = Depends(get_db)):
    """
    Retrieve conversation history
    """
    try:
        # Check cache first
        cache_key = f"conversation:{conversation_id}"
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        conversation = db.query(Conversation).filter(
            Conversation.conversation_id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at).all()
        
        result = {
            "conversation_id": conversation.conversation_id,
            "customer_id": conversation.customer_id,
            "status": conversation.status,
            "started_at": conversation.started_at,
            "ended_at": conversation.ended_at,
            "messages": [
                {
                    "message_id": msg.message_id,
                    "sender_type": msg.sender_type,
                    "message_text": msg.message_text,
                    "intent": msg.intent,
                    "created_at": msg.created_at
                }
                for msg in messages
            ]
        }
        
        # Cache for 1 hour
        cache.set(cache_key, result, ttl=3600)
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving conversation {conversation_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/conversation/{conversation_id}/end")
async def end_conversation(
    conversation_id: str,
    satisfaction_score: int = None,
    db: Session = Depends(get_db)
):
    """
    End a conversation
    """
    try:
        conversation = db.query(Conversation).filter(
            Conversation.conversation_id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        conversation.status = "closed"
        conversation.ended_at = datetime.utcnow()
        if satisfaction_score:
            conversation.satisfaction_score = satisfaction_score
        
        db.commit()
        
        # Clear cache
        cache.delete(f"conversation:{conversation_id}")
        
        logger.info(f"Conversation {conversation_id} ended")
        
        return {
            "status": "success",
            "message": "Conversation ended successfully",
            "satisfaction_score": satisfaction_score
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error ending conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))
