"""
BankWorkflow - Email Processing Orchestration
==============================================

Orchestrates the complete email processing pipeline through the multi-agent system.

Pipeline Stages:
----------------
1. Customer Identification: Look up customer in database by email
2. Triage: Route email to appropriate specialist agent
3. Execution: Specialist agent generates draft response
4. Audit: Compliance check by AuditorAgent
5. Evaluation: Track metrics (routing, quality, compliance, latency)
6. Response: Return final response with logs and metrics

Integration with Evaluation System:
------------------------------------
- Tracks routing accuracy for each request
- Measures response quality (0-100 score)
- Monitors compliance rates (APPROVED vs REJECTED)
- Records latency for performance analysis
- Logs detailed interaction history

Return Values:
--------------
- final_response: Email response text to send to customer
- logs: List of processing steps for transparency
- eval_metrics: Dictionary containing:
  - routing: {expected, actual, is_correct, accuracy}
  - compliance: {status, compliance_rate}
  - quality_score: 0-100
  - duration: Processing time in seconds

Author: BankAssist Team
"""

from agents import TriageAgent, AccountAgent, CardAgent, AuditorAgent, LoanAgent
from bank_system import BankDatabase
from evaluation import AgentEvaluator
import time

class BankWorkflow:
    def __init__(self):
        self.db = BankDatabase()
        self.triage = TriageAgent("Dispatcher", "Triage", self.db)
        self.account_agent = AccountAgent("Bob", "Account Manager", self.db)
        self.card_agent = CardAgent("Charlie", "Security Officer", self.db)
        self.loan_agent = LoanAgent("Diana", "Loan Specialist", self.db)
        self.auditor = AuditorAgent("Smith", "Compliance", self.db)
        self.evaluator = AgentEvaluator()  # Initialize evaluator

    def process_email(self, email_content, user_email):
        logs = []
        start_time = time.time()
        
        # 1. Identify Customer
        customer = self.db.get_customer_by_email(user_email)
        if not customer:
            return "Error: Customer not found.", ["Lookup failed"], {}
        
        logs.append(f"✅ Identified Customer: {customer[1]} (Risk Score: {customer[4]})")

        # 2. Triage
        target_agent_name = self.triage.analyze_email(email_content)
        logs.append(f"🔀 Triage: Routing to {target_agent_name}")

        # Evaluate Routing
        routing_eval = self.evaluator.evaluate_routing(email_content, target_agent_name)
        logs.append(f"📊 Routing Evaluation: {'✅ Correct' if routing_eval['is_correct'] else '⚠️ Mismatch'} (Expected: {routing_eval['expected']})")

        # 3. Execution
        draft_response = ""
        if target_agent_name == "CardAgent":
            draft_response = self.card_agent.handle(email_content, customer)
        elif target_agent_name == "AccountAgent":
            draft_response = self.account_agent.handle(email_content, customer)
        elif target_agent_name == "LoanAgent":
            draft_response = self.loan_agent.handle(email_content, customer)
        else:
            draft_response = "I am not sure how to help with that yet."
        
        logs.append(f"⚙️ {target_agent_name} generated draft.")

        # 4. Audit
        audit_result = self.auditor.review(draft_response)
        logs.append(f"⚖️ Auditor Verdict: {audit_result}")

        # Evaluate Compliance
        compliance_eval = self.evaluator.evaluate_compliance(audit_result)
        
        # Update agent-specific compliance stats
        if compliance_eval['status'] == 'APPROVED':
            self.evaluator.metrics['agent_stats'][target_agent_name]['compliance_pass'] += 1
        else:
            self.evaluator.metrics['agent_stats'][target_agent_name]['compliance_fail'] += 1

        if "REJECTED" in audit_result:
            final_response = "Your request is being reviewed by a human manager."
        else:
            final_response = draft_response

        # Calculate latency
        duration = time.time() - start_time
        self.evaluator.track_latency(target_agent_name, duration)
        
        # Evaluate Response Quality
        quality_score = self.evaluator.evaluate_response_quality(final_response, target_agent_name)
        logs.append(f"⭐ Quality Score: {quality_score}/100")
        
        # Log full interaction
        self.evaluator.log_interaction(
            email_content, target_agent_name, final_response,
            duration, routing_eval, compliance_eval, quality_score
        )
        
        # Return response, logs, AND evaluation metrics
        eval_metrics = {
            'routing': routing_eval,
            'compliance': compliance_eval,
            'quality_score': quality_score,
            'duration': duration
        }

        return final_response, logs, eval_metrics
