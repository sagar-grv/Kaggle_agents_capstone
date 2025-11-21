import os
import time
import google.generativeai as genai

def configure_genai(api_key):
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

# Try to configure from env immediately if available
if os.environ.get("GOOGLE_API_KEY"):
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

class Agent:
    def __init__(self, name, role, db):
        self.name = name
        self.role = role
        self.db = db
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def think(self, prompt):
        max_retries = 3
        base_delay = 2
        
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(
                    f"You are a {self.role} at a bank. {prompt}"
                )
                return response.text
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "ResourceExhausted" in error_str:
                    if attempt < max_retries - 1:
                        sleep_time = base_delay * (2 ** attempt)
                        time.sleep(sleep_time)
                        continue
                    else:
                        return "System Notice: We are experiencing high traffic. Please try again in a moment. (Rate Limit Reached)"
                else:
                    return f"System Error: {error_str}"
        return "System Error: Unable to generate response."

class TriageAgent(Agent):
    def analyze_email(self, email_content):
        prompt = f"""
        You are the Triage Dispatcher for a bank. Your job is to route incoming emails to the correct specialist agent.
        
        Available Agents:
        1. CardAgent: Handles lost/stolen cards, fraud alerts, blocked cards, and travel notifications. PRIORITY: CRITICAL.
        2. LoanAgent: Handles loan applications, mortgage rates, and credit inquiries.
        3. AccountAgent: Handles balance checks, transaction history, statement requests, and general account questions.
        
        Incoming Email: "{email_content}"
        
        Instructions:
        - Analyze the intent of the email.
        - CRITICAL RULE: If the email contains ANY mention of a lost card, stolen card, fraud, or unauthorized transaction, you MUST route to "CardAgent", even if the user also asks about their balance or other topics. Security is the #1 priority.
        - Output ONLY the name of the agent to route to (e.g., "CardAgent"). Do not add any other text.
        """
        # Clean the response to ensure we just get the agent name
        response = self.think(prompt).strip()
        
        # Fallback safety if LLM is chatty
        if "CardAgent" in response: return "CardAgent"
        if "LoanAgent" in response: return "LoanAgent"
        if "AccountAgent" in response: return "AccountAgent"
        
        return "AccountAgent" # Default fallback

class AccountAgent(Agent):
    def handle(self, email, customer):
        # Tool use simulation
        balance = self.db.get_balance(customer[0])
        prompt = f"""
        You are a strict Bank Compliance Officer. Review the draft email response below.
        
        Draft Response:
        "{draft_response}"
        
        Compliance Rules:
        1. NO false promises (e.g., "I guarantee", "I promise").
        2. NO unprofessional language.
        3. IF the email mentions a "blocked card", it MUST advise the customer on next steps (e.g., visit branch, call support).
        4. The tone must be professional and empathetic.
        
        Task:
        - If the email is compliant, output exactly: "APPROVED"
        - If not, output "REJECTED: [Reason]"
        """
        return self.think(prompt).strip()

