# 🏗️ OpsPilot AI - Architecture Guide

**Author & Creator:** **Nivesh Kumar Meena**  
**Copyright © 2026 Nivesh Kumar Meena. All Rights Reserved.**

---

## High-Level System Architecture

OpsPilot AI is an enterprise-grade Autonomous Agentic Operations and Incident Resolution Platform. It bridges real-time telemetry alerts with stateful multi-agent intelligence, semantic RAG retrieval, and policy-governed automation.

```
                      ┌─────────────────────────────────────────┐
                      │        Alert Ingestion Layer            │
                      │  Prometheus / Datadog / Webhooks / n8n   │
                      └────────────────────┬────────────────────┘
                                           │
                                           ▼
                      ┌─────────────────────────────────────────┐
                      │          OpsPilot FastAPI Gateway       │
                      │     Auth (JWT) + RBAC + PII Redaction   │
                      └────────────────────┬────────────────────┘
                                           │
                                           ▼
                      ╔═════════════════════════════════════════╗
                      ║          LANGGRAPH ORCHESTRATOR         ║
                      ║                                         ║
                      ║           [ Supervisor Agent ]          ║
                      ║                    │                    ║
                      ║           [ Triage Agent ]              ║
                      ║                    │                    ║
                      ║     ┌──────────────┼──────────────┐     ║
                      ║     ▼              ▼              ▼     ║
                      ║  [ Logs ]     [ Metrics ]    [ GitHub ] ║
                      ║  [ Agent ]     [ Agent ]     [ Agent ]  ║
                      ║     │              │              │     ║
                      ║     └──────────────┼──────────────┘     ║
                      ║                    ▼                    ║
                      ║         [ Root Cause Agent ]            ║
                      ║                    │                    ║
                      ║        [ Risk & Policy Agent ]          ║
                      ╚════════════════════╤════════════════════╝
                                           │
                          ┌────────────────┴────────────────┐
                          ▼                                 ▼
                 [ LOW Risk Actions ]              [ HIGH Risk Actions ]
                          │                                 │
                 (Auto-Remediate)                 (Interrupt / Pause)
                          │                                 │
                          │                        [ Human SRE Approval ]
                          │                                 │
                          └────────────────┬────────────────┘
                                           ▼
                      ┌─────────────────────────────────────────┐
                      │          Remediation Execution          │
                      │     Kubernetes Rollout Undo / Restart   │
                      └────────────────────┬────────────────────┘
                                           │
                                           ▼
                      ┌─────────────────────────────────────────┐
                      │       Communication & Postmortem        │
                      │       Slack + Jira + Blameless Report   │
                      └─────────────────────────────────────────┘
```

---

## Multi-Agent Responsibilities

1. **Supervisor Agent**: Deconstructs incoming incidents, initializes investigation tracks, monitors convergence across parallel sub-agents.
2. **Incident Triage Agent**: Evaluates error rates and latency against production SLOs, classifies severity (P1 to P4), generates an investigation plan.
3. **Log Investigation Agent**: Searches centralized application logs, aggregates tracebacks, identifies error signatures (e.g., PostgreSQL connection timeout).
4. **Metrics Agent**: Queries Prometheus time-series metrics, flags latency p99 anomalies, inspects database connection pool saturation and node CPU.
5. **Code & Deployment Agent**: Correlates deployment timestamps with incident alert times, inspects Git commits and PR diffs for regressions.
6. **Root Cause Agent**: Synthesizes evidence across all agents and matches against historical incident postmortems using RAG to produce causal explanations with confidence scores (e.g. 94%).
7. **Risk & Policy Agent**: Classifies actions into LOW, MEDIUM, HIGH, and BLOCKED. Halts high-risk actions until verified by a human SRE.
8. **Communication Agent**: Generates Slack updates, files Jira tickets, and writes blameless postmortems with preventive action checklists.
