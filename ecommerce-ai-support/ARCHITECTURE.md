# Project Structure Documentation

## Backend Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration management
│   ├── api/                 # API route handlers
│   │   ├── chat.py          # Chat endpoints
│   │   ├── orders.py        # Order endpoints
│   │   ├── escalations.py   # Escalation endpoints
│   │   └── health.py        # Health check endpoints
│   ├── services/            # Business logic
│   │   ├── intent_classifier.py   # Intent classification
│   │   ├── rag_pipeline.py        # RAG implementation
│   │   ├── order_manager.py       # Order operations
│   │   └── escalation_manager.py  # Escalation logic
│   ├── models/              # Database models
│   │   ├── database.py      # SQLAlchemy setup & models
│   │   └── schemas.py       # Pydantic schemas
│   └── utils/               # Utilities
│       ├── logger.py        # Logging setup
│       ├── cache.py         # Redis caching
│       └── validators.py    # Input validation
├── tests/
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   └── load/                # Load tests
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container image
└── pytest.ini              # Test configuration
```

## Frontend Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── ChatWindow.jsx   # Main chat interface
│   │   ├── MessageBubble.jsx # Message display
│   │   ├── OrderContext.jsx  # Order lookup
│   │   └── EscalationPrompt.jsx # Escalation dialog
│   ├── pages/               # Page components
│   │   └── ChatPage.jsx     # Main page
│   ├── services/            # API services
│   │   └── api.js          # API client
│   ├── App.jsx             # Root component
│   ├── main.jsx            # Entry point
│   └── index.jsx           # DOM mount
├── package.json            # Dependencies
├── vite.config.js          # Build config
├── nginx.conf              # Nginx config
└── Dockerfile              # Container image
```

## Infrastructure

```
infrastructure/
├── kubernetes/
│   ├── deployment.yaml     # K8s deployment
│   ├── service.yaml        # K8s service & HPA
│   └── ingress.yaml        # K8s ingress
├── terraform/
│   └── aws/
│       ├── main.tf         # AWS resources
│       ├── variables.tf    # Variables
│       └── outputs.tf      # Outputs
└── scripts/
    └── deploy.sh           # Deployment script
```

## Key Design Patterns

### 1. Service Layer Pattern
- `IntentClassifier` - NLP-based intent detection
- `RAGSystem` - Retrieval augmented generation
- `OrderManager` - Order CRUD operations
- `EscalationManager` - Escalation workflow

### 2. API Design
- RESTful endpoints with standard HTTP methods
- JSON request/response bodies
- Pydantic schema validation
- Consistent error handling

### 3. Database Design
- Normalized PostgreSQL schema
- SQLAlchemy ORM for type safety
- Indexed queries for performance
- Foreign key relationships

### 4. Caching Strategy
- Redis for conversation history
- TTL-based expiration
- Cache invalidation on updates

### 5. Testing Strategy
- Unit tests for services
- Integration tests for APIs
- Load tests with Locust
- >80% code coverage target

## Deployment Pipeline

```
Code Push → Tests → Build Images → Push Registry → Deploy to K8s
```

## Configuration Management

- Environment variables via `.env`
- `Settings` class for type-safe config
- Secret management via K8s secrets
- Region-specific Terraform variables
