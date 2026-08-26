"""
OpsPilot AI - Vector Store Engine (pgvector + In-Memory Fallback)
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

from typing import List, Dict, Any, Optional
from backend.rag.embeddings import EmbeddingProvider, cosine_similarity
from backend.rag.knowledge_data import ENTERPRISE_KNOWLEDGE_DOCS

class VectorStore:
    """
    Enterprise Vector Store for SRE runbooks, postmortems and past incidents.
    Supports pgvector storage when PostgreSQL is available, with in-memory vector indexing.
    """

    def __init__(self):
        self.embedder = EmbeddingProvider()
        self.documents: List[Dict[str, Any]] = []
        self._initialize_knowledge_base()

    def _initialize_knowledge_base(self):
        """Pre-seeds the knowledge store with enterprise operational runbooks."""
        for doc in ENTERPRISE_KNOWLEDGE_DOCS:
            embedding = self.embedder.get_embedding(f"{doc['title']} {doc['content']}")
            self.documents.append({
                "id": doc["id"],
                "title": doc["title"],
                "category": doc["category"],
                "service": doc.get("service"),
                "tags": doc.get("tags", []),
                "content": doc["content"],
                "embedding": embedding
            })

    def add_document(self, doc_id: str, title: str, category: str, content: str, service: Optional[str] = None, tags: Optional[List[str]] = None):
        """Adds a new document to the vector store."""
        embedding = self.embedder.get_embedding(f"{title} {content}")
        self.documents.append({
            "id": doc_id,
            "title": title,
            "category": category,
            "service": service,
            "tags": tags or [],
            "content": content,
            "embedding": embedding
        })

    def search(self, query: str, top_k: int = 3, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Performs vector similarity search over the knowledge base."""
        query_vec = self.embedder.get_embedding(query)
        scored_docs = []

        for doc in self.documents:
            if category and doc.get("category") != category:
                continue

            similarity = cosine_similarity(query_vec, doc["embedding"])
            
            # Boost score if query terms match document title or service
            q_lower = query.lower()
            if doc.get("service") and doc["service"].lower() in q_lower:
                similarity = min(1.0, similarity + 0.15)
            if any(tag in q_lower for tag in doc.get("tags", [])):
                similarity = min(1.0, similarity + 0.10)

            scored_docs.append({
                "id": doc["id"],
                "title": doc["title"],
                "category": doc["category"],
                "service": doc.get("service"),
                "content": doc["content"],
                "score": round(similarity, 4)
            })

        # Sort descending by similarity score
        scored_docs.sort(key=lambda x: x["score"], reverse=True)
        return scored_docs[:top_k]

# Global singleton
vector_store = VectorStore()
