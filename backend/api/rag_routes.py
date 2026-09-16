"""
OpsPilot AI - RAG Knowledge Base Routes
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

from typing import List, Optional
from backend.api.router_compat import APIRouter
from backend.models.schemas import RAGQueryRequest, RAGDocumentResponse
from backend.rag.vector_store import vector_store

router = APIRouter(prefix="/api/rag", tags=["RAG Knowledge Base"])

@router.post("/search")
def search_knowledge_base(payload: RAGQueryRequest):
    """Semantic vector search across runbooks, architecture docs, and postmortems."""
    results = vector_store.search(
        query=payload.query,
        top_k=payload.top_k,
        category=payload.category
    )
    return {
        "query": payload.query,
        "results": results,
        "total": len(results)
    }

@router.get("/documents")
def list_knowledge_documents():
    """Lists indexed runbooks and postmortems."""
    docs = []
    for d in vector_store.documents:
        docs.append({
            "id": d["id"],
            "title": d["title"],
            "category": d["category"],
            "service": d.get("service"),
            "tags": d.get("tags", [])
        })
    return docs
