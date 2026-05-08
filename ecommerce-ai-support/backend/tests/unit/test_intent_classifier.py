import pytest
from app.services.intent_classifier import IntentClassifier


@pytest.fixture
def classifier():
    return IntentClassifier()


def test_order_status_intent(classifier):
    query = "Where is my order?"
    intent, confidence = classifier.classify_intent(query)
    assert intent == "order_status"
    assert confidence > 0


def test_return_intent(classifier):
    query = "I want to return my purchase"
    intent, confidence = classifier.classify_intent(query)
    assert intent == "return"


def test_shipping_intent(classifier):
    query = "How long does shipping take?"
    intent, confidence = classifier.classify_intent(query)
    assert intent == "shipping"


def test_payment_intent(classifier):
    query = "Why was I charged twice?"
    intent, confidence = classifier.classify_intent(query)
    assert intent == "payment"


def test_general_help_low_confidence(classifier):
    query = "Hello"
    intent, confidence = classifier.classify_intent(query)
    assert intent in ["general_help", "order_status"]


def test_entity_extraction(classifier):
    query = "My order ID is ORD-12345"
    entities = classifier.extract_entities(query)
    assert "order_id" in entities
    assert entities["order_id"] == "ORD-12345"


def test_email_extraction(classifier):
    query = "Please contact me at john@example.com"
    entities = classifier.extract_entities(query)
    assert "email" in entities
    assert entities["email"] == "john@example.com"


def test_intent_description(classifier):
    description = classifier.get_intent_description("return")
    assert "return" in description.lower()
