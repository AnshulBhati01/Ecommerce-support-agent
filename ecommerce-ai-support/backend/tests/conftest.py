"""Test configuration and fixtures"""
import pytest
from app.config import Settings


@pytest.fixture
def settings():
    """Override settings for testing"""
    settings = Settings()
    settings.DEBUG = True
    settings.DATABASE_URL = "sqlite:///./test.db"
    return settings


@pytest.fixture
def sample_conversation_data():
    return {
        "customer_id": "test-customer",
        "status": "active"
    }


@pytest.fixture
def sample_order_data():
    return {
        "customer_id": "test-customer",
        "order_id": "ORD-12345",
        "status": "pending",
        "total_amount": 99.99,
        "items": [
            {
                "product_name": "Test Product",
                "quantity": 1,
                "unit_price": 99.99
            }
        ]
    }
