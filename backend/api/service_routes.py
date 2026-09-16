"""
OpsPilot AI - Microservices & Deployment Routes
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

from typing import List, Dict, Any
from backend.api.router_compat import APIRouter
from backend.tools.github_tool import get_deployment

router = APIRouter(prefix="/api/services", tags=["Services"])

SERVICES_MOCK = [
    {
        "id": "srv-01",
        "name": "payment-api",
        "namespace": "production",
        "description": "Core payment processing, checkout gateway and Stripe/Adyen integration",
        "current_version": "v2.4.1",
        "health_status": "degraded"
    },
    {
        "id": "srv-02",
        "name": "order-processor",
        "namespace": "production",
        "description": "Asynchronous order state machine and Kafka consumer pipeline",
        "current_version": "v1.8.0",
        "health_status": "healthy"
    },
    {
        "id": "srv-03",
        "name": "inventory-service",
        "namespace": "production",
        "description": "Real-time stock reservation and warehouse sync",
        "current_version": "v3.1.2",
        "health_status": "healthy"
    },
    {
        "id": "srv-04",
        "name": "catalog-api",
        "namespace": "production",
        "description": "Product catalog and Redis caching layer",
        "current_version": "v2.0.4",
        "health_status": "healthy"
    }
]

@router.get("")
def list_services():
    """List microservices registered with OpsPilot AI."""
    return SERVICES_MOCK

@router.get("/{service_name}/deployments")
def get_service_deployments(service_name: str):
    """Retrieve deployment history for a service."""
    return get_deployment(service=service_name)
