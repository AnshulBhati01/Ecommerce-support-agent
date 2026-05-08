from locust import HttpUser, task, between
import random
import uuid


class ChatUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Initialize conversation on start"""
        self.customer_id = str(uuid.uuid4())
        self.conversation_id = None
        
        # Start a new conversation
        response = self.client.post(
            "/api/v1/chat/conversation/start",
            json={"customer_id": self.customer_id}
        )
        
        if response.status_code == 200:
            self.conversation_id = response.json().get("conversation_id")
    
    @task(3)
    def send_message(self):
        """Send chat messages"""
        if not self.conversation_id:
            return
        
        messages = [
            "Where is my order?",
            "I want to return my purchase",
            "How long does shipping take?",
            "Can I change my delivery address?",
            "What's your return policy?"
        ]
        
        self.client.post(
            "/api/v1/chat/message",
            json={
                "conversation_id": self.conversation_id,
                "customer_id": self.customer_id,
                "message": random.choice(messages)
            }
        )
    
    @task(1)
    def get_conversation(self):
        """Retrieve conversation history"""
        if self.conversation_id:
            self.client.get(f"/api/v1/chat/conversation/{self.conversation_id}")
    
    @task(1)
    def escalate(self):
        """Create escalation ticket"""
        if self.conversation_id:
            self.client.post(
                "/api/v1/escalations/tickets",
                json={
                    "conversation_id": self.conversation_id,
                    "customer_id": self.customer_id,
                    "reason": "Need human assistance",
                    "priority": "medium"
                }
            )
    
    @task(1)
    def health_check(self):
        """Check service health"""
        self.client.get("/health")


# Run with: locust -f tests/load/load_test.py --host=http://localhost:8000 -u 100 -r 10
