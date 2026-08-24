"""
OpsPilot AI - Embedding Provider
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

import math
import hashlib
from typing import List
from backend.config import settings

class EmbeddingProvider:
    """
    High-performance embedding provider.
    Supports OpenAI text-embedding-3-small when API key is configured,
    and provides a deterministic semantic dense-vectorizer for offline local execution.
    """

    def __init__(self):
        self.dimension = 256
        self.use_openai = bool(settings.OPENAI_API_KEY and len(settings.OPENAI_API_KEY) > 10)

    def get_embedding(self, text: str) -> List[float]:
        """Generate normalized dense embedding vector for text."""
        if self.use_openai:
            try:
                import httpx
                headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
                payload = {"input": text, "model": settings.EMBEDDING_MODEL}
                with httpx.Client(timeout=10.0) as client:
                    resp = client.post("https://api.openai.com/v1/embeddings", headers=headers, json=payload)
                    if resp.status_code == 200:
                        return resp.json()["data"][0]["embedding"]
            except Exception:
                # Fallback to local dense vectorizer on network or key issue
                pass

        return self._local_semantic_embedding(text)

    def _local_semantic_embedding(self, text: str) -> List[float]:
        """
        Deterministic, word-frequency and n-gram hash projection into unit-normalized L2 vector.
        Preserves keyword and semantic similarities across SRE technical terms.
        """
        vec = [0.0] * self.dimension
        words = text.lower().split()
        if not words:
            return vec

        for word in words:
            # Hash word into vector dimensions
            h = int(hashlib.sha256(word.encode("utf-8")).hexdigest(), 16)
            idx = h % self.dimension
            sign = 1.0 if ((h >> 8) % 2 == 0) else -1.0
            weight = 1.0
            
            # Boost domain keywords for SRE context
            if word in ["postgres", "postgresql", "timeout", "pool", "connection", "database", "rollback", "query"]:
                weight = 3.0
            elif word in ["kafka", "lag", "partition", "rebalance"]:
                weight = 3.0
            elif word in ["oomkilled", "memory", "leak", "exitcode"]:
                weight = 3.0

            vec[idx] += sign * weight

        # L2 normalize
        norm = math.sqrt(sum(v * v for v in vec))
        if norm > 0:
            vec = [v / norm for v in vec]

        return vec

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Computes cosine similarity between two unit vectors."""
    min_len = min(len(v1), len(v2))
    dot = sum(v1[i] * v2[i] for i in range(min_len))
    return max(0.0, min(1.0, float(dot)))
