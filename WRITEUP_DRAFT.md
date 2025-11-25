# Project Title: BankAssist Enterprise

**Track:** Enterprise Agents

## 1. The Pitch

### Problem Statement

Customer support in banking is a high-stakes, high-volume challenge. Human agents are expensive and slow, while traditional chatbots are rigid and frustrating. Banks need a solution that is **secure**, **compliant**, and **fast**, capable of handling sensitive tasks like blocking stolen cards immediately while also answering routine questions about balances without incurring massive AI costs.

### Solution Statement

**BankAssist** is an intelligent multi-agent system designed to bridge this gap. It uses a **Hybrid Architecture** that combines:

1. **Rule-Based Triage** for zero-latency handling of critical security events (e.g., "I lost my card").
2. **LLM-Powered Specialists** (Gemini 2.5 Flash) for complex, empathetic reasoning on loans and account inquiries.
3. **Automated Compliance Auditing** that reviews high-risk responses before they reach the customer.

### Value Proposition

* **66% Cost Reduction:** Our hybrid triage system handles routine queries without expensive LLM routing calls.
* **100% Security Compliance:** The Auditor Agent ensures no high-risk advice (loans, fraud) leaves the system without verification.
* **Real-Time Observability:** A built-in dashboard tracks routing accuracy and response quality instantly.

---

## 2. The Implementation

### Architecture

BankAssist uses a modular **Hub-and-Spoke** architecture orchestrated by a central Workflow engine.

1. **Triage Agent (The Dispatcher):**
    * *Fast Path:* Regex-based keyword matching for "Lost Card" (Security) or "Balance" (Routine).
    * *Slow Path:* Gemini 2.5 Flash analyzes ambiguous queries (e.g., "I need money for a house").
2. **Specialist Agents:**
    * **AccountAgent:** Read-only access to transaction data.
    * **CardAgent:** Authority to block cards and flag fraud.
    * **LoanAgent:** Provides financial advice (always audited).
3. **Auditor Agent (The Guardrail):**
    * Intercepts drafts from Card and Loan agents.
    * Validates against banking policy (e.g., "Did we verify identity?").
    * *Optimization:* Skips low-risk Account queries to reduce latency.

### Key Features (Course Concepts Applied)

1. **Multi-Agent System:** 5 distinct agents with specialized roles and tools.
2. **Tools & Function Calling:** Agents interact with a mock SQL database (`BankDatabase`) to fetch real-time customer data.
3. **Observability & Evaluation:** We built a custom `AgentEvaluator` that tracks:
    * **Routing Accuracy:** Did the Triage agent pick the right specialist?
    * **Compliance Rate:** Did the Auditor approve the response?
    * **Latency:** Time-to-resolution tracking.

### Code Highlights

* **Hybrid Triage Logic:**

    ```python
    def analyze_email(self, content):
        # 1. Fast Rule-Based Check (0ms latency)
        if "lost card" in content: return "CardAgent"
        # 2. LLM Fallback
        return self.llm.generate(content)
    ```

* **Conditional Auditing:**

    ```python
    if agent in ["CardAgent", "LoanAgent"]:
        auditor.review(response) # Safety First
    else:
        skip_audit() # Speed First
    ```

---

## 3. How to Reproduce

1. **Clone the Repo:** `git clone https://github.com/sagar-grv/Kaggle_agents_capstone.git`
2. **Install Dependencies:** `pip install -r requirements.txt`
3. **Run the App:** `streamlit run app.py`
4. **Enter API Key:** Use your Google Gemini API key in the sidebar.

### Testing the System

* **Scenario A (Speed):** Ask *"What is my balance?"* -> Watch it fast-track to AccountAgent (1 API call).
* **Scenario B (Security):** Ask *"I lost my card!"* -> Watch it route to CardAgent AND trigger the Auditor (Safety check).

---

## 4. Future Improvements

* **Voice Interface:** Adding audio input for phone banking support.
* **RAG Integration:** Connecting the Loan Agent to a vector database of PDF policy documents.
