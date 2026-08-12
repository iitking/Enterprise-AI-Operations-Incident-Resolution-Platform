"""
OpsPilot AI - PII & Secret Redaction Engine
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

import re
from typing import Any

# Regular expressions for sensitive patterns
PATTERNS = [
    # JWT tokens
    (re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"), "[REDACTED_JWT]"),
    # API Keys & Bearer tokens
    (re.compile(r"(?i)(api[_-]?key|secret|token|password|passwd|auth)\s*[:=]\s*['\"]?([A-Za-z0-9_\-\.]{8,})['\"]?"), r"\1=[REDACTED_SECRET]"),
    (re.compile(r"(?i)bearer\s+[A-Za-z0-9_\-\.]{15,}"), "Bearer [REDACTED_TOKEN]"),
    # AWS Access Keys
    (re.compile(r"AKIA[0-9A-Z]{16}"), "[REDACTED_AWS_KEY]"),
    # Credit Card numbers
    (re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b"), "[REDACTED_CC]"),
    # IPv4 addresses (private IPs can be masked or labeled)
    (re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"), "[IP_MASKED]"),
    # Email addresses
    (re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"), "[REDACTED_EMAIL]"),
]

def redact_sensitive_data(text: str) -> str:
    """Sanitizes text by masking API keys, credentials, PII and secrets."""
    if not isinstance(text, str):
        return text

    sanitized = text
    for pattern, replacement in PATTERNS:
        sanitized = pattern.sub(replacement, sanitized)
    return sanitized

def redact_dict(data: Any) -> Any:
    """Recursively redacts dictionary or list structures."""
    if isinstance(data, dict):
        return {k: redact_dict(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [redact_dict(item) for item in data]
    elif isinstance(data, str):
        return redact_sensitive_data(data)
    return data
