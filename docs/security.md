# 🔐 OpsPilot AI - Security & Governance Architecture

**Author & Creator:** **Nivesh Kumar Meena**  
**Copyright © 2026 Nivesh Kumar Meena. All Rights Reserved.**

---

## 1. Principles of Least Privilege

OpsPilot AI enforces strict security perimeters between autonomous AI reasoning and production environments:

- **Read-Only Inspection**: Log search, metric queries, Git commit inspection, and RAG searches operate under read-only service accounts.
- **Action Tiering**: Actions are partitioned into four strict risk classifications:
  - **LOW**: Diagnostic queries, notifications, Jira ticket creation. Executed automatically.
  - **MEDIUM**: Service restarts, pod recycling. Configurable policy gates.
  - **HIGH**: Production deployments, image rollbacks, database configuration changes. Requires cryptographic human-in-the-loop approval.
  - **BLOCKED**: Destructive operations (drop database, truncate table, delete namespace). Hard-blocked in code.

---

## 2. Policy Enforcement Matrix

| Action | Risk Level | Auto Execute? | Requires Approval? |
|---|---|---|---|
| `search_logs` | LOW | Yes | No |
| `get_metrics` | LOW | Yes | No |
| `search_github` | LOW | Yes | No |
| `query_rag` | LOW | Yes | No |
| `create_jira` | LOW | Yes | No |
| `send_slack` | LOW | Yes | No |
| `restart_service` | MEDIUM | Configurable (Admin/SRE) | Optional |
| `rollback_deployment` | HIGH | **No** | **Yes (Mandatory)** |
| `delete_database` | BLOCKED | **No (Forbidden)** | Forbidden |

---

## 3. PII & Secret Redaction

Incoming log streams, tracebacks, and prompt inputs pass through regex and entropy-based sanitizers before reaching agents or vector memory:
- Bearer tokens & JWT headers
- AWS / Cloud IAM credentials
- API keys & secrets
- Credit card numbers & IPv4 addresses
- Personal Identifiable Information (emails, usernames)

---

## 4. Prompt Injection Defense

All user prompts and telemetry metadata are passed through `inspect_for_prompt_injection` to block adversarial instructions such as:
- `Ignore all previous instructions`
- `Reveal your system prompt`
- `Drop database / delete tables`
- `Bypass safety approvals`
