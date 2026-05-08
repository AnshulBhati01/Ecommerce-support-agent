import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.database import create_tables, drop_tables, SessionLocal

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Setup test database"""
    create_tables()
    yield
    drop_tables()


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_readiness_check():
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_start_conversation():
    response = client.post(
        "/api/v1/chat/conversation/start",
        json={"customer_id": "test-customer-123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "conversation_id" in data
    assert data["customer_id"] == "test-customer-123"
    assert data["status"] == "active"


def test_send_message():
    # Start conversation
    conv_response = client.post(
        "/api/v1/chat/conversation/start",
        json={"customer_id": "test-customer-456"}
    )
    conversation_id = conv_response.json()["conversation_id"]
    
    # Send message
    response = client.post(
        "/api/v1/chat/message",
        json={
            "conversation_id": conversation_id,
            "customer_id": "test-customer-456",
            "message": "Where is my order?"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "intent" in data
    assert "requires_escalation" in data
    assert "message_id" in data


def test_get_conversation_history():
    # Start conversation
    conv_response = client.post(
        "/api/v1/chat/conversation/start",
        json={"customer_id": "test-customer-789"}
    )
    conversation_id = conv_response.json()["conversation_id"]
    
    # Send message
    client.post(
        "/api/v1/chat/message",
        json={
            "conversation_id": conversation_id,
            "customer_id": "test-customer-789",
            "message": "I have a question"
        }
    )
    
    # Get conversation
    response = client.get(f"/api/v1/chat/conversation/{conversation_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["conversation_id"] == conversation_id
    assert "messages" in data
    assert len(data["messages"]) >= 2  # Customer message + AI response


def test_create_escalation_ticket():
    # Start conversation
    conv_response = client.post(
        "/api/v1/chat/conversation/start",
        json={"customer_id": "test-customer-escalation"}
    )
    conversation_id = conv_response.json()["conversation_id"]
    
    # Create escalation
    response = client.post(
        "/api/v1/escalations/tickets",
        json={
            "conversation_id": conversation_id,
            "customer_id": "test-customer-escalation",
            "reason": "Complex billing issue",
            "priority": "high"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "ticket_id" in data
    assert data["priority"] == "high"
    assert data["status"] == "open"


def test_invalid_conversation():
    response = client.get("/api/v1/chat/conversation/invalid-id")
    assert response.status_code == 404


def test_missing_required_fields():
    response = client.post(
        "/api/v1/chat/conversation/start",
        json={}
    )
    assert response.status_code == 422  # Validation error
