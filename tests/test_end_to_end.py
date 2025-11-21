import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import google.generativeai as genai

# IMPORTANT: Set your API key before running this test
# Option 1: Set environment variable GOOGLE_API_KEY
# Option 2: Uncomment the lines below and add your key
# api_key = "YOUR_API_KEY_HERE"
# os.environ["GOOGLE_API_KEY"] = api_key
# genai.configure(api_key=api_key)

from workflow import BankWorkflow
import time

# Logging setup
log_file = open("test_results_internal.txt", "w", encoding="utf-8")

def log(message):
    print(message)
    log_file.write(message + "\n")
    log_file.flush()

def run_test(name, email, user_email, expected_agent):
    log(f"\n🔹 TEST: {name}")
    log(f"   Email: \"{email}\"")
    
    workflow = BankWorkflow()
    start_time = time.time()
    response, logs = workflow.process_email(email, user_email)
    duration = time.time() - start_time
    
    # Extract Triage Decision
    triage_log = next((log for log in logs if "Triage:" in log), "No Triage Log")
    routed_agent = triage_log.split("Routing to ")[-1] if "Routing to " in triage_log else "Unknown"
    
    # Extract Auditor Decision
    auditor_log = next((log for log in logs if "Auditor Verdict:" in log), "No Audit Log")
    
    log(f"   ⏱️ Time: {duration:.2f}s")
    log(f"   🔀 Routed To: {routed_agent}")
    log(f"   ⚖️ Auditor: {auditor_log}")
    log(f"   ✉️ Response Snippet: {response[:100]}...")
    
    # Validation
    if expected_agent in routed_agent:
        log("   ✅ Routing Correct")
    else:
        log(f"   ❌ Routing FAILED (Expected {expected_agent}, got {routed_agent})")
        
    if "APPROVED" in auditor_log:
        log("   ✅ Compliance Passed")
    else:
        log(f"   ⚠️ Compliance Flagged: {auditor_log}")

    return response

log("="*60)
log("🤖 INTELLIGENT AGENT SYSTEM - END-TO-END VERIFICATION")
log("="*60)

# Scenario 1: Complex Intent (Lost Card + Balance)
run_test(
    "Complex Intent Prioritization", 
    "I lost my credit card at the airport! Also what is my checking balance?", 
    "alice@example.com", 
    "CardAgent"
)

# Scenario 2: Simple Inquiry
run_test(
    "Simple Balance Check", 
    "Can you tell me how much money I have?", 
    "alice@example.com", 
    "AccountAgent"
)

# Scenario 3: Ambiguous/Security
run_test(
    "Fraud Suspicion", 
    "I see a transaction I didn't make.", 
    "bob@example.com", 
    "CardAgent"
)

# Scenario 4: Loan Inquiry
run_test(
    "Loan Inquiry", 
    "What are your current mortgage rates?", 
    "charlie@example.com", 
    "LoanAgent"
)

log_file.close()
