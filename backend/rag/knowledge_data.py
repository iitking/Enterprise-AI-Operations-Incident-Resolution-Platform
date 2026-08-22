"""
OpsPilot AI - Enterprise Knowledge Base Data (Runbooks & Postmortems)
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

from typing import List, Dict, Any

ENTERPRISE_KNOWLEDGE_DOCS: List[Dict[str, Any]] = [
    {
        "id": "runbook-db-pool-01",
        "title": "Payment API Database Connection Pool Troubleshooting Runbook",
        "category": "runbook",
        "service": "payment-api",
        "tags": ["postgresql", "connection_pool", "timeout", "payment-api", "latency"],
        "content": (
            "Title: Payment API Database Connection Pool Troubleshooting\n"
            "Symptoms: High API latency (>4000ms), 500 error rate spikes > 15%, 'PostgreSQL connection timeout' in logs, "
            "database CPU > 85%, connection pool active count reaching maximum (e.g., 20/20 active connections).\n"
            "Probable Causes:\n"
            "1. Newly deployed release introducing long-running or unindexed SQL query that holds connections open.\n"
            "2. Traffic surge exceeding max_connections without connection pooling proxy (PgBouncer).\n"
            "3. Database transaction leak or uncommitted transactions holding connection locks.\n"
            "Remediation Procedure:\n"
            "Step 1: Check recent deployments within the last 30 minutes. If a new version was deployed, inspect git commits.\n"
            "Step 2: If git diff shows new SQL queries without index or slow join, recommend immediate rollback to previous stable version.\n"
            "Step 3: Rollback Risk is HIGH (requires human approval). Present confidence score and commit details.\n"
            "Step 4: Execute rollback via Kubernetes: kubectl rollout undo deployment/payment-api.\n"
            "Step 5: Post-remediation verification: Check error rate drops below 1% and latency drops below 200ms."
        )
    },
    {
        "id": "postmortem-inc-097",
        "title": "Postmortem INC-097: Payment API Database Pool Exhaustion",
        "category": "postmortem",
        "service": "payment-api",
        "tags": ["payment-api", "postmortem", "rollback", "v2.4.1", "postgres"],
        "content": (
            "Incident ID: INC-097 | Service: payment-api | Severity: P1\n"
            "Date: 2026-03-15 | Duration: 6 minutes | Impact: 18.4% failed payment transactions.\n"
            "Root Cause: Deployment of payment-api v2.4.1 contained commit 'Optimize payment query' which accidentally "
            "removed an index condition on the transactions table. The unindexed query scan increased query latency from 8ms to 3200ms, "
            "causing all 20 worker threads to exhaust the HikariCP / SQLAlchemy database connection pool. Subsequent requests timed out.\n"
            "Resolution: OpsPilot AI identified the correlation between deployment v2.4.1 and database timeout logs. "
            "An SRE approved the automated rollback to v2.4.0. Service error rate returned to 0.4% within 60 seconds.\n"
            "Action Items: 1. Add query performance regression test in CI/CD. 2. Implement PgBouncer. 3. Add canary deployment."
        )
    },
    {
        "id": "runbook-kafka-lag-02",
        "title": "Kafka Consumer Lag & Partition Rebalance Storm Runbook",
        "category": "runbook",
        "service": "order-processor",
        "tags": ["kafka", "consumer_lag", "rebalance", "order-processor"],
        "content": (
            "Title: Kafka Consumer Lag & Rebalance Runbook\n"
            "Symptoms: High consumer lag (>50,000 messages), order processing delay > 10m, heartbeats timing out.\n"
            "Probable Causes:\n"
            "1. Consumer processing time exceeding max.poll.interval.ms leading to coordinator kicking consumer out.\n"
            "2. Unhandled payload exception causing infinite retry loops.\n"
            "Remediation:\n"
            "Step 1: Check consumer pod CPU and memory.\n"
            "Step 2: Scale consumer pod replicas up to match topic partition count.\n"
            "Step 3: Restart stuck consumer pods if locked in rebalance loop.\n"
            "Risk: MEDIUM. Can be auto-executed or approved by SRE."
        )
    },
    {
        "id": "runbook-oom-kill-03",
        "title": "Kubernetes OOMKilled & Memory Leak Incident Runbook",
        "category": "runbook",
        "service": "inventory-service",
        "tags": ["kubernetes", "oomkilled", "exitcode_137", "memory_leak"],
        "content": (
            "Title: Kubernetes OOMKilled Diagnostic & Mitigation\n"
            "Symptoms: Container restarts with ExitCode 137 (OOMKilled), pod memory metric climbing steadily linearly.\n"
            "Remediation:\n"
            "Step 1: Inspect memory limits in k8s deployment manifest.\n"
            "Step 2: Temporarily increase memory limit by 50% via k8s patch to prevent flapping.\n"
            "Step 3: If introduced by recent deployment, trigger rollback to previous stable release.\n"
            "Step 4: Capture heap dump for development team."
        )
    },
    {
        "id": "runbook-redis-stampede-04",
        "title": "Redis Cache Stampede & Latency Spike Runbook",
        "category": "runbook",
        "service": "catalog-api",
        "tags": ["redis", "cache_stampede", "thundering_herd", "catalog-api"],
        "content": (
            "Title: Redis Cache Stampede & Cache Eviction Runbook\n"
            "Symptoms: Sudden spike in backend database read traffic, Redis memory usage 100%, cache hit ratio drops from 98% to 15%.\n"
            "Remediation:\n"
            "Step 1: Verify Redis memory maxmemory-policy (allkeys-lru vs noeviction).\n"
            "Step 2: Scale Redis cluster or increase maxmemory limit.\n"
            "Step 3: Enable probabilistic early expiration or mutex locks in application client."
        )
    }
]
