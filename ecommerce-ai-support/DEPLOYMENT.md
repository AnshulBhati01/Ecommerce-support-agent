# Deployment Guide

## Prerequisites

- Docker & Docker Compose
- Kubernetes cluster (optional)
- AWS account (for cloud deployment)
- GitHub repository with actions enabled

## Local Development

### 1. Environment Setup

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 2. Start Services

```bash
docker-compose up --build
```

Services will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Database: localhost:5432
- Redis: localhost:6379

### 3. Initialize Database

```bash
docker-compose exec backend python -c "from app.models.database import create_tables; create_tables()"
```

## Docker Deployment

### Build Images

```bash
docker-compose build
```

### Run in Production Mode

```bash
docker-compose -f docker-compose.yml up -d
```

## Kubernetes Deployment

### Prerequisites

```bash
kubectl cluster-info
# Create namespace
kubectl create namespace ecommerce-ai
```

### Deploy Services

```bash
# Create secrets
kubectl create secret generic db-credentials \
  --from-literal=connection-string=postgresql://user:pass@db:5432/ecommerce_ai

# Deploy
kubectl apply -f infrastructure/kubernetes/deployment.yaml
kubectl apply -f infrastructure/kubernetes/service.yaml
kubectl apply -f infrastructure/kubernetes/ingress.yaml

# Verify
kubectl get deployments
kubectl get pods
kubectl get services
```

### Monitor Deployment

```bash
# Watch rollout status
kubectl rollout status deployment/ai-support-backend

# Check logs
kubectl logs -f deployment/ai-support-backend

# Port forward for local testing
kubectl port-forward svc/ai-support-backend 8000:80
```

## AWS Deployment

### Prerequisites

```bash
terraform init
aws configure
```

### Deploy Infrastructure

```bash
cd infrastructure/terraform/aws

terraform plan -var="environment=production"
terraform apply -var="environment=production"
```

## Continuous Deployment

### GitHub Actions

Push to `main` branch triggers:
1. Tests
2. Linting
3. Build Docker images
4. Push to registry
5. Deploy to Kubernetes

### Manual Deployment

```bash
bash infrastructure/scripts/deploy.sh production us-east-1
```

## Health Checks

### Service Health

```bash
# Health check
curl http://localhost:8000/health

# Readiness check
curl http://localhost:8000/ready

# Liveness check
curl http://localhost:8000/live
```

### Database Health

```bash
docker-compose exec postgres pg_isready -U ecommerce_user
```

### Redis Health

```bash
docker-compose exec redis redis-cli ping
```

## Scaling

### Kubernetes Auto-scaling

```bash
kubectl apply -f infrastructure/kubernetes/service.yaml
# HPA configured for 70% CPU utilization
```

### Manual Scaling

```bash
kubectl scale deployment ai-support-backend --replicas=5
```

## Backup & Recovery

### Database Backup

```bash
docker-compose exec postgres pg_dump -U ecommerce_user ecommerce_ai > backup.sql
```

### Database Restore

```bash
docker-compose exec postgres psql -U ecommerce_user ecommerce_ai < backup.sql
```

## Troubleshooting

### Connection Issues

```bash
# Check logs
docker-compose logs backend
docker-compose logs postgres

# Verify networking
docker-compose exec backend ping postgres
```

### Performance Issues

```bash
# Check resource usage
docker stats

# Monitor K8s resources
kubectl top nodes
kubectl top pods
```

### Database Issues

```bash
# Connect to database
docker-compose exec postgres psql -U ecommerce_user -d ecommerce_ai

# Check migrations
docker-compose exec backend alembic current
```

## Security Considerations

1. **Secrets Management**
   - Use AWS Secrets Manager
   - Never commit `.env` files
   - Rotate API keys regularly

2. **Network Security**
   - Enable HTTPS/TLS
   - Use security groups
   - Restrict database access

3. **Application Security**
   - Enable rate limiting
   - Implement CORS properly
   - Validate all inputs
   - Use prepared statements

4. **Compliance**
   - Encrypt data in transit
   - Encrypt data at rest
   - Implement audit logging
   - GDPR/CCPA compliance

## Monitoring & Alerts

### Prometheus Metrics

```bash
curl http://localhost:8000/metrics
```

### Grafana Dashboards

Access at http://localhost:3000

### CloudWatch (AWS)

Monitor via AWS Console

## Cost Optimization

- Use reserved instances for stable workloads
- Auto-scale based on metrics
- Use spot instances for non-critical workloads
- Optimize database queries
- Cache aggressively

## Support

For deployment issues:
1. Check logs
2. Verify configuration
3. Test connectivity
4. Review monitoring dashboards
5. Contact DevOps team
