# E-Commerce AI Customer Support Agent

A production-ready AI-powered customer support system built with FastAPI, React, and LLMs.

## Features

- **AI Chat Interface**: Natural language conversations with intelligent routing
- **Intent Classification**: Automatic detection of customer intents
- **RAG System**: Context-aware responses using knowledge base
- **Order Lookup**: Integrated order management and tracking
- **Escalation System**: Smart routing to human agents when needed
- **Database**: PostgreSQL for persistent data storage
- **Caching**: Redis for performance optimization
- **Monitoring**: Prometheus metrics and health checks

## Architecture

```
Frontend (React) → Backend (FastAPI) → Database (PostgreSQL)
                        ↓
                  Services Layer
                  ├── Intent Classifier
                  ├── RAG Pipeline
                  ├── Order Manager
                  └── Escalation Manager
                        ↓
                  Cache Layer (Redis)
```

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+

### Local Development

```bash
# Clone repository
git clone <repo-url>
cd ecommerce-ai-support

# Start services
docker-compose up

# Backend will be available at http://localhost:8000
# Frontend will be available at http://localhost:3000
```

### Manual Setup

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

### Chat
- `POST /api/v1/chat/conversation/start` - Start conversation
- `POST /api/v1/chat/message` - Send message
- `GET /api/v1/chat/conversation/{id}` - Get history
- `POST /api/v1/chat/conversation/{id}/end` - End conversation

### Orders
- `GET /api/v1/orders/{order_id}` - Get order details
- `GET /api/v1/orders/customer/{customer_id}` - Get customer orders
- `POST /api/v1/orders/` - Create order
- `PUT /api/v1/orders/{order_id}/status` - Update status

### Escalations
- `POST /api/v1/escalations/tickets` - Create ticket
- `GET /api/v1/escalations/tickets/{id}` - Get ticket
- `PUT /api/v1/escalations/tickets/{id}/status` - Update status
- `GET /api/v1/escalations/pending` - Get pending tickets

### Health
- `GET /health` - Health check
- `GET /ready` - Readiness check
- `GET /live` - Liveness check

## Testing

```bash
# Unit tests
pytest backend/tests/unit -v

# Integration tests
pytest backend/tests/integration -v

# Load testing
locust -f backend/tests/load/load_test.py --host=http://localhost:8000
```

## Deployment

### Docker
```bash
docker-compose up --build
```

### Kubernetes
```bash
kubectl apply -f infrastructure/kubernetes/deployment.yaml
kubectl apply -f infrastructure/kubernetes/service.yaml
kubectl apply -f infrastructure/kubernetes/ingress.yaml
```

### Terraform
```bash
cd infrastructure/terraform/aws
terraform init
terraform plan
terraform apply
```

## Environment Variables

Create `.env` file from `.env.example`:
```bash
cp .env.example .env
```

Update with your API keys:
- `OPENAI_API_KEY` - OpenAI API key
- `PINECONE_API_KEY` - Pinecone vector DB key
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string

## Monitoring

- **Metrics**: Prometheus at `/metrics`
- **Logs**: Available in `logs/app.log`
- **Health**: Check `/health` endpoint

## Performance Targets

- Response time: <500ms (p95)
- Availability: 99.9% uptime
- First-contact resolution: 80%+
- Cost per interaction: ₹1-2

## License

MIT License

## Support

For issues, questions, or contributions, please open an issue on GitHub.
