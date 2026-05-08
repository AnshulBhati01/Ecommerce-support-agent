from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Boolean, JSON, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.pool import NullPool, StaticPool
from app.config import Settings
from datetime import datetime
import uuid

settings = Settings()

# Use StaticPool for SQLite (single-file DB), NullPool for PostgreSQL
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=settings.SQLALCHEMY_ECHO
    )
else:
    engine = create_engine(
        settings.DATABASE_URL,
        poolclass=NullPool,
        echo=settings.SQLALCHEMY_ECHO
    )

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db() -> Session:
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database Models
class Customer(Base):
    __tablename__ = "customers"
    
    customer_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    vip_status = Column(Boolean, default=False)

class Order(Base):
    __tablename__ = "orders"
    
    order_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(String(36), ForeignKey("customers.customer_id"), nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), nullable=False, default="pending")
    total_amount = Column(Float, nullable=True)
    shipping_address = Column(Text, nullable=True)
    tracking_number = Column(String(100), nullable=True)
    expected_delivery = Column(DateTime, nullable=True)

class OrderItem(Base):
    __tablename__ = "order_items"
    
    item_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(String(36), ForeignKey("orders.order_id"), nullable=False)
    product_id = Column(String(36), nullable=False)
    product_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)

class Return(Base):
    __tablename__ = "returns"
    
    return_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(String(36), ForeignKey("orders.order_id"), nullable=False)
    customer_id = Column(String(36), ForeignKey("customers.customer_id"), nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    approved_at = Column(DateTime, nullable=True)
    refund_amount = Column(Float, nullable=True)

class Conversation(Base):
    __tablename__ = "conversations"
    
    conversation_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(String(36), ForeignKey("customers.customer_id"), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    status = Column(String(50), nullable=False, default="active")
    escalated = Column(Boolean, default=False)
    escalation_ticket_id = Column(String(36), nullable=True)
    satisfaction_score = Column(Integer, nullable=True)

class Message(Base):
    __tablename__ = "messages"
    
    message_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String(36), ForeignKey("conversations.conversation_id"), nullable=False)
    sender_type = Column(String(20), nullable=False)  # 'customer', 'ai', 'human'
    sender_id = Column(String(255), nullable=True)
    message_text = Column(Text, nullable=False)
    intent = Column(String(100), nullable=True)
    entities = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class EscalationTicket(Base):
    __tablename__ = "escalation_tickets"
    
    ticket_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String(36), ForeignKey("conversations.conversation_id"), nullable=False)
    customer_id = Column(String(36), ForeignKey("customers.customer_id"), nullable=False)
    reason = Column(Text, nullable=False)
    priority = Column(String(50), nullable=False, default="medium")
    assigned_to = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False, default="open")
    resolution = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

class InteractionLog(Base):
    __tablename__ = "interaction_logs"
    
    log_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String(36), ForeignKey("conversations.conversation_id"), nullable=True)
    interaction_type = Column(String(100), nullable=False)
    resolution_type = Column(String(50), nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    customer_satisfaction = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """Drop all database tables (use with caution)"""
    Base.metadata.drop_all(bind=engine)
