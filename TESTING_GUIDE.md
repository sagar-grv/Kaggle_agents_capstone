# BankAssist - Extreme Testing Guide 🧪

## Overview

This guide provides comprehensive test scenarios including edge cases and extreme conditions to thoroughly validate the BankAssist system.

---

## Test Setup

### Prerequisites

```bash
# Set your API key
export GOOGLE_API_KEY="your_api_key_here"

# Start the application
streamlit run app.py
```

### Available Test Customers

- **<alice@example.com>** - Alice Johnson (Risk Score: 10, Low Risk)
- **<bob@example.com>** - Bob Smith (Risk Score: 80, High Risk)
- **<charlie@example.com>** - Charlie Brown (Risk Score: 5, Very Low Risk)

---

## 1. Normal Scenarios (Baseline)

### Test 1.1: Simple Balance Inquiry

**Email:** `What is my account balance?`  
**Customer:** <alice@example.com>  
**Expected Agent:** AccountAgent  
**Expected Output:**

- Balance information for checking and savings accounts
- Professional tone
- Signed by "BankAssist Support Team"
- ✅ Auditor: APPROVED

### Test 1.2: Lost Card Report

**Email:** `I lost my credit card`  
**Customer:** <bob@example.com>  
**Expected Agent:** CardAgent  
**Expected Output:**

- Card blocked confirmation
- Instructions to visit branch for replacement
- Security-focused language
- ✅ Auditor: APPROVED

### Test 1.3: Loan Inquiry

**Email:** `What are your mortgage rates?`  
**Customer:** <charlie@example.com>  
**Expected Agent:** LoanAgent  
**Expected Output:**

- Mock rates (Mortgage 6.5%, Personal 8%)
- Credit score mention
- Professional tone
- ✅ Auditor: APPROVED

---

## 2. Edge Cases - Multi-Intent Emails

### Test 2.1: Security + Balance (Priority Test)

**Email:** `I lost my wallet with my card! Also, can you tell me my balance?`  
**Customer:** <alice@example.com>  
**Expected Agent:** CardAgent (Security takes priority!)  
**Expected Output:**

- Card blocking confirmation
- Balance query deferred or mentioned secondary
- Security-first response
- ✅ Auditor: APPROVED

### Test 2.2: Three Intents in One

**Email:** `I need a loan, my card was stolen, and what's my account balance?`  
**Customer:** <bob@example.com>  
**Expected Agent:** CardAgent (Security is highest priority)  
**Expected Output:**

- Focus on card security
- Other requests acknowledged but not primary
- ✅ Auditor: APPROVED

---

## 3. Extreme Conditions - Input Validation

### Test 3.1: Empty Email

**Email:** ` ` (just spaces)  
**Customer:** <alice@example.com>  
**Expected Agent:** AccountAgent (default fallback)  
**Expected Output:**

- Generic helpful response or error handling
- No crash

### Test 3.2: Very Long Email (>500 words)

**Email:**

```
I have been a customer for 20 years and I am very concerned about 
my account. I noticed that there are several transactions that I 
don't recognize. I was at the grocery store yesterday and [continue 
with a 500+ word rambling email about various topics]...
```

**Customer:** <bob@example.com>  
**Expected Agent:** CardAgent (fraud keywords trigger)  
**Expected Output:**

- Should handle long input without crashing
- Focus on fraud keywords
- ✅ Response generated successfully

### Test 3.3: Special Characters

**Email:** `My card is lost!!! 😱😱😱 ###URGENT### @@@`  
**Customer:** <charlie@example.com>  
**Expected Agent:** CardAgent  
**Expected Output:**

- Handle special characters gracefully
- Respond to "lost card" intent
- ✅ Auditor: APPROVED

### Test 3.4: ALL CAPS SHOUTING

**Email:** `I NEED MY BALANCE RIGHT NOW!!!`  
**Customer:** <alice@example.com>  
**Expected Agent:** AccountAgent  
**Expected Output:**

- Calm, professional response despite aggressive tone
- Balance information provided
- ✅ Auditor: APPROVED

---

## 4. Extreme Cases - Ambiguity

### Test 4.1: Vague Request

**Email:** `Help`  
**Customer:** <bob@example.com>  
**Expected Agent:** AccountAgent (default)  
**Expected Output:**

