"""
OpsPilot AI - RAG Knowledge Retriever
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

from typing import List, Dict, Any, Optional
from backend.rag.vector_store import vector_store

class KnowledgeRetriever:
    """
    RAG Retriever that equips multi-agent systems with organizational memory,
    retrieving past incident postmortems, runbooks, and remediation steps.
    """

    def __init__(self, store=vector_store):
        self.store = store

    def retrieve_incident_context(self, service: str, symptoms: str, top_k: int = 2) -> Dict[str, Any]:
        """
        Retrieves relevant runbooks and previous postmortems given service and symptoms.
        """
        query = f"service: {service} symptoms: {symptoms}"
        results = self.store.search(query=query, top_k=top_k)

        runbooks = [doc for doc in results if doc.get("category") == "runbook"]
        postmortems = [doc for doc in results if doc.get("category") == "postmortem"]

        formatted_context = ""
        for idx, doc in enumerate(results, 1):
            formatted_context += f"--- Document #{idx}: {doc['title']} (Score: {doc['score']}) ---\n"
            formatted_context += f"{doc['content']}\n\n"

        return {
            "query": query,
            "total_retrieved": len(results),
            "documents": results,
            "runbooks": runbooks,
            "postmortems": postmortems,
            "formatted_context": formatted_context.strip()
        }

retriever = KnowledgeRetriever()
