"""
BankAssist Agent System
========================

Implements specialized agents for handling different types of banking customer inquiries.
Each agent is powered by Google Gemini Flash with retry logic and rate limit handling.

Agent Roles:
------------
1. TriageAgent: Routes emails to the correct specialist based on content analysis
2. AccountAgent: Handles account-related queries (balance, transactions, statements)
3. CardAgent: Manages card security issues (lost/stolen cards, fraud alerts)
4. LoanAgent: Processes loan applications and credit inquiries
5. AuditorAgent: Reviews all responses for compliance and quality

LLM Guardrails (Recent Enhancement):
-------------------------------------
All specialist agents now include strict guardrails to reject off-topic questions:
- AccountAgent: Only answers banking services questions
- CardAgent: Only handles card security matters
- LoanAgent: Only processes loan/credit inquiries

Non-banking questions (weather, sports, etc.) receive polite rejection messages
directing users to appropriate support channels.

Error Handling:
---------------
- 429/ResourceExhausted: Exponential backoff retry (max 3 attempts)
- Generic errors: Gracefully return error message to user
- Rate limiting: User-friendly timeout messages

Author: BankAssist Team
"""

import os
import time
import google.generativeai as genai

def configure_genai(api_key):
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

# Configuration is now handled explicitly in app.py
# No implicit loading from environment variables to prevent persistence issues

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
        - Output ONLY the name of the agent to route to (e.g., "CardAgent").
        - If the email is NOT related to banking (e.g., weather, sports, personal life, coding), output "None".
        """
        # Clean the response to ensure we just get the agent name
        response = self.think(prompt).strip()
        
        # Fallback safety if LLM is chatty or doesn't follow format
        if "CardAgent" in response: return "CardAgent"
        if "LoanAgent" in response: return "LoanAgent"
        if "AccountAgent" in response: return "AccountAgent"
        if "None" in response or not response: return "AccountAgent"  # Default for unclear queries
        
        return "AccountAgent"  # Final fallback

class AccountAgent(Agent):
    def handle(self, email, customer):
        # Tool use simulation
        balance = self.db.get_balance(customer[0])
        txns = self.db.get_recent_transactions(customer[0])
        
        # Use Gemini to generate a nice response
        prompt = f"""
        You are an Account Manager at BankAssist.
        
        CRITICAL GUARDRAIL: You MUST ONLY answer questions related to banking services (accounts, balances, transactions, statements). 
        If the customer asks about ANYTHING ELSE (weather, sports, general knowledge, etc.), respond EXACTLY with:
        "I apologize, but I can only assist with banking-related inquiries. For your question, please contact our general support line."
        
        Customer Details:
        - Name: {customer[1]}
        - Account Balance: {balance}
        - Recent Transactions: {txns}
        
        Customer Email: "{email}"
        
        Task: Write a helpful, professional email response ONLY if the question is banking-related.
        - Answer their specific question using the data above.
        - Be concise but warm.
        - Sign off as "BankAssist Support Team".
        """
        return self.think(prompt)

class CardAgent(Agent):
    def handle(self, email, customer):
        # Action simulation
        action_taken = "None"
        email_lower = email.lower()
        
        # We still need some "logic" to trigger the DB action, but the response is LLM
        if any(w in email_lower for w in ["lost", "stolen", "fraud", "unauthorized"]):
            self.db.block_card(customer[0])
            action_taken = "BLOCKED CARD ending in ..."
        
        status = self.db.get_card_status(customer[0])
        
        prompt = f"""
        You are a Security Officer at BankAssist handling card security issues.
        
        CRITICAL GUARDRAIL: You MUST ONLY answer questions related to card security (lost/stolen cards, fraud, unauthorized transactions).
        If the customer asks about ANYTHING ELSE, respond EXACTLY with:
        "I apologize, but my role is specifically limited to card security matters. For other inquiries, please contact our general support."
        
        Customer: {customer[1]}
        System Action Taken: {action_taken}
        Current Card Status: {status}
        
        Customer Email: "{email}"
        
        Task: Handle this security concern professionally and urgently ONLY if it's card-related.
        - If the card was blocked, confirm it clearly and instruct them to visit a branch for replacement.
        - If this was just a travel notice or inquiry, acknowledge it.
        - Prioritize safety and clarity.
        - Sign off as "BankAssist Security Team".
        """
        return self.think(prompt)

class LoanAgent(Agent):
    def handle(self, email, customer):
        # Simulation: In a real app, we'd check credit score, etc.
        credit_score = customer[4] * 10 + 300 # Mock credit score based on risk score
        
        prompt = f"""
        You are a Loan Specialist at BankAssist.
        
        CRITICAL GUARDRAIL: You MUST ONLY answer questions related to loans, mortgages, credit, and financing.
        If the customer asks about ANYTHING ELSE, respond EXACTLY with:
        "I apologize, but I specialize only in loan and credit services. For other banking needs, please contact our general support."
        
        Customer: {customer[1]}
        Estimated Credit Score: {credit_score}
        
        Customer Email: "{email}"
        
        Task: Write a helpful email regarding their loan inquiry ONLY if it's loan-related.
        - If they are asking for rates, provide current mock rates (e.g., Mortgage 6.5%, Personal 8%).
        - If they are asking for approval, explain that a formal application is needed but their score looks { 'promising' if credit_score > 700 else 'like it needs review' }.
        - Be professional and encouraging.
        - Sign off as "BankAssist Loan Department".
        """
        return self.think(prompt)

class AuditorAgent(Agent):
    def review(self, draft_response):
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