- Generic helpful response
- Offer to clarify needs
- No crash

### Test 4.2: Unrelated Query

**Email:** `What's the weather like today?`  
**Customer:** <charlie@example.com>  
**Expected Agent:** AccountAgent (default)  
**Expected Output:**

- Polite redirection to banking topics
- Professional tone

### Test 4.3: Mixed Languages (if applicable)

**Email:** `Hola, I lost my tarjeta de credito`  
**Customer:** <alice@example.com>  
**Expected Agent:** CardAgent (recognizes "lost")  
**Expected Output:**

- Should still detect "lost" keyword
- Card blocking action
- English response

---

## 5. Security & Compliance Edge Cases

### Test 5.1: Aggressive Guarantee Request

**Email:** `Can you guarantee I'll get this loan?`  
**Customer:** <bob@example.com>  
**Expected Agent:** LoanAgent  
**Expected Output:**

- Response should NOT contain "guarantee" or "promise"
- ⚠️ Auditor should flag if guarantee is made
- Should say "formal application needed"

### Test 5.2: Request for Sensitive Data

**Email:** `Send me all my transaction details via email`  
**Customer:** <charlie@example.com>  
**Expected Agent:** AccountAgent  
**Expected Output:**

- Should NOT send detailed PFI in email body
- ⚠️ Auditor should REJECT if detailed transactions included
- Should direct to secure portal

---

## 6. System Stress Tests

### Test 6.1: Rapid Consecutive Requests

**Action:** Submit 5 emails in quick succession  
**Expected:**

- All processed successfully
- No crashes
- Each gets unique response

### Test 6.2: Invalid Customer Email

**Email:** `I lost my card`  
**Customer:** `invalid@notfound.com`  
**Expected Output:**

- "Error: Customer not found."
- Graceful error handling

---

## 7. UI Validation Tests

### Test 7.1: Analytics Tab Population

**Action:** Process 3 different types of emails (Account, Card, Loan)  
**Check:**

- ✅ Traffic Distribution chart shows all 3 agents
- ✅ Detailed Log table has 3 rows
- ✅ Metrics update correctly

### Test 7.2: System Health Tab

**Action:** Navigate to "System Health" tab  
**Check:**

- ✅ All 5 agents shown: Triage, Account, Card, Loan, Auditor
- ✅ All show 🟢 Active
- ✅ Database shows Connected

---

## Expected Success Criteria

### ✅ Pass Conditions

1. **No Application Crashes** - System handles all inputs
2. **Correct Routing** - Security always takes priority
3. **Auditor Compliance** - No guarantees, no PFI leaks
4. **Professional Tone** - Even with aggressive inputs
5. **UI Updates** - Analytics and metrics work correctly

### ⚠️ Warning Conditions (Acceptable)

1. Auditor rejects overly detailed responses (this is correct behavior)
2. Generic responses for vague/unrelated queries
3. Rate limit messages during rapid testing

### ❌ Fail Conditions

1. Application crash
2. Security routing failures (fraud/lost card → wrong agent)
3. Auditor approves responses with guarantees
4. Data exposure (detailed PFI in email body)
5. Missing Loan Agent in System Health

---

## Sample Test Session

```bash
# Test Session Example
1. Open app: streamlit run app.py
2. Enter API key in sidebar
3. Test sequence:
   - alice@example.com: "What's my balance?" → AccountAgent
   - bob@example.com: "Fraud on my account!" → CardAgent
   - charlie@example.com: "Loan rates?" → LoanAgent
   - alice@example.com: "Lost card + need balance" → CardAgent (priority)
4. Check Analytics tab → Should show distribution
5. Check System Health → Should show 5 agents
```

---

## Automated Test Command

```bash
# Run the automated test suite
python tests/test_end_to_end.py

# Expected: 4/4 scenarios pass
```

---

## Troubleshooting

**If tests fail:**

1. Check API key is set correctly
2. Verify all dependencies installed: `pip install -r requirements.txt`
3. Check database exists: `bankassist.db` should be created automatically
4. Review logs in expander for error details

**Rate Limit Issues:**

- Wait 60 seconds between rapid tests
- System has retry logic with exponential backoff
- Will show "High traffic" message if exhausted
