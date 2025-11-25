# 🛡️ Security & Compliance Audit

**Date:** 2025-11-25
**Status:** ✅ PASSED

This document certifies that the **BankAssist** codebase has undergone a security review prior to submission.

## 🔒 1. Secret Management

* **API Keys:** No hardcoded keys. The system uses `st.sidebar` input or `os.environ["GOOGLE_API_KEY"]`.
* **Admin Access:** The Admin Dashboard uses a secure comparison against `os.environ["ADMIN_PASSWORD"]` (with a safe default for local demos).
* **Git Ignore:** `.env`, `*.db`, and `.streamlit/secrets.toml` are strictly excluded from version control.

## 👤 2. PII & Data Privacy

* **Mock Data:** All customer data (Alice, Bob, Charlie) is synthetically generated in `bank_system.py`. No real user data is ever processed.
* **Local Execution:** The SQLite database runs locally. No customer data is sent to the cloud *except* the specific query text sent to Gemini (which is stateless).

## 👮 3. AI Safety Guardrails

* **Auditor Agent:** A dedicated LLM agent reviews high-risk responses (Loans, Fraud) for compliance before they are shown to the user.
* **Off-Topic Rejection:** The Triage Agent is instructed to reject non-banking queries (e.g., "Write me a poem").

---
*Verified by BankAssist Dev Team*
