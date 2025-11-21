from agents import TriageAgent, AccountAgent, CardAgent, AuditorAgent, LoanAgent
from bank_system import BankDatabase

class BankWorkflow:
    def __init__(self):
        self.db = BankDatabase()
        self.triage = TriageAgent("Dispatcher", "Triage", self.db)
        self.account_agent = AccountAgent("Bob", "Account Manager", self.db)
        self.card_agent = CardAgent("Charlie", "Security Officer", self.db)
        self.loan_agent = LoanAgent("Diana", "Loan Specialist", self.db)
        self.auditor = AuditorAgent("Smith", "Compliance", self.db)

    def process_email(self, email_content, user_email):
        logs = []
        
        # 1. Identify Customer
        customer = self.db.get_customer_by_email(user_email)
        if not customer:
            return "Error: Customer not found.", ["Lookup failed"]
        
        logs.append(f"✅ Identified Customer: {customer[1]} (Risk Score: {customer[4]})")

        # 2. Triage
        target_agent_name = self.triage.analyze_email(email_content)
        logs.append(f"🔀 Triage: Routing to {target_agent_name}")

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

        if "REJECTED" in audit_result:
            final_response = "Your request is being reviewed by a human manager."
        else:
            final_response = draft_response

        return final_response, logs
