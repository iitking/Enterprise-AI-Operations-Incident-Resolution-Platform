"""
OpsPilot AI - RAG Knowledge Base Tests
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

import unittest
from backend.rag.vector_store import vector_store
from backend.rag.retriever import retriever
from backend.rag.embeddings import EmbeddingProvider, cosine_similarity

class TestRAGLayer(unittest.TestCase):

    def test_embedding_normalization(self):
        provider = EmbeddingProvider()
        vec = provider.get_embedding("database connection timeout error in postgresql pool")
        self.assertEqual(len(vec), 256)
        # Verify L2 norm is 1.0 (or close to 1)
        norm = sum(v * v for v in vec)
        self.assertAlmostEqual(norm, 1.0, places=2)

    def test_vector_search_finds_database_runbook(self):
        query = "payment-api postgresql connection pool timeout"
        results = vector_store.search(query=query, top_k=2)
        self.assertGreater(len(results), 0)
        top_match = results[0]
        self.assertIn("Payment API", top_match["title"])
        self.assertGreater(top_match["score"], 0.5)

    def test_retriever_context_assembly(self):
        context = retriever.retrieve_incident_context(
            service="payment-api",
            symptoms="PostgreSQL connection timeout latency 4200ms",
            top_k=2
        )
        self.assertGreater(context["total_retrieved"], 0)
        self.assertIn("runbook", [d["category"] for d in context["documents"]])

if __name__ == "__main__":
    unittest.main()
