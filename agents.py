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

class CardAgent(Agent):
    def handle(self, email, customer, action_taken, status):
        # Tool use simulation
        # For a real agent, this would interact with a card system
        # For now, we just use the provided action_taken and status
        
        prompt = f"""
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

class LoanAgent(Agent):
    def handle(self, email, customer, credit_score):
        # Tool use simulation
        # For a real agent, this would interact with a loan system
        # For now, we just use the provided credit_score
        
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
        return self.think(prompt).strip()

class CardAgent(Agent):
    def handle(self, email, customer, action_taken, status):
        # Tool use simulation
        # For a real agent, this would interact with a card system
        # For now, we just use the provided action_taken and status
        
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
        return self.think(prompt).strip()
