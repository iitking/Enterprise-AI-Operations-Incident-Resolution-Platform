"""
OpsPilot AI - Global Configuration
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

import os
from typing import Optional

try:
    from pydantic_settings import BaseSettings
    class BaseConfig(BaseSettings):
        class Config:
            env_file = ".env"
            extra = "ignore"
except ImportError:
    class BaseConfig:
        pass

class Settings(BaseConfig):
    APP_NAME: str = "OpsPilot AI"
    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    PROJECT_AUTHOR: str = "Nivesh Kumar Meena"

    # Security
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "opspilot_super_secret_jwt_key_nivesh_kumar_meena_2026")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    DEFAULT_ADMIN_EMAIL: str = "admin@opspilot.ai"
    DEFAULT_ADMIN_PASSWORD: str = "admin_secret_pass"

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./opspilot.db")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # LLM / OpenAI
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    LLM_TEMPERATURE: float = 0.1

    # LangSmith Observability
    LANGCHAIN_TRACING_V2: bool = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    LANGCHAIN_ENDPOINT: str = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
    LANGCHAIN_API_KEY: Optional[str] = os.getenv("LANGCHAIN_API_KEY", "")
    LANGCHAIN_PROJECT: str = os.getenv("LANGCHAIN_PROJECT", "opspilot-ai-production")

    # n8n Automation
    N8N_BASE_URL: str = os.getenv("N8N_BASE_URL", "http://localhost:5678")
    N8N_WEBHOOK_INCIDENT_TRIGGER: str = os.getenv("N8N_WEBHOOK_INCIDENT_TRIGGER", "http://localhost:5678/webhook/incident-trigger")
    N8N_WEBHOOK_APPROVAL: str = os.getenv("N8N_WEBHOOK_APPROVAL", "http://localhost:5678/webhook/approval-decision")
    N8N_WEBHOOK_REMEDIATION: str = os.getenv("N8N_WEBHOOK_REMEDIATION", "http://localhost:5678/webhook/execute-remediation")

    # Integrations
    SLACK_WEBHOOK_URL: Optional[str] = os.getenv("SLACK_WEBHOOK_URL", "")
    SLACK_CHANNEL: str = "#incidents-prod"
    JIRA_BASE_URL: Optional[str] = os.getenv("JIRA_BASE_URL", "")
    JIRA_PROJECT_KEY: str = "OPS"

    # Infrastructure
    KUBERNETES_NAMESPACE: str = "production"

settings = Settings()
