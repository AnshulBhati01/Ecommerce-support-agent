from typing import List, Dict, Any
from app.config import Settings
from app.utils.logger import logger

settings = Settings()

# Mock FAQ database
FAQ_DATABASE = [
    {
        "question": "How do I track my order?",
        "answer": "You can track your order using the tracking number sent to your email. Visit our tracking page and enter the order ID.",
        "keywords": ["track", "order", "tracking", "status"]
    },
    {
        "question": "What is your return policy?",
        "answer": "We offer 30-day returns for all products in original condition. Contact our support team to initiate a return.",
        "keywords": ["return", "refund", "policy", "return policy"]
    },
    {
        "question": "How long does shipping take?",
        "answer": "Standard shipping takes 5-7 business days. Express shipping takes 2-3 business days.",
        "keywords": ["shipping", "delivery", "time", "how long"]
    },
    {
        "question": "Can I change my delivery address?",
        "answer": "You can change your address if the order hasn't shipped yet. Please contact us immediately with your new address.",
        "keywords": ["address", "change", "delivery", "shipping address"]
    },
    {
        "question": "Do you offer international shipping?",
        "answer": "We currently ship to 50+ countries. Check if your country is eligible on our shipping page.",
        "keywords": ["international", "shipping", "country", "overseas"]
    }
]

class RAGSystem:
    """Retrieval Augmented Generation system for customer support"""
    
    def __init__(self):
        self.settings = Settings()
        self.faq_db = FAQ_DATABASE
        logger.info("RAG System initialized")
    
    def retrieve_context(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant FAQ and documentation
        In production, this would query Pinecone vector DB
        """
        query_lower = query.lower()
        
        # Score FAQs based on keyword matching
        scores = []
        for idx, faq in enumerate(self.faq_db):
            score = sum(1 for keyword in faq["keywords"] if keyword in query_lower)
            if score > 0:
                scores.append((idx, score))
        
        # Sort by score and take top k
        scores.sort(key=lambda x: x[1], reverse=True)
        top_indices = [idx for idx, _ in scores[:k]]
        
        return [self.faq_db[idx] for idx in top_indices]
    
    def generate_response(self, query: str, intent: str, order_data: Dict = None) -> Dict[str, Any]:
        """
        Generate contextual response based on query and intent
        In production, this would use OpenAI GPT-4
        """
        try:
            context_docs = self.retrieve_context(query)
            context = "\n".join([f"Q: {doc['question']}\nA: {doc['answer']}" for doc in context_docs])
            
            # Template-based response generation (mock)
            response = self._generate_template_response(
                intent=intent,
                query=query,
                context=context,
                order_data=order_data
            )
            
            logger.info(f"Generated response for intent: {intent}")
            
            return {
                "response": response,
                "context_used": len(context_docs),
                "sources": [doc.get("question") for doc in context_docs]
            }
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                "response": "I apologize, but I'm having trouble processing your request. Please try again or contact our support team.",
                "context_used": 0,
                "sources": []
            }
    
    def _generate_template_response(self, intent: str, query: str, context: str, order_data: Dict = None) -> str:
        """Generate response using templates"""
        
        templates = {
            "order_status": lambda: f"Based on your order: {order_data.get('status', 'pending')}. Your tracking number is {order_data.get('tracking_number', 'N/A')}. Expected delivery: {order_data.get('expected_delivery', 'To be updated')}.",
            "return": lambda: "We'd be happy to help with a return. Our return policy allows 30 days for returns in original condition. Please provide your order number and reason for return.",
            "shipping": lambda: "Shipping information: Standard delivery takes 5-7 business days, Express takes 2-3 days. " + context,
            "payment": lambda: "For payment-related inquiries, please provide your order number. Our billing team will assist you.",
            "product_info": lambda: f"Product information: {context}. Is there anything specific you'd like to know?",
            "general_help": lambda: f"How can I assist you today? {context}",
            "escalation": lambda: "I understand your concern. Let me connect you with our specialized support team to resolve this quickly."
        }
        
        response_template = templates.get(intent, templates["general_help"])
        return response_template()
    
    def validate_response(self, response: str) -> bool:
        """Validate response quality"""
        return len(response) > 10 and len(response) < 2000
