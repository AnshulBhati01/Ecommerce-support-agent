from typing import Tuple, Dict, List
from app.config import Settings
import json

settings = Settings()

# Mock intents for demonstration
INTENTS = {
    "order_status": ["where", "order", "tracking", "status", "when", "arrive", "deliver"],
    "return": ["return", "refund", "exchange", "wrong", "damaged", "defective"],
    "shipping": ["shipping", "delivery", "address", "reship", "cost"],
    "payment": ["payment", "charge", "billing", "credit card", "invoice"],
    "product_info": ["product", "specs", "features", "size", "color", "available"],
    "general_help": ["help", "support", "assist", "information", "question"],
    "escalation": ["complaint", "problem", "issue", "urgent", "angry", "frustrated"]
}

class IntentClassifier:
    """Classify customer intents using keyword matching and NLP"""
    
    def __init__(self):
        self.settings = Settings()
        self.intents_db = INTENTS
    
    def classify_intent(self, message: str) -> Tuple[str, float]:
        """
        Classify intent from customer message
        Returns: (intent, confidence_score)
        """
        message_lower = message.lower()
        intent_scores = {}
        
        # Score each intent based on keyword matches
        for intent, keywords in self.intents_db.items():
            matches = sum(1 for keyword in keywords if keyword in message_lower)
            score = matches / len(keywords) if keywords else 0
            intent_scores[intent] = score
        
        # Get intent with highest score
        best_intent = max(intent_scores, key=intent_scores.get)
        confidence = intent_scores[best_intent]
        
        # If confidence is very low, default to general_help
        if confidence < 0.1:
            best_intent = "general_help"
            confidence = 0.3
        
        return best_intent, confidence
    
    def extract_entities(self, message: str) -> Dict[str, str]:
        """Extract entities like order ID, product name, etc."""
        entities = {}
        
        # Extract order ID (ORD-XXXXX pattern)
        import re
        order_match = re.search(r'ORD-\d+', message, re.IGNORECASE)
        if order_match:
            entities["order_id"] = order_match.group()
        
        # Extract email
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', message)
        if email_match:
            entities["email"] = email_match.group()
        
        # Extract phone number
        phone_match = re.search(r'\b\d{10}\b|\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b', message)
        if phone_match:
            entities["phone"] = phone_match.group()
        
        return entities
    
    def get_intent_description(self, intent: str) -> str:
        """Get human-readable description of intent"""
        descriptions = {
            "order_status": "Customer inquiring about order status",
            "return": "Customer requesting return or refund",
            "shipping": "Customer asking about shipping",
            "payment": "Customer inquiring about payment",
            "product_info": "Customer asking for product information",
            "general_help": "General support request",
            "escalation": "Customer expressing frustration or complaints"
        }
        return descriptions.get(intent, "Unknown intent")
