# 🚀 OpsPilot AI

## Enterprise AI Operations & Incident Resolution Platform

> **An autonomous multi-agent AI platform for enterprise incident investigation, root-cause analysis, workflow automation, and human-approved remediation.**

OpsPilot AI is a production-oriented Agentic AI platform designed to investigate software and infrastructure incidents, identify probable root causes, recommend or execute remediation, and automate communication and incident-management workflows.

The project combines **LangGraph, LangSmith, RAG, MCP/tool calling, n8n, FastAPI, PostgreSQL/pgvector, Kubernetes, observability, security, and Human-in-the-Loop (HITL)** into one end-to-end system.

---

# 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [Key Features](#-key-features)
- [Why This Project](#-why-this-project)
- [Architecture](#-architecture)
- [Agent Architecture](#-agent-architecture)
- [LangGraph](#-langgraph)
- [LangSmith](#-langsmith)
- [n8n Automation](#-n8n-automation)
- [RAG Architecture](#-rag-architecture)
- [MCP and Tools](#-mcp-and-tools)
- [Human-in-the-Loop](#-human-in-the-loop)
- [Security](#-security)
- [Dashboard](#-dashboard)
- [Technology Stack](#-technology-stack)
- [Database Design](#-database-design)
- [Repository Structure](#-repository-structure)
- [Incident Lifecycle](#-incident-lifecycle)
- [Example Scenario](#-example-scenario)
- [Development Roadmap](#-development-roadmap)
- [Evaluation Strategy](#-evaluation-strategy)
- [Production Deployment](#-production-deployment)
- [Future Enhancements](#-future-enhancements)
- [Resume Description](#-resume-description)
- [Interview Talking Points](#-interview-talking-points)
- [Project Goals](#-project-goals)
- [License](#-license)

---

# 🧠 Project Overview

Modern companies operate complex systems containing:

- AWS / GCP / Azure
- Kubernetes
- Microservices
- PostgreSQL
- Redis
- Kafka
- GitHub
- Jira
- Slack
- Prometheus
- Grafana
- Datadog
- CI/CD pipelines

When something fails in production, engineers often have to manually:

1. Receive an alert.
2. Check monitoring dashboards.
3. Search logs.
4. Investigate metrics.
5. Check recent deployments.
6. Inspect GitHub commits.
7. Search previous incidents.
8. Identify the root cause.
9. Decide the remediation.
10. Create Jira tickets.
11. Inform the team on Slack.
12. Execute or approve a fix.
13. Write a postmortem.

This process can take significant time, especially during high-severity incidents.

OpsPilot AI attempts to automate this workflow using a **stateful multi-agent AI system**.

---

# ❗ Problem Statement

Traditional incident management looks like:

```text
Alert
  ↓
DevOps Engineer
  ↓
Check Grafana
  ↓
Check Logs
  ↓
Check Database
  ↓
Check GitHub
  ↓
Check Deployment
  ↓
Find Root Cause
  ↓
Create Jira Ticket
  ↓
Inform Team
  ↓
Rollback / Restart
  ↓
Write Postmortem
```

OpsPilot AI transforms this into:

```text
Alert
  ↓
OpsPilot AI
  ↓
Incident Triage
  ↓
Parallel Investigation
  ├── Logs
  ├── Metrics
  ├── GitHub
  ├── Deployments
  └── Historical Incidents
  ↓
Root Cause Analysis
  ↓
Risk & Policy Evaluation
  ↓
┌──────────────────────┐
│                      │
│ Low Risk             │ High Risk
│                      │
▼                      ▼
Auto Remediation       Human Approval
│                      │
└──────────┬───────────┘
           ↓
          n8n
           ↓
   Slack / Jira / GitHub
           ↓
      Verification
           ↓
       Postmortem
           ↓
    LangSmith Evaluation
```

---

# 💡 Solution

OpsPilot AI is an **AI Operations Command Center**.

It uses specialized agents to investigate an incident from multiple sources.

The system can:

- Detect incidents.
- Classify severity.
- Investigate logs.
- Analyze infrastructure metrics.
- Inspect recent deployments.
- Analyze GitHub changes.
- Search previous incidents.
- Perform RAG over company runbooks and postmortems.
- Identify probable root causes.
- Estimate confidence.
- Assess remediation risk.
- Request human approval for sensitive actions.
- Execute low-risk remediation.
- Create Jira tickets.
- Send Slack notifications.
- Generate incident reports.
- Generate postmortems.
- Record traces in LangSmith.
- Evaluate agent performance.

---

# ⭐ Key Features

## 🤖 Multi-Agent AI

Specialized agents:

- Supervisor Agent
- Incident Triage Agent
- Log Investigation Agent
- Metrics Agent
- Code & Deployment Agent
- Root Cause Agent
- Risk & Policy Agent
- Communication Agent

---

## 🧠 LangGraph

LangGraph is responsible for:

- Agent orchestration
- Stateful workflows
- Conditional routing
- Parallel investigation
- Retries
- Checkpoints
- Interrupts
- Human approval
- Persistent state
- Multi-agent coordination

---

## 🔍 LangSmith

LangSmith is used for:

- Agent tracing
- LLM observability
- Tool-call inspection
- Prompt debugging
- Evaluation datasets
- Agent evaluation
- Latency tracking
- Token usage
- Cost monitoring
- Failure analysis
- Feedback collection

---

## 🔄 n8n

n8n is used as the automation layer for:

- Alert ingestion
- Slack notifications
- Jira ticket creation
- Email
- Human approval workflows
- GitHub actions
- Remediation workflows
- Scheduled workflows
- External integrations

---

## 📚 RAG

The platform can retrieve information from:

- Runbooks
- Architecture documentation
- Incident reports
- Previous postmortems
- Troubleshooting guides
- Internal documentation

Technology:

```text
Embeddings
    ↓
PostgreSQL
    +
pgvector
```

---

## 🧩 MCP / Tools

Agents can interact with external systems through tools or MCP-compatible integrations.

Examples:

```text
search_logs()
get_metrics()
get_deployment()
search_github()
create_jira()
send_slack()
query_database()
restart_service()
rollback_deployment()
```

---

## 👨‍💻 Human-in-the-Loop

Sensitive actions require approval.

Example:

```text
AI Recommendation

Rollback payment-api
v2.4.1 → v2.4.0

Risk: HIGH
Confidence: 94%

Reason:
Recent deployment correlates strongly
with increased database timeouts.

[ APPROVE ] [ REJECT ]
```

The system should never blindly execute high-risk production actions.

---

# 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │       USERS          │
                         │  Slack / Web / API   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Next.js Frontend  │
                         │      Dashboard       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     FastAPI Gateway  │
                         │ Auth + Rate Limiting │
                         └──────────┬───────────┘
                                    │
                                    ▼
                ╔════════════════════════════════════╗
                ║             LANGGRAPH             ║
                ║        Agent Orchestrator         ║
                ║                                    ║
                ║     ┌────────────────────────┐     ║
                ║     │ Supervisor / Router    │     ║
                ║     └────────────┬───────────┘     ║
                ║                  │                 ║
                ║       ┌──────────┼──────────┐      ║
                ║       ▼          ▼          ▼      ║
                ║     Logs       Metrics     Code     ║
                ║     Agent       Agent      Agent    ║
                ║       │          │          │      ║
                ║       └──────────┼──────────┘      ║
                ║                  ▼                 ║
                ║           Root Cause Agent        ║
                ║                  │                 ║
                ║                  ▼                 ║
                ║          Risk / Policy Agent      ║
                ╚══════════════════╤═════════════════╝
                                   │
                         ┌─────────┴─────────┐
                         ▼                   ▼
                  Auto Remediation      Human Approval
                         │                   │
                         └─────────┬─────────┘
                                   ▼
                                  n8n
                                   │
                   ┌───────────────┼────────────────┐
                   ▼               ▼                ▼
                 Slack            Jira            GitHub
                   │               │                │
                   └───────────────┼────────────────┘
                                   ▼
                           Infrastructure
                     ┌────────┬────┬────────┐
                     │        │    │        │
                    AWS      K8s  Kafka     DB


        ┌────────────────────────────────────────┐
        │               RAG LAYER                │
        │ PostgreSQL + pgvector + Embeddings     │
        └────────────────────┬───────────────────┘
                             │
                             ▼
                        Knowledge Base


        ┌────────────────────────────────────────┐
        │              LANGSMITH                 │
        │ Tracing + Evaluation + Monitoring      │
        └────────────────────────────────────────┘
```

---

# 🤖 Agent Architecture

## 1. Supervisor Agent

The Supervisor Agent controls the investigation.

Responsibilities:

- Understand incident context.
- Decide which agents are required.
- Route tasks.
- Coordinate parallel investigation.
- Track agent results.
- Decide when enough evidence is available.

Example:

```text
Incident received
       ↓
Supervisor
       ↓
Need logs?        YES
Need metrics?     YES
Need GitHub?      YES
Need database?    MAYBE
       ↓
Parallel investigation
```

---

# 2. Incident Triage Agent

Input:

```json
{
  "service": "payment-api",
  "error_rate": 18.5,
  "latency_ms": 4200,
  "environment": "production"
}
```

Output:

```json
{
  "incident_type": "production_failure",
  "severity": "P1",
  "investigation_plan": [
    "check_logs",
    "check_metrics",
    "check_recent_deployment"
  ]
}
```

Responsibilities:

- Severity classification.
- Incident categorization.
- Investigation planning.
- Initial risk assessment.

---

# 3. Log Investigation Agent

Responsibilities:

- Search logs.
- Filter errors.
- Detect repeated exceptions.
- Correlate timestamps.
- Identify error patterns.
- Summarize relevant logs.

Example:

```text
1,000 errors detected

73% originate from:
PostgreSQL connection timeout

Potential issue:
Database connection pool exhaustion
```

---

# 4. Metrics Agent

Analyzes:

```text
CPU
Memory
Latency
Request Rate
Error Rate
Database Connections
Kafka Lag
Network Traffic
```

It can identify:

- Anomalies.
- Sudden spikes.
- Resource exhaustion.
- Performance degradation.
- Correlation between metrics.

---

# 5. Code & Deployment Agent

Connects to:

```text
GitHub
Git Commits
Pull Requests
Deployment History
Docker
Kubernetes
```

Example:

```text
Incident started:
14:32

Latest deployment:
14:27

Commit:
"Optimize payment query"

Potential correlation:
HIGH
```

The agent compares:

```text
Incident timeline
+
Deployment timeline
+
Code changes
```

---

# 6. Root Cause Agent

Combines evidence from:

```text
Logs
+
Metrics
+
GitHub
+
Deployment History
+
Historical Incidents
+
RAG Knowledge
```

Example output:

```text
ROOT CAUSE

Payment service deployed version v2.4.1.

The new database query increased execution
time significantly.

This exhausted the database connection pool,
causing API timeouts.

Confidence: 94%
```

---

# 7. Risk & Policy Agent

The Risk Agent decides whether an action can be executed automatically.

Example:

```text
Action                    Risk

Read logs                 LOW
Read metrics              LOW
Create Jira               LOW
Send Slack message        LOW
Restart service            MEDIUM
Rollback production       HIGH
Delete database            BLOCKED
```

Policy:

```text
LOW
 ↓
Auto Execute

MEDIUM
 ↓
Configurable Approval

HIGH
 ↓
Human Approval Required

BLOCKED
 ↓
Never Execute
```

---

# 8. Communication Agent

Generates:

- Slack updates.
- Jira tickets.
- Incident summaries.
- Management reports.
- Customer communication drafts.
- Postmortems.

Example:

```text
P1 Incident Update

Service:
payment-api

Impact:
18.4% requests failing

Root Cause:
Database connection pool exhaustion

Current Action:
Rollback pending approval

Confidence:
94%
```

---

# 🔗 LangGraph

LangGraph is the central orchestration engine.

Basic workflow:

```text
START
  ↓
Supervisor
  ↓
Triage
  ↓
Investigation
  ↓
┌──────────────┬──────────────┬──────────────┐
▼              ▼              ▼
Logs         Metrics        GitHub
│              │              │
└──────────────┼──────────────┘
               ▼
         Root Cause
               ↓
         Risk Analysis
               ↓
       ┌───────┴────────┐
       ▼                ▼
   Auto Fix       Human Approval
       │                │
       └───────┬────────┘
               ▼
              n8n
               ↓
        Notification
               ↓
              END
```

Important LangGraph concepts used:

```text
State
Nodes
Edges
Conditional Edges
Parallel Execution
Checkpoints
Persistence
Interrupts
Human-in-the-Loop
Retries
```

---

# 🔍 LangSmith

LangSmith provides observability and evaluation for the AI system.

A typical trace:

```text
Incident
  ↓
Supervisor
  ↓
Triage Agent
  ↓
Log Tool
  ↓
Metrics Tool
  ↓
GitHub Tool
  ↓
Root Cause Agent
  ↓
Risk Agent
  ↓
Final Decision
```

Track:

```text
Prompt
LLM Response
Agent Decision
Tool Call
Tool Result
Retrieved Documents
Latency
Token Usage
Cost
Errors
```

---

# 🧪 LangSmith Evaluation

Create an evaluation dataset containing historical or simulated incidents.

Example:

```text
Incident #42

Expected Root Cause:
Database connection pool exhaustion

Agent Root Cause:
Database connection pool exhaustion

Result:
PASS
```

Metrics:

```text
Root Cause Accuracy
Tool Selection Accuracy
Severity Classification Accuracy
Resolution Accuracy
RAG Retrieval Quality
Hallucination Rate
Average Latency
Average Token Cost
```

Target benchmark example:

```text
Root Cause Accuracy        > 90%
Tool Selection Accuracy    > 90%
Severity Accuracy          > 95%
Resolution Accuracy        > 85%
```

These are project targets, not guaranteed results.

---

# 🔄 n8n Automation

n8n is the workflow automation layer.

LangGraph handles:

```text
AI reasoning
Agent coordination
State
Decision making
Tool selection
```

n8n handles:

```text
Business automation
External integrations
Notifications
Approvals
Scheduled workflows
Data movement
```

---

# ⚡ Example n8n Workflow

```text
Prometheus Alert
       ↓
      n8n
       ↓
Webhook
       ↓
OpsPilot API
       ↓
LangGraph
       ↓
Incident Analysis
       ↓
Risk Decision
       ↓
┌───────────────────────┐
│                       │
LOW                     HIGH
│                       │
▼                       ▼
Auto Fix             Slack Approval
│                       │
│                  Human Approves
│                       │
└───────────┬───────────┘
            ▼
       Execute Fix
            ↓
       Update Jira
            ↓
      Slack Notification
            ↓
      Save Incident
```

---

# 📚 RAG Architecture

The system stores organizational knowledge.

Sources:

```text
Runbooks
Postmortems
Architecture Documentation
Incident History
Troubleshooting Guides
Internal Documentation
```

Pipeline:

```text
Documents
    ↓
Document Loader
    ↓
Chunking
    ↓
Embeddings
    ↓
pgvector
    ↓
Retriever
    ↓
Relevant Context
    ↓
LangGraph Agent
```

---

# 🧠 Historical Incident Search

Example:

```text
Current Incident
       ↓
Vector Search
       ↓
Previous Incidents
       ↓
Incident #97
Incident #121
Incident #153
       ↓
Same error pattern detected
       ↓
Previous solution:
Rollback deployment
+
Increase DB pool
```

This allows the agent to use organizational memory instead of starting every investigation from zero.

---

# 🧩 MCP and Tools

Tools can expose enterprise capabilities to agents.

Examples:

```python
search_logs()
get_metrics()
get_deployment()
search_github()
search_incident_history()
create_jira()
send_slack()
query_database()
restart_service()
rollback_deployment()
```

The system should enforce permissions around every tool.

---

# 👨‍💻 Human-in-the-Loop

High-risk actions must require explicit approval.

Example:

```text
┌──────────────────────────────────────────┐
│         PRODUCTION ACTION REQUIRED       │
├──────────────────────────────────────────┤
│                                          │
│ Action: Rollback payment-api             │
│ From:   v2.4.1                           │
│ To:     v2.4.0                           │
│                                          │
│ Risk: HIGH                               │
│ Confidence: 94%                          │
│                                          │
│ Reason:                                  │
│ Recent deployment strongly correlates    │
│ with increased database timeouts.        │
│                                          │
│      [ APPROVE ]     [ REJECT ]          │
└──────────────────────────────────────────┘
```

After approval:

```text
Human
  ↓
n8n
  ↓
Kubernetes / GitHub
  ↓
Rollback
  ↓
Health Verification
  ↓
Close Incident
```

---

# 🔐 Security

Security is a core part of the system.

Implement:

```text
JWT Authentication
RBAC
API Keys
Secret Management
Tool Permissions
Prompt Injection Protection
Rate Limiting
Audit Logs
PII Redaction
Approval Gates
```

Example permission matrix:

| Action | Risk | Permission |
|---|---|---|
| Read logs | LOW | Automatic |
| Read metrics | LOW | Automatic |
| Search GitHub | LOW | Automatic |
| Create Jira | LOW | Automatic |
| Send Slack | LOW | Automatic |
| Restart service | MEDIUM | Configurable |
| Rollback production | HIGH | Human approval |
| Delete database | BLOCKED | Never |

---

# 📊 Dashboard

The frontend should provide a production-style operations dashboard.

Example:

```text
┌─────────────────────────────────────────────┐
│                  OpsPilot AI                │
├──────────────┬──────────────┬───────────────┤
│ Active       │ Resolved     │ AI Success    │
│ Incidents    │ Today        │ Rate          │
│     03       │      17      │     91%       │
├──────────────┴──────────────┴───────────────┤
│                                             │
│              INCIDENT TIMELINE              │
│                                             │
│  14:32  Alert received                     │
│    ↓                                        │
│  14:33  Triage completed                   │
│    ↓                                        │
│  14:34  Logs analyzed                      │
│    ↓                                        │
│  14:35  Root cause identified              │
│    ↓                                        │
│  14:36  Human approval requested           │
│    ↓                                        │
│  14:37  Rollback executed                  │
│                                             │
├─────────────────────────────────────────────┤
│ Root Cause: Database Connection Pool        │
│ Confidence: 94%                             │
│                                             │
│ [ View LangSmith Trace ]                    │
│ [ View Incident ]                           │
└─────────────────────────────────────────────┘
```

---

# 🛠️ Technology Stack

## Backend

```text
Python
FastAPI
Pydantic
SQLAlchemy
```

## AI / Agentic AI

```text
LangGraph
LangChain
LLM APIs
Structured Outputs
Function Calling
MCP
RAG
Embeddings
```

## Observability / Evaluation

```text
LangSmith
Prometheus
Grafana
```

## Database

```text
PostgreSQL
pgvector
Redis
```

## Automation

```text
n8n
```

## Frontend

```text
Next.js
React
TypeScript
Tailwind CSS
```

## Infrastructure

```text
Docker
Docker Compose
Kubernetes
AWS / GCP / Azure
Terraform
```

## DevOps

```text
Git
GitHub
GitHub Actions
CI/CD
```

## Integrations

```text
Slack
Jira
GitHub
Prometheus
Grafana
Kubernetes
Cloud Infrastructure
```

---

# 🗄️ Database Design

PostgreSQL tables:

```text
users
incidents
agent_runs
agent_decisions
tool_calls
approvals
actions
deployments
services
postmortems
evaluations
```

Example:

```text
incidents
---------------------------
id
service_id
severity
status
description
root_cause
confidence
created_at
resolved_at
```

```text
agent_runs
---------------------------
id
incident_id
agent_name
input
output
status
latency
token_usage
created_at
```

```text
approvals
---------------------------
id
incident_id
action
risk_level
requested_by
approved_by
status
created_at
approved_at
```

---

# 📁 Repository Structure

```text
opspilot-ai/
│
├── backend/
│   ├── api/
│   ├── agents/
│   │   ├── supervisor.py
│   │   ├── triage.py
│   │   ├── logs.py
│   │   ├── metrics.py
│   │   ├── github.py
│   │   ├── root_cause.py
│   │   ├── risk.py
│   │   └── communication.py
│   │
│   ├── graph/
│   │   ├── state.py
│   │   ├── graph.py
│   │   └── nodes.py
│   │
│   ├── tools/
│   ├── rag/
│   ├── models/
│   └── main.py
│
├── frontend/
│   ├── components/
│   ├── pages/
│   └── dashboard/
│
├── n8n/
│   ├── incident_trigger.json
│   ├── approval_workflow.json
│   └── remediation_workflow.json
│
├── evaluation/
│   ├── datasets/
│   ├── evaluators/
│   └── benchmarks/
│
├── infrastructure/
│   ├── docker/
│   ├── kubernetes/
│   └── terraform/
│
├── tests/
│
├── docs/
│   ├── architecture.md
│   ├── security.md
│   └── agent-design.md
│
├── docker-compose.yml
├── .env.example
├── requirements.txt
├── README.md
└── LICENSE
```

---

# 🔄 Incident Lifecycle

```text
1. Incident Detected
        ↓
2. Incident Triage
        ↓
3. Severity Classification
        ↓
4. Investigation Plan
        ↓
5. Parallel Evidence Collection
        ├── Logs
        ├── Metrics
        ├── GitHub
        ├── Deployments
        └── Historical Incidents
        ↓
6. Root Cause Analysis
        ↓
7. Confidence Calculation
        ↓
8. Risk Analysis
        ↓
9. Action Recommendation
        ↓
10. Human Approval if Required
        ↓
11. Remediation
        ↓
12. Health Verification
        ↓
13. Jira / Slack Update
        ↓
14. Incident Closure
        ↓
15. Postmortem Generation
        ↓
16. LangSmith Evaluation
```

---

# 🔥 Example Scenario

## Payment API Failure

Suppose the company deploys:

```text
payment-api v2.4.1
```

Five minutes later:

```text
Error Rate: 18.4%
Latency: 4.2 seconds
Database CPU: 92%
```

Prometheus sends an alert.

---

## Step 1 — n8n receives alert

```text
Prometheus
   ↓
n8n
   ↓
OpsPilot API
```

---

## Step 2 — LangGraph starts

```text
Supervisor
   ↓
Triage Agent
```

Triage:

```text
Severity: P1
Service: payment-api
Environment: production
```

---

## Step 3 — Parallel investigation

### Logs

```text
PostgreSQL timeout errors
```

### Metrics

```text
Database CPU increased
Connection pool exhausted
```

### GitHub

```text
Recent commit:
"Optimize payment query"
```

### Deployment

```text
v2.4.1 deployed 5 minutes before incident
```

### Historical RAG

```text
Previous incident had similar symptoms.
Previous solution:
Rollback deployment.
```

---

# 🧠 Root Cause

Agent concludes:

```text
ROOT CAUSE

The latest payment-api deployment introduced
a database query that significantly increased
execution time.

The increased query latency exhausted the
database connection pool, resulting in API
timeouts.

Confidence: 94%
```

---

# ⚠️ Risk Analysis

Agent recommends:

```text
Rollback v2.4.1 → v2.4.0
```

Risk:

```text
HIGH
```

Therefore:

```text
Human approval required.
```

---

# 👨‍💻 Approval

Engineer receives:

```text
OpsPilot AI

P1 Production Incident

Recommended Action:
Rollback payment-api v2.4.1

Confidence: 94%
Risk: HIGH

[ APPROVE ] [ REJECT ]
```

Engineer selects:

```text
APPROVE
```

---

# 🔄 Remediation

```text
Approval
   ↓
n8n
   ↓
Kubernetes
   ↓
Rollback
   ↓
Health Check
   ↓
Error Rate = 0.8%
   ↓
Incident Resolved
```

---

# 📝 Automatic Postmortem

OpsPilot generates:

```text
Incident:
INC-1042

Service:
payment-api

Severity:
P1

Root Cause:
Database query performance regression.

Impact:
18.4% request failures.

Resolution:
Rollback to v2.4.0.

Detection:
14:32

Resolution:
14:37

Duration:
5 minutes

Preventive Actions:
1. Add query performance tests.
2. Add deployment canary.
3. Add database latency alert.
4. Add connection pool monitoring.
```

---

# 🗺️ Development Roadmap

## Phase 1 — Foundation

### Week 1

Learn/build:

```text
Python
FastAPI
Pydantic
PostgreSQL
Docker
Git
```

Initial structure:

```text
/backend
/frontend
/agents
/workflows
/tools
/rag
/evaluation
/infra
```

---

# Phase 2 — LangGraph

### Week 2

Build:

```text
START
 ↓
Supervisor
 ↓
Agent
 ↓
Tool
 ↓
Decision
 ↓
END
```

Then implement:

```text
State
Conditional Edges
Retries
Memory
Checkpoints
Interrupts
```

---

# Phase 3 — Multi-Agent System

### Week 3–4

Implement:

```text
Supervisor Agent
Triage Agent
Log Agent
Metrics Agent
GitHub Agent
Root Cause Agent
Risk Agent
Communication Agent
```

---

# Phase 4 — RAG

### Week 5

Build:

```text
Documents
 ↓
Chunking
 ↓
Embeddings
 ↓
pgvector
 ↓
Retriever
 ↓
Agent
```

Knowledge base:

```text
Runbooks
Postmortems
Architecture Docs
Incident History
```

---

# Phase 5 — Tools / MCP

### Week 6

Implement:

```text
search_logs()
get_metrics()
get_deployment()
search_github()
create_jira()
send_slack()
restart_service()
rollback_deployment()
query_database()
```

Then introduce MCP where appropriate.

---

# Phase 6 — n8n

### Week 7

Build:

```text
Alert → AI Investigation
AI → Jira
AI → Slack
AI → Email
AI → Approval
AI → Remediation
```

---

# Phase 7 — LangSmith

### Week 8

Implement:

```text
Tracing
Datasets
Evaluations
Feedback
Latency Tracking
Token Tracking
Error Tracking
```

Create:

```text
50–100 test incidents
```

---

# Phase 8 — Security

### Week 9

Add:

```text
JWT
RBAC
Tool Permissions
Approval Gates
Rate Limits
Audit Logs
PII Masking
Prompt Injection Defense
```

---

# Phase 9 — Production Deployment

### Week 10

Dockerize:

```text
FastAPI
PostgreSQL
Redis
n8n
Frontend
```

Deploy using:

```text
Docker
Kubernetes
GitHub Actions
Terraform
```

Add:

```text
Prometheus
Grafana
```

---

# Phase 10 — Final Polish

### Week 11–12

Add:

```text
Professional Dashboard
Architecture Diagram
Demo Video
Benchmark Results
Evaluation Report
API Documentation
Docker Compose
CI/CD
Unit Tests
Integration Tests
Load Testing
Security Documentation
```

---

# 🧪 Evaluation Strategy

Create a benchmark dataset containing simulated or historical incidents.

Example:

```text
100 incidents
```

Each record:

```text
Input
Expected Root Cause
Expected Severity
Expected Tool
Expected Action
```

Example:

```text
Test #42

Expected:
Database connection pool exhaustion

Agent:
Database connection pool exhaustion

Result:
PASS
```

Measure:

```text
Root Cause Accuracy
Tool Selection Accuracy
Severity Accuracy
Resolution Accuracy
RAG Retrieval Quality
Hallucination Rate
Latency
Token Cost
```

Example target dashboard:

```text
Root Cause Accuracy       91%
Tool Selection Accuracy   94%
Severity Accuracy         96%
Resolution Accuracy       87%
```

Actual numbers should be reported only after running the evaluation.

---

# 🚀 Production Deployment

Recommended production architecture:

```text
Internet
   ↓
Load Balancer
   ↓
API Gateway
   ↓
FastAPI
   ↓
LangGraph
   ↓
Workers
   ↓
PostgreSQL
   ↓
pgvector

n8n
 ↓
External Integrations

LangSmith
 ↓
AI Observability

Prometheus
 ↓
Metrics

Grafana
 ↓
Infrastructure Dashboard
```

Containerization:

```text
Docker
```

Orchestration:

```text
Kubernetes
```

CI/CD:

```text
GitHub Actions
```

Infrastructure as Code:

```text
Terraform
```

---

# 🔐 Production Safety Principles

OpsPilot AI should follow these principles:

### 1. Least Privilege

Agents receive only the permissions required for their tasks.

### 2. Human Approval

High-impact production actions require human approval.

### 3. Auditability

Every important action must be recorded.

### 4. Observability

Every agent decision should be traceable.

### 5. Explainability

The system should explain why an action was recommended.

### 6. Fail Safe

If confidence is low, the system should request human intervention.

---

# 🌟 Why This Project Is Different

A basic AI project:

```text
User
 ↓
LLM
 ↓
Answer
```

OpsPilot AI:

```text
Event
 ↓
Supervisor
 ↓
Multi-Agent Investigation
 ↓
Tools
 ↓
RAG
 ↓
Evidence Correlation
 ↓
Root Cause
 ↓
Risk Assessment
 ↓
Human Approval
 ↓
Automation
 ↓
Remediation
 ↓
Verification
 ↓
Postmortem
 ↓
Evaluation
```

This demonstrates knowledge of:

```text
AI
Agentic AI
LLMs
RAG
Multi-Agent Systems
Workflow Orchestration
Observability
Evaluation
Backend Engineering
DevOps
Cloud
Security
Automation
```

---

# 💼 Resume Description

## OpsPilot AI — Enterprise Multi-Agent Incident Resolution Platform

> Built a production-oriented multi-agent incident response platform using **LangGraph, RAG and tool calling** to autonomously investigate infrastructure incidents across logs, metrics, deployments and source code. Integrated **LangSmith** for agent tracing, observability and evaluation, and **n8n** for event-driven automation, Jira/Slack workflows and human-in-the-loop remediation. Implemented **RBAC, risk-based tool permissions, approval gates, PostgreSQL/pgvector memory, automated incident reporting and postmortem generation**.

---

# 📌 Short Resume Version

> **OpsPilot AI:** Built a LangGraph-based multi-agent incident resolution system integrating RAG, LangSmith observability/evaluation and n8n automation to investigate production incidents, perform root-cause analysis and execute risk-controlled remediation with human approval.

---

# 🎯 Interview Talking Points

During interviews, be prepared to explain:

### Why LangGraph?

Because the workflow requires:

```text
State
Conditional Routing
Parallel Agents
Retries
Persistence
Human Interrupts
```

---

### Why not just one LLM?

Because different tasks require different:

```text
Tools
Permissions
Prompts
Context
Responsibilities
```

Specialized agents make the system modular.

---

### Why LangSmith?

Because production agent failures aren't limited to API errors.

The agent may:

```text
Choose the wrong tool
Retrieve bad context
Make a wrong decision
Loop unnecessarily
Use excessive tokens
```

Tracing and evaluation make these failures visible.

---

### Why n8n?

Because business automation and AI reasoning are different concerns.

LangGraph:

```text
AI reasoning
```

n8n:

```text
Workflow automation
```

---

### Why Human-in-the-Loop?

AI should not blindly execute destructive production actions.

The system should use:

```text
Risk
+
Confidence
+
Policy
```

to determine whether human approval is required.

---

### Why RAG?

The company already has organizational knowledge.

Instead of expecting the LLM to know everything:

```text
Current Incident
+
Company Knowledge
+
Historical Incidents
=
Better Investigation
```

---

# 📈 Future Enhancements

Possible future versions:

## v2.0

```text
Predictive Incident Detection
```

Predict incidents before they become critical.

---

## v2.1

```text
Auto-Generated Runbooks
```

AI generates troubleshooting procedures.

---

## v2.2

```text
Incident Pattern Mining
```

Identify recurring infrastructure problems.

---

## v2.3

```text
Cost Optimization Agent
```

Detect unnecessary cloud infrastructure costs.

---

## v2.4

```text
Security Operations Agent
```

Investigate suspicious infrastructure events.

---

## v2.5

```text
AI SRE Copilot
```

Natural language interface:

```text
"Why is payment-api slow?"
```

System:

```text
Investigating...

Logs ✓
Metrics ✓
Deployment ✓
GitHub ✓
Historical incidents ✓

Root cause:
Database query regression.

Confidence:
94%

Recommended:
Rollback v2.4.1.
```

---

# 🏆 Project Goals

The final system should demonstrate:

```text
                OpsPilot AI
                     │
       ┌─────────────┼─────────────┐
       │             │             │
       ▼             ▼             ▼
     AI/ML        Backend        DevOps
       │             │             │
       ▼             ▼             ▼
   LangGraph       FastAPI       Docker
   LangSmith      PostgreSQL    Kubernetes
   RAG            Redis         Terraform
   MCP            APIs          CI/CD
       │             │             │
       └─────────────┼─────────────┘
                     ▼
                 n8n
                     │
                     ▼
              Enterprise AI
```

---

# ⭐ Final Vision

The final product should feel like an **AI SRE / AI Operations Engineer** working alongside a company's engineering team.

Instead of:

> "Here is a chatbot."

The product should demonstrate:

> **"Give OpsPilot an incident, and it investigates the system, gathers evidence, reasons over company knowledge, identifies the probable root cause, evaluates remediation risk, asks for approval when necessary, executes the approved workflow, verifies recovery, updates the team, and records the entire AI decision process for evaluation."**

---

# 📜 License

This project is intended for educational, portfolio, research, and demonstration purposes.

Add an appropriate open-source license before public production use.
