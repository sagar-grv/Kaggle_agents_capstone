# 🎯 Quick Test Reference Card

**Print this page for quick reference during manual testing!**

---

## 🚀 Quick Start (3 steps)

1. `streamlit run app.py`
2. Enter API key in sidebar
3. Start testing below ⬇️

---

## ✅ 5-Minute Smoke Test

Copy-paste these queries to verify core functionality:

### Test 1: Balance Check ✓

- **Email:** <alice@example.com>
- **Query:** `What is my current account balance?`
- **Expected:** AccountAgent → Shows $5,400.50 + $12,000.00

### Test 2: Lost Card 🚨

- **Email:** <alice@example.com>  
- **Query:** `I lost my credit card! Please block it immediately.`
- **Expected:** CardAgent → Card BLOCKED + visit branch instructions

### Test 3: Mortgage Rates 🏠

- **Email:** <charlie@example.com>
- **Query:** `What are your current mortgage rates?`
- **Expected:** LoanAgent → Shows rates (6.5%), credit score mention

### Test 4: Off-Topic ⛔

- **Email:** <bob@example.com>
- **Query:** `What's the weather today?`
- **Expected:** Polite rejection → "only assist with banking inquiries"

### Test 5: Empty Email 🛑

- **Email:** (any)
- **Query:** (leave blank)
- **Expected:** Instant error → "Please enter an email message"

**If all 5 pass → ✅ System working correctly!**

---

## 📋 Pre-Seeded Customer Data

| Email | Name | Checking | Savings | Risk Score | Card Status |
|-------|------|----------|---------|------------|-------------|
| `alice@example.com` | Alice Johnson | $5,400.50 | $12,000.00 | 10 (low) | ACTIVE* |
| `bob@example.com` | Bob Smith | $200.00 | - | 80 (high) | BLOCKED |
| `charlie@example.com` | Charlie Brown | $850.00 | - | 5 (low) | ACTIVE |

*Will change to BLOCKED after lost card test

---

## 🎯 Agent Routing Keywords

### → AccountAgent (👤)

- balance, account, transaction, statement, deposit, withdrawal

### → CardAgent (💳) [PRIORITY]

- **lost, stolen, fraud, unauthorized, suspicious, hacked**

### → LoanAgent (🏠)

- loan, mortgage, credit, borrow, financing, rate, apply

### → None (Rejected)

- weather, sports, homework, recipes, etc.

---

## 🔍 What to Check in Responses

✅ **Good Response Checklist:**

- [ ] Customer name mentioned (e.g., "Dear Alice")
- [ ] Specific data included ($5,400.50, not "your balance")
- [ ] Professional tone
- [ ] Clear signature ("BankAssist [Team Name]")
- [ ] 50-300 words (not too short/long)
- [ ] Answers the actual question

❌ **Red Flags:**

- Generic responses ("Your account is fine")
- No specific numbers/data
- Wrong agent (balance → CardAgent)
- Crash or "System Error"
- Off-topic answers with banking data

---

## 🚨 Security Tests - MUST PASS

### Critical: Card Blocking

**Query:** `"I lost my card!"`
**Must Include:**

1. ✅ Card is BLOCKED (explicit confirmation)
2. ✅ Visit branch for replacement
3. ✅ Security tone (urgent but reassuring)
4. ✅ Signed by "Security Team"

**Verify in Logs:**

- "Routing to CardAgent"
- "generated draft"
- "Auditor Verdict: APPROVED"

---

## 📊 Evaluation Dashboard Quick Check

After 10+ tests, check **"🎯 Evaluation Dashboard"**:

| Metric | Good Range | Red Flag |
|--------|------------|----------|
| Routing Accuracy | 90-100% | < 80% |
| Compliance Rate | 85-100% | < 70% |
| Avg Quality Score | 70-95 | < 50 |
| Avg Latency | 2-5 sec | > 10 sec |

---

## 🛠️ Common Issues & Fixes

### Issue: Everything routes to AccountAgent

**Fix:** Use explicit keywords: "MY CARD WAS STOLEN"

### Issue: No specific data in responses

**Fix:** Check customer email is valid (alice/bob/charlie only)

### Issue: "Rate Limit" errors

**Fix:** Wait 60 seconds, use slower pace

### Issue: Generic/vague responses

**Fix:** Check API key is valid, may be using fallback

---

## 🎓 Testing Tips

1. **Read the Logs!** Click "View Agent Thought Process"
2. **One test at a time** - wait 3 seconds between
3. **Try all 3 customers** - different data for each
4. **Check System Health** - all should be 🟢 Active
5. **Rotate agents** - don't just test one agent

---

## 📞 Report Issues Template

```
Test #: [e.g., Test 2.1]
Customer: [alice/bob/charlie]
Query: "[exact text]"
Expected: [what should happen]
Actual: [what did happen]
Logs: [paste error if any]
```

---

## 🎉 Success Criteria

Your testing is complete when:

- ✅ All 3 agents respond correctly
- ✅ Security queries block cards
- ✅ Off-topic queries rejected politely
- ✅ Empty emails caught immediately
- ✅ Evaluation metrics in good ranges
- ✅ No crashes or unhandled errors
- ✅ Responses contain specific data

**Total Test Time:** 10-15 minutes for full suite

---

**For detailed tests → See MANUAL_TESTING_GUIDE.md**

**Happy Testing! 🚀**
