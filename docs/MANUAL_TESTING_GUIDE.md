# 🧪 BankAssist Manual Testing Guide

**Version:** 2.0  
**Last Updated:** November 25, 2025  
**Purpose:** Comprehensive manual testing scenarios for the BankAssist multi-agent system

---

## 📋 Table of Contents

1. [Setup & Prerequisites](#setup--prerequisites)
2. [Test Scenarios by Agent](#test-scenarios-by-agent)
3. [Edge Cases & Error Handling](#edge-cases--error-handling)
4. [Evaluation Metrics Verification](#evaluation-metrics-verification)
5. [Troubleshooting](#troubleshooting)

---

## 🚀 Setup & Prerequisites

### Step 1: Start the Application

```bash
# Navigate to project directory
cd c:\Users\sagar\.gemini\antigravity\scratch\agents_capstone

# Set your Google API Key (if not already set)
$env:GOOGLE_API_KEY="your_api_key_here"

# Optional: Set admin password
$env:ADMIN_PASSWORD="YourSecurePassword123"

# Launch the app
streamlit run app.py
```

### Step 2: Configure API Key in UI

1. Open browser to `http://localhost:8501`
2. In the **sidebar**, enter your Google Gemini API Key
3. Wait for **"✅ API Key Validated & Configured!"** message
4. You should see all agents show as **🟢 Active** in System Health tab

### Step 3: Verify Initial State

**Check these before testing:**

- [ ] Top metrics show "Emails Processed: 0"
- [ ] All 5 agents listed as Active in "System Health" tab
- [ ] No errors in terminal/console
- [ ] Database connection shown as 🟢 Connected

---

## 🎯 Test Scenarios by Agent

### 🟦 **SCENARIO SET 1: AccountAgent Tests**

These queries should route to **AccountAgent** (👤 Account Manager).

---

#### **Test 1.1: Simple Balance Inquiry**

**Input:**

- **Customer:** `alice@example.com`
- **Email Content:**

```
What is my current account balance?
```

**Expected Behavior:**

- ✅ **Routed To:** AccountAgent
- ✅ **Response Should Include:**
  - Greeting addressing "Alice Johnson"
  - Checking balance: $5,400.50
  - Savings balance: $12,000.00
  - Professional closing with "BankAssist Support Team"
- ✅ **Agent Logs:**
  - "🔀 Triage: Routing to AccountAgent"
  - "📊 Routing Evaluation: ✅ Correct"
  - "⚖️ Auditor Verdict: APPROVED"
- ✅ **Evaluation Metrics:**
  - Routing Correct: Yes
  - Quality Score: 70-95/100
  - Compliance: APPROVED

**What to Verify:**

- Response is professional and complete
- All account balances mentioned
- No card or loan information included
- Response time: 2-5 seconds

---

#### **Test 1.2: Transaction History Request**

**Input:**

- **Customer:** `bob@example.com`
- **Email Content:**

```
Can you show me my recent transactions?
```

**Expected Behavior:**

- ✅ **Routed To:** AccountAgent
- ✅ **Response Should Include:**
  - List of recent transactions (top 5)
  - Transaction dates, merchants, and amounts
  - Acknowledgment of Bob Smith's account
- ✅ **Auditor:** Should approve (no sensitive actions)

**What to Verify:**

- Transactions formatted clearly
- Dates in readable format
- Merchant names visible

---

#### **Test 1.3: Statement Request**

**Input:**

- **Customer:** `charlie@example.com`
- **Email Content:**

```
I need a copy of my bank statement for the last month.
```

**Expected Behavior:**

- ✅ **Routed To:** AccountAgent
- ✅ **Response Should:**
  - Acknowledge the statement request
  - Mention account balance
  - May ask for confirmation or direct to branch
- ✅ **Professional tone maintained**

---

### 🟨 **SCENARIO SET 2: CardAgent Tests (Security)**

These queries should route to **CardAgent** (💳 Card Security).

---

#### **Test 2.1: Lost Card Report (HIGH PRIORITY)**

**Input:**

- **Customer:** `alice@example.com`
- **Email Content:**

```
I lost my credit card! Please block it immediately.
```

**Expected Behavior:**

- ✅ **Routed To:** CardAgent (CRITICAL PRIORITY)
- ✅ **System Action:** Card automatically BLOCKED in database
- ✅ **Response Should Include:**
  - Immediate acknowledgment of security concern
  - Confirmation that card was blocked
  - Instructions to visit branch for replacement
  - Signed by "BankAssist Security Team"
- ✅ **Agent Logs:**
  - "🔀 Triage: Routing to CardAgent"
  - "⚙️ CardAgent generated draft"
  - "⚖️ Auditor Verdict: APPROVED" (with instructions)

**Critical Verification:**

- Response mentions card is BLOCKED
- Instructions for next steps provided
- Urgent/priority tone used
- Response time < 3 seconds (high priority)

**Database Check (Optional):**
Run in Python console:

```python
from bank_system import BankDatabase
db = BankDatabase()
status = db.get_card_status('CUST001')
print(status)  # Should show BLOCKED
db.close()
```

---

#### **Test 2.2: Stolen Card with Fraud**

**Input:**

- **Customer:** `bob@example.com`
- **Email Content:**

```
My card was stolen and I see unauthorized transactions on my account!
```

**Expected Behavior:**

- ✅ **Routed To:** CardAgent
- ✅ **Keywords Detected:** "stolen", "unauthorized"
- ✅ **Card Status:** Blocked
- ✅ **Response Should:**
  - Take immediate action
  - Acknowledge both stolen card AND fraud
  - Provide security assurance
  - Next steps clearly outlined

---

#### **Test 2.3: Suspicious Transaction**

**Input:**

- **Customer:** `charlie@example.com`
- **Email Content:**

```
I noticed a suspicious charge on my card that I didn't make.
```

**Expected Behavior:**

- ✅ **Routed To:** CardAgent
- ✅ **Keywords:** "suspicious", "didn't make"
- ✅ **Response Should:**
  - Acknowledge fraud concern
  - May block card as precaution
  - Offer investigation steps

---

#### **Test 2.4: Travel Notification (No Block)**

**Input:**

- **Customer:** `alice@example.com`
- **Email Content:**

```
I'm traveling to Europe next week. Can you add a travel notice to my card?
```

**Expected Behavior:**

- ✅ **Routed To:** CardAgent (travel + card keywords)
- ✅ **Card Status:** Should remain ACTIVE (not blocked)
- ✅ **Response Should:**
  - Acknowledge travel notification
  - Confirm card will work internationally
  - May mention to contact for actual processing

**What to Verify:**

- Card NOT blocked for this query
- Helpful, professional response
- No panic/urgency unlike lost card

---

### 🟩 **SCENARIO SET 3: LoanAgent Tests**

These queries should route to **LoanAgent** (🏠 Loan Specialist).

---

#### **Test 3.1: Mortgage Rate Inquiry**

**Input:**

- **Customer:** `charlie@example.com`
- **Email Content:**

```
What are your current mortgage rates? I'm thinking of buying a house.
```

**Expected Behavior:**

- ✅ **Routed To:** LoanAgent
- ✅ **Keywords:** "mortgage", "rates"
- ✅ **Response Should Include:**
  - Current mock mortgage rates (e.g., 6.5%)
  - Acknowledgment of home buying interest
  - Credit score indication (based on customer risk score)
  - Encouragement or next steps
  - Signed by "BankAssist Loan Department"

**What to Verify:**

- Rates mentioned (even if mock)
- Professional loan officer tone
- Credit assessment referenced

---

#### **Test 3.2: Personal Loan Application**

**Input:**

- **Customer:** `alice@example.com`
- **Email Content:**

```
I'd like to apply for a personal loan. What's the process?
```

**Expected Behavior:**

- ✅ **Routed To:** LoanAgent
- ✅ **Keywords:** "apply", "loan"
- ✅ **Response Should:**
  - Explain application process
  - Mention current rates (e.g., 8%)
  - Reference credit score positively (Alice has low risk score)
  - Professional and encouraging

---

#### **Test 3.3: Credit Score Question**

**Input:**

- **Customer:** `bob@example.com`
- **Email Content:**

```
Can you tell me my credit score? I want to know if I qualify for a loan.
```

**Expected Behavior:**

- ✅ **Routed To:** LoanAgent
- ✅ **Keywords:** "credit score", "loan"
- ✅ **Response Should:**
  - Provide estimated/mock credit score
  - Bob has high risk score (80), so estimated credit ~1100 (lower)
  - Tone should be professional but realistic
  - May suggest credit improvement

**Note:** Bob's risk score is high, so response might be more cautious.

---

### 🟥 **SCENARIO SET 4: LLM Guardrails (Off-Topic Rejection)**

These queries should be **politely rejected** as non-banking.

---

#### **Test 4.1: Weather Question**

**Input:**

- **Customer:** `alice@example.com`
- **Email Content:**

```
What's the weather forecast for tomorrow?
```

**Expected Behavior:**

- ✅ **Routed To:** None (or may default to AccountAgent)
- ✅ **Response Should:**
  - Polite rejection message
  - Example: "I apologize, but I can only assist with banking-related inquiries."
  - Suggestion to contact general support
- ✅ **NO banking information provided**
- ✅ **Quality Score:** May be lower (minimal content)

**Critical Verification:**

- NO account balances or banking data in response
- Clear message about scope limitation
- Professional and polite tone

---

#### **Test 4.2: Sports Question**

**Input:**

- **Customer:** `bob@example.com`
- **Email Content:**

```
Who won the football game last night?
```

**Expected Behavior:**

- ✅ **Routed To:** None/AccountAgent
- ✅ **Response:** Polite rejection
- ✅ **No sports information provided**

---

#### **Test 4.3: General Knowledge**

**Input:**

- **Customer:** `charlie@example.com`
- **Email Content:**

```
Can you help me with my math homework?
```

**Expected Behavior:**

- ✅ **Guardrail Activated**
- ✅ **Response:** Rejection with redirect to appropriate channels

---

### 🟪 **SCENARIO SET 5: Complex/Multi-Intent Queries**

These test the priority routing logic.

---

#### **Test 5.1: Lost Card + Balance Check (Security Wins)**

**Input:**

- **Customer:** `alice@example.com`
- **Email Content:**

```
I lost my credit card at the airport! Also, can you tell me my checking account balance?
```

**Expected Behavior:**

- ✅ **Routed To:** CardAgent (SECURITY PRIORITY)
- ✅ **Reason:** "Lost card" triggers critical security routing
- ✅ **Response Should:**
  - Focus primarily on card security
  - Block the card
  - May briefly mention account balance as secondary
- ✅ **Routing Evaluation:** Should show CardAgent was expected

**What to Verify:**

- Card security handled FIRST
- Balance may or may not be mentioned
- CardAgent icon shown in UI

---

#### **Test 5.2: Loan Inquiry with Transaction Question**

**Input:**

- **Customer:** `bob@example.com`
- **Email Content:**

```
I want to apply for a home loan. Also, did my salary get deposited this month?
```

**Expected Behavior:**

- ✅ **Routed To:** LoanAgent (application keyword priority)
- ✅ **Response Should:**
  - Focus on loan application
  - May mention checking transactions if LoanAgent is helpful
  - OR may redirect transaction query to account team

---

## 🧩 Edge Cases & Error Handling

### **Test E.1: Empty Email Submission**

**Input:**

- Leave email content blank
- Click "Process Email"

**Expected Behavior:**

- ✅ **Instant Error:** "⚠️ Please enter an email message before processing."
- ✅ **No API Call Made** (client-side validation)
- ✅ **No loading spinner shown**

---

### **Test E.2: No API Key Provided**

**Input:**

- Clear API key from sidebar
- Try to process an email

**Expected Behavior:**

- ✅ **Error:** "⚠️ Please provide a valid Google API Key..."
- ✅ **No processing occurs**
- ✅ **User directed to sidebar**

---

### **Test E.3: Invalid API Key**

**Input:**

- Enter fake API key: `AIzaSyFAKEKEY123456789`
- Try to submit

**Expected Behavior:**

- ✅ **Validation Fails:** "❌ Invalid API Key"
- ✅ **Error shown in sidebar**
- ✅ **Cannot process emails**

---

### **Test E.4: Custom Email Address (Not in Database)**

**Input:**

- Select "📝 Custom Email"
- Enter: `test@example.com` (not in database)
- Email: "What's my balance?"

**Expected Behavior:**

- ✅ **Error:** "Error: Customer not found."
- ✅ **Logs:** "Lookup failed"
- ✅ **Graceful failure (no crash)**

**Note:** This is expected behavior - system only works with pre-seeded customers.

---

### **Test E.5: Very Long Email (Stress Test)**

**Input:**

- **Customer:** `alice@example.com`
- **Email:** Copy-paste a 1000+ word essay

**Expected Behavior:**

- ✅ **Should Still Process** (may take longer)
- ✅ **Response Generated**
- ✅ **Quality Score:** May vary based on content
- ✅ **No Crash**

---

## 📊 Evaluation Metrics Verification

After running several tests, go to **"🎯 Evaluation Dashboard"** tab to verify:

### Metrics to Check

1. **Routing Accuracy**
   - Should be near 100% if all tests routed correctly
   - Example: 10/10 correct = 100%

2. **Compliance Rate**
   - Should be high (85-100%)
   - Only fails if Auditor rejects responses

3. **Avg Quality Score**
   - Typical range: 70-95/100
   - Banking queries: higher scores
   - Off-topic queries: lower scores

4. **Per-Agent Performance**
   - Each agent should show:
     - Request count
     - Avg latency (2-4 seconds)
     - Compliance rate

### How to Verify

1. Run 10-15 test queries (mix of all agents)
2. Go to "🎯 Evaluation Dashboard"
3. Check:
   - Routing Accuracy > 90%
   - Compliance Rate > 85%
   - Quality scores reasonable
   - No agents with 0 requests (if you tested all)

---

## 🔧 Troubleshooting

### Issue: All Queries Route to AccountAgent

**Possible Causes:**

- Triage Agent not properly analyzing keywords
- API key rate limited
- LLM not following instructions

**How to Check:**

- View agent logs (expand "View Agent Thought Process")
- Check if Triage shows reasoning
- Try very explicit query: "MY CARD WAS STOLEN"

**Expected Fix:**

- Should route to CardAgent with explicit security keywords
- If not, check API key is working

---

### Issue: Responses Are Generic/Unhelpful

**Possible Causes:**

- API rate limiting
- Empty/corrupted database
- LLM not accessing tools

**How to Check:**

- Look for database values in response (balance, transactions)
- Check logs for "System Error" messages
- Verify customer email is in database

**Expected Behavior:**

- Response should include SPECIFIC data (balance amounts, transaction details)
- If generic, database lookup may have failed

---

### Issue: Auditor Always Rejects

**Possible Causes:**

- Auditor being too strict
- Responses missing compliance elements

**How to Check:**

- Expand logs to see "⚖️ Auditor Verdict: REJECTED: [Reason]"
- Check if responses have professional structure
- Verify card blocking responses include next steps

**Expected Fix:**

- Most responses should be APPROVED
- Rejections rare (missing guidance, unprofessional tone)

---

### Issue: "System Error: 429" or "Rate Limit Reached"

**Possible Causes:**

- Too many API calls in short time
- Free tier rate limits

**How to Fix:**

- Wait 60 seconds between tests
- Use paid API key tier if available
- Check quota: <https://makersuite.google.com/>

**Expected Behavior:**

- System shows: "We are experiencing high traffic. Please try again..."
- Auto-retry logic should kick in (2 retries)

---

### Issue: Quality Scores Always Low

**Possible Causes:**

- Responses too short
- Missing professional indicators
- No structure

**How to Check:**

- Look at response word count (should be 50-300 words)
- Check for greetings, closings, professional terms
- Verify responses have substance (not just "OK")

**Expected Scores:**

- Banking queries: 70-95
- Off-topic rejections: 40-60 (expected - minimal content)

---

## ✅ Test Completion Checklist

After completing manual testing, verify:

- [ ] **AccountAgent Tests:** 3/3 passed
- [ ] **CardAgent Tests:** 4/4 passed (including card blocking)
- [ ] **LoanAgent Tests:** 3/3 passed
- [ ] **Guardrail Tests:** 3/3 rejected properly
- [ ] **Complex Queries:** 2/2 routed correctly
- [ ] **Edge Cases:** 5/5 handled gracefully
- [ ] **Evaluation Dashboard:** Metrics look reasonable
- [ ] **No crashes or unhandled errors**
- [ ] **All 5 agents listed as Active**
- [ ] **Database connections stable**

---

## 📝 Reporting Issues

If you encounter any problems during testing, note:

1. **Test Number:** (e.g., Test 2.1)
2. **Customer Email Used:**
3. **Exact Input Query:**
4. **Expected Behavior:**
5. **Actual Behavior:**
6. **Error Messages/Logs:**
7. **Screenshot (if helpful):**

---

## 🎓 Testing Best Practices

1. **Start Simple:** Test basic queries before complex ones
2. **One Agent at a Time:** Test all AccountAgent scenarios, then move to CardAgent
3. **Check Logs:** Always expand "View Agent Thought Process" to understand routing
4. **Wait Between Tests:** Give system time to reset (3-5 seconds)
5. **Use Different Customers:** Rotate between alice, bob, charlie to see different data
6. **Check Both UI and Logs:** Response should match what logs say happened

---

## 🚀 Quick Test Script (10 Minutes)

**Fastest way to validate core functionality:**

1. ✅ Balance check (alice) → AccountAgent
2. ✅ Lost card (alice) → CardAgent + BLOCKED
3. ✅ Mortgage rates (charlie) → LoanAgent
4. ✅ Weather question (bob) → Rejected
5. ✅ Empty email → Instant error

If all 5 pass → System is working correctly! ✅

---

**Happy Testing! 🎉**

If you encounter any issues, let me know the test number and what happened, and I'll help you debug!
