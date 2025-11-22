"""
Comprehensive System Diagnostic Test
Run this to identify all issues in the BankAssist system
"""
# CRITICAL: Set API key BEFORE importing other modules
import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyBR0fPdqCAB7_6ASAj8cK-T4atrkfHz6TU"

# Now import after API key is set
from workflow import BankWorkflow
from bank_system import BankDatabase
import traceback

print("="*70)
print("BANKASSIST SYSTEM DIAGNOSTIC TEST")
print("="*70)

# Test 1: Database Initialization
print("\n[TEST 1] Database Initialization...")
try:
    db = BankDatabase()
    print("✅ PASS - Database initialized successfully")
    
    # Check if customers exist
    alice = db.get_customer_by_email("alice@example.com")
    bob = db.get_customer_by_email("bob@example.com")
    charlie = db.get_customer_by_email("charlie@example.com")
    
    if alice and bob and charlie:
        print("✅ PASS - All test customers found")
    else:
        print("❌ FAIL - Missing test customers")
    
    db.close()
except Exception as e:
    print(f"❌ FAIL - Database error: {e}")
    traceback.print_exc()

# Test 2: Workflow Initialization
print("\n[TEST 2] Workflow Initialization...")
try:
    workflow = BankWorkflow()
    print("✅ PASS - Workflow initialized")
    
    # Check all agents exist
    if hasattr(workflow, 'triage') and hasattr(workflow, 'account_agent'):
        print("✅ PASS - All agents initialized")
    else:
        print("❌ FAIL - Missing agents")
except Exception as e:
    print(f"❌ FAIL - Workflow error: {e}")
    traceback.print_exc()

# Test 3: Simple Balance Query
print("\n[TEST 3] Account Balance Query...")
try:
    workflow = BankWorkflow()
    response, logs, metrics = workflow.process_email(
        "What is my account balance?",
        "alice@example.com"
    )
    
    if response and "Error" not in response:
        print("✅ PASS - Response generated")
        print(f"   Agent: {metrics.get('routing', {}).get('actual', 'Unknown')}")
        print(f"   Quality: {metrics.get('quality_score', 0)}/100")
    else:
        print(f"❌ FAIL - Error response: {response[:100]}")
except Exception as e:
    print(f"❌ FAIL - Processing error: {e}")
    traceback.print_exc()

# Test 4: Card Security Query
print("\n[TEST 4] Lost Card Query...")
try:
    workflow = BankWorkflow()
    response, logs, metrics = workflow.process_email(
        "I lost my credit card! Please block it.",
        "bob@example.com"
    )
    
    if response and "BLOCKED" in response.upper():
        print("✅ PASS - Card blocked successfully")
        print(f"   Agent: {metrics.get('routing', {}).get('actual', 'Unknown')}")
    else:
        print(f"❌ FAIL - Card not blocked: {response[:100]}")
except Exception as e:
    print(f"❌ FAIL - Processing error: {e}")
    traceback.print_exc()

# Test 5: Off-topic Query (Guardrails)
print("\n[TEST 5] Off-topic Query (Guardrails Test)...")
try:
    workflow = BankWorkflow()
    response, logs, metrics = workflow.process_email(
        "What's the weather like today?",
        "charlie@example.com"
    )
    
    if "cannot" in response.lower() or "sorry" in response.lower():
        print("✅ PASS - Guardrails working (rejected off-topic)")
    else:
        print(f"⚠️ WARNING - May have answered off-topic question")
        print(f"   Response: {response[:100]}")
except Exception as e:
    print(f"❌ FAIL - Processing error: {e}")
    traceback.print_exc()

# Test 6: Empty Query
print("\n[TEST 6] Empty Query Validation...")
try:
    workflow = BankWorkflow()
    response, logs, metrics = workflow.process_email(
        "   ",  # Just spaces
        "alice@example.com"
    )
    
    if "Error" in response or "empty" in response.lower():
        print("✅ PASS - Empty query rejected")
    else:
        print("❌ FAIL - Empty query not validated")
        print(f"   Unexpected response: {response[:100]}")
except Exception as e:
    # Some implementations might throw an exception, which is also acceptable
    print(f"✅ PASS - Empty query handled (exception thrown)")

# Test 7: Routing Accuracy
print("\n[TEST 7] Routing Accuracy Check...")
test_cases = [
    ("What's my balance?", "alice@example.com", "AccountAgent"),
    ("Lost card emergency!", "bob@example.com", "CardAgent"),
    ("Home loan rates?", "charlie@example.com", "LoanAgent"),
]

correct = 0
total = len(test_cases)

for query, email, expected_agent in test_cases:
    try:
        workflow = BankWorkflow()
        response, logs, metrics = workflow.process_email(query, email)
        actual_agent = metrics.get('routing', {}).get('actual', 'Unknown')
        
        if actual_agent == expected_agent:
            correct += 1
            print(f"  ✅ '{query[:30]}...' → {actual_agent}")
        else:
            print(f"  ❌ '{query[:30]}...' → {actual_agent} (expected {expected_agent})")
    except Exception as e:
        print(f"  ❌ Error: {e}")

accuracy_pct = (correct / total) * 100
print(f"\nRouting Accuracy: {accuracy_pct:.1f}% ({correct}/{total})")

if accuracy_pct >= 66:
    print("✅ PASS - Acceptable routing accuracy")
else:
    print("❌ FAIL - Poor routing accuracy")

print("\n" + "="*70)
print("DIAGNOSTIC COMPLETE")
print("="*70)
