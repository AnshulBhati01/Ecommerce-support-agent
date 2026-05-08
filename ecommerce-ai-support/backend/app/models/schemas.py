from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

# Chat Models
class ChatRequest(BaseModel):
    conversation_id: str
    customer_id: str
    message: str

class ChatResponse(BaseModel):
    message_id: str
    response: str
    intent: str
    requires_escalation: bool
    context_used: int

class ConversationStart(BaseModel):
    customer_id: str

class ConversationResponse(BaseModel):
    conversation_id: str
    customer_id: str
    status: str
    started_at: datetime

class MessageHistory(BaseModel):
    message_id: str
    sender_type: str
    message_text: str
    intent: Optional[str]
    created_at: datetime

# Order Models
class OrderResponse(BaseModel):
    order_id: str
    customer_id: str
    status: str
    total_amount: Optional[float]
    tracking_number: Optional[str]
    expected_delivery: Optional[datetime]

class OrderItemResponse(BaseModel):
    product_name: str
    quantity: int
    unit_price: float
    total_price: float

class OrderDetailResponse(BaseModel):
    order_id: str
    customer_id: str
    order_date: datetime
    status: str
    total_amount: Optional[float]
    shipping_address: Optional[str]
    tracking_number: Optional[str]
    expected_delivery: Optional[datetime]
    items: List[OrderItemResponse]

# Escalation Models
class EscalationRequest(BaseModel):
    conversation_id: str
    customer_id: str
    reason: str
    priority: str = "medium"

class EscalationResponse(BaseModel):
    ticket_id: str
    conversation_id: str
    customer_id: str
    reason: str
    priority: str
    status: str
    created_at: datetime

# Customer Models
class CustomerRequest(BaseModel):
    email: str
    phone: Optional[str] = None
    vip_status: bool = False

class CustomerResponse(BaseModel):
    customer_id: str
    email: str
    phone: Optional[str]
    vip_status: bool
    created_at: datetime

# Return Models
class ReturnRequest(BaseModel):
    order_id: str
    customer_id: str
    reason: str

class ReturnResponse(BaseModel):
    return_id: str
    order_id: str
    customer_id: str
    reason: str
    status: str
    refund_amount: Optional[float]
    created_at: datetime

# Health Check
class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime
