# 🏦 BankAssist Enterprise

**Intelligent Multi-Agent Banking Support System**

BankAssist is a production-ready AI agent system designed to automate customer support for banking services. Built with **Google Gemini Flash** and **Streamlit**, it uses a multi-agent architecture to securely handle balance inquiries, card security, and loan applications.

---

## 🆕 Latest Updates (v2.0)

We have significantly optimized the system for performance and robustness:

* **⚡ Model Upgrade:** Switched to **Gemini 2.5 Flash** for faster, more accurate responses.
* **📉 66% API Reduction:** Implemented **Hybrid Triage** (Rule-based + LLM) and **Conditional Auditing** to reduce API calls for common queries from 3 to 1.
* **📝 Enhanced Visibility:** Added verbose API logging in the UI to show exact model interactions and latency.
* **📊 Dashboard Fixes:** Evaluation metrics now correctly track all queries, including optimized/skipped steps.

---

## 🚀 Key Features

* **🤖 Multi-Agent Architecture:** Specialized agents for Triage, Accounts, Cards, Loans, and Compliance.
* **⚡ Hybrid Routing:** Zero-latency rule-based triage for common queries + LLM fallback for complex intents.
* **🛡️ Enterprise Security:**
  * **Guardrails:** Strict off-topic rejection.
  * **Auditor Agent:** Reviews every high-risk response before sending.
  * **PII Protection:** Mock database ensures no real data leakage.
* **📊 Evaluation Dashboard:** Real-time metrics for routing accuracy, compliance rates, and quality scores.
* **📝 Verbose Logging:** Full visibility into API calls, latency, and agent reasoning in the UI.

---

## 📂 Project Structure

```
├── app.py              # Main Streamlit Application
├── agents.py           # Agent Definitions (Triage, Account, Card, Loan, Auditor)
├── workflow.py         # Workflow Orchestration & Logic
├── bank_system.py      # Mock Banking Database (SQLite)
├── evaluation.py       # ADK-Style Evaluation Metrics
├── requirements.txt    # Project Dependencies
├── docs/               # Documentation & Guides
│   ├── MANUAL_TESTING_GUIDE.md
│   ├── CRITICAL_TEST_CASES.md
│   ├── QUICK_TEST_REFERENCE.md
│   └── DEPLOYMENT.md
└── tests/              # Unit & Integration Tests
```

---

## 🛠️ Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/yourusername/bankassist.git
cd bankassist
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run app.py
```

### 3. Configure API Key

* Open the app in your browser (usually `http://localhost:8501`).
* Enter your **Google Gemini API Key** in the sidebar.
* *Don't have a key? Get one [here](https://makersuite.google.com/app/apikey).*

---

## 🧪 Testing

We provide comprehensive testing guides in the `docs/` folder:

* **[Quick Start Guide](docs/QUICK_TEST_REFERENCE.md):** 5-minute smoke test.
* **[Manual Testing Guide](docs/MANUAL_TESTING_GUIDE.md):** Detailed scenarios for every agent.
* **[Critical Stress Tests](docs/CRITICAL_TEST_CASES.md):** Security and edge-case testing.

---

## 🏗️ Architecture

### The Hybrid Workflow

1. **User Query** → **Triage Agent**
    * *Fast Path:* Keywords (e.g., "lost card") route immediately.
    * *Slow Path:* LLM analyzes complex intent.
2. **Specialist Agent** (Account/Card/Loan)
    * Retrieves data from `bank_system.py`.
    * Generates a personalized response using Gemini.
3. **Auditor Agent** (Conditional)
    * *High Risk:* Reviews response for compliance (Card/Loan).
    * *Low Risk:* Skips review for speed (Balance checks).
4. **Final Response** → User

---

## 📊 Evaluation

The system includes a built-in **Evaluation Dashboard** (Tab 3) that tracks:

* **Routing Accuracy:** Did the email go to the right agent?
* **Compliance Rate:** Did the Auditor approve the response?
* **Quality Score:** Automated scoring of tone and structure.
* **Latency:** Processing time per request.

---

## 👥 Team

**Kaggle Agents Intensive - Capstone Project**

* **SagarGrv** - Team Leader
* **Rhythm Mantri** - Core Developer

---

*Built with ❤️ using Google Gemini and Streamlit.*
