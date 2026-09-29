# 🤖 OpsPilot AI - Agent Design & Prompt Specifications

**Author & Creator:** **Nivesh Kumar Meena**  
**Copyright © 2026 Nivesh Kumar Meena. All Rights Reserved.**

---

## Agent Specification Overview

OpsPilot AI coordinates eight specialized agents within a unified LangGraph state machine:

### 1. Supervisor Agent
- **Role**: Workflow Coordinator & Investigation Dispatcher
- **State Inputs**: `service_name`, `error_rate`, `latency_ms`
- **Output**: Parallel route plan (`["logs", "metrics", "github", "rag"]`)

### 2. Incident Triage Agent
- **Role**: SLA & Blast Radius Evaluator
- **Logic**:
  - $P1$ if $\text{error\_rate} \ge 15\%$ or $\text{latency} \ge 3500\text{ms}$ in production.
  - $P2$ if $\text{error\_rate} \ge 5\%$ or $\text{latency} \ge 1000\text{ms}$.
  - $P3$ if $\text{error\_rate} \ge 1\%$.
  - $P4$ otherwise.

### 3. Log Investigation Agent
- **Role**: Error Clusterer & Exception Extractor
- **Tools**: `search_logs(service, minutes_back)`
- **Output**: Error distribution, primary exception, sample stack traces.

### 4. Metrics Agent
- **Role**: Statistical Telemetry & Anomaly Detector
- **Tools**: `get_metrics(service, duration_minutes)`
- **Output**: Latency p99, database connection pool active count, host CPU utilization.

### 5. Code & Deployment Agent
- **Role**: CI/CD & Commit Regression Analyzer
- **Tools**: `get_deployment(service)`, `search_github(service, commit_sha)`
- **Output**: Recent version deployment timestamp, commit author, PR diff.

### 6. Root Cause Agent
- **Role**: Causal Synthesis & Precedent Matching
- **Tools**: `retriever.retrieve_incident_context(service, symptoms)`
- **Output**: Concise causal explanation, confidence percentage (e.g. 94%), evidence summary.

### 7. Risk & Policy Agent
- **Role**: Remediation Gatekeeper & Safety Enforcer
- **Tools**: `evaluate_action_policy(action_name)`
- **Output**: Approval payload, risk level (HIGH), human approval interrupt flag.

### 8. Communication Agent
- **Role**: Stakeholder Broadcaster & Postmortem Generator
- **Tools**: `send_slack(...)`, `create_jira(...)`
- **Output**: Postmortem document, Slack payload, Jira issue key (`OPS-1042`).
