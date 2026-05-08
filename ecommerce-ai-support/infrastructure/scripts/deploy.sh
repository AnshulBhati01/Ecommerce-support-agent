#!/bin/bash
# Deployment script for staging and production

set -e

ENVIRONMENT=${1:-staging}
REGION=${2:-us-east-1}

echo "🚀 Deploying E-Commerce AI Support to $ENVIRONMENT in $REGION"

# Build images
echo "📦 Building Docker images..."
docker-compose build --no-cache

# Run database migrations
echo "🗄️ Running database migrations..."
docker-compose run --rm backend alembic upgrade head

# Deploy to Kubernetes
if [ "$ENVIRONMENT" = "production" ]; then
    echo "🔒 Deploying to production..."
    kubectl apply -f infrastructure/kubernetes/deployment.yaml
    kubectl apply -f infrastructure/kubernetes/service.yaml
    kubectl apply -f infrastructure/kubernetes/ingress.yaml
    kubectl rollout status deployment/ai-support-backend
else
    echo "🧪 Deploying to staging..."
    docker-compose up -d
fi

echo "✅ Deployment complete!"
echo "📊 Monitor at: https://monitoring.yourdomain.com"
