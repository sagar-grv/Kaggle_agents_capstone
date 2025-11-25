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
        # Using gemini-2.5-flash (confirmed available in user's API key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def think(self, prompt):
        logs = []
        max_retries = 2  # Reduced from 3 to fail faster on free tier
        base_delay = 1   # Reduced from 2 to improve responsiveness
        
        for attempt in range(max_retries):
            try:
                # Log API call for visibility
                logs.append(f"🌐 API CALL: {self.name} ({self.role})")
                logs.append(f"📤 Sending request to Gemini API (Attempt {attempt + 1}/{max_retries})")
                logs.append(f"🤖 Model: {self.model.model_name}")
                
                start_time = time.time()
                
                response = self.model.generate_content(
                    f"You are a {self.role} at a bank. {prompt}"
                )
                
                duration = time.time() - start_time
                
                logs.append(f"✅ API Response received in {duration:.2f}s")
                logs.append(f"📥 Response length: {len(response.text)} characters")
                
                return response.text, logs
            except Exception as e:
                error_str = str(e)
                logs.append(f"❌ API Error: {error_str[:100]}...")
                
                if "429" in error_str or "ResourceExhausted" in error_str:
                    if attempt < max_retries - 1:
                        sleep_time = base_delay * (2 ** attempt)
                        logs.append(f"⏳ Rate limited. Retrying in {sleep_time}s...")
                        time.sleep(sleep_time)
                        continue
                    else:
                        return "System Notice: We are experiencing high traffic. Please try again in a moment. (Rate Limit Reached)", logs
                else:
                    return f"System Error: {error_str}", logs
        return "System Error: Unable to generate response.", logs

class TriageAgent(Agent):
    def rule_based_triage(self, email_content):
        """
        Fast, zero-cost routing based on strong keywords.
        Returns: (AgentName, Reason) or (None, None)
        """
        text = email_content.lower()
        
        # 1. CRITICAL SECURITY (CardAgent) - Highest Priority
        security_keywords = ["lost", "stolen", "fraud", "unauthorized", "block card", "hacked", "suspicious"]
        if any(kw in text for kw in security_keywords):
            return "CardAgent", "🔒 Rule Match: Security Keyword Detected"
            
        # 2. LOANS & CREDIT (LoanAgent)
        loan_keywords = ["loan", "mortgage", "interest rate", "credit score", "apply for", "lending"]
        if any(kw in text for kw in loan_keywords):
            return "LoanAgent", "🏠 Rule Match: Loan Keyword Detected"
            
        # 3. ACCOUNTS (AccountAgent)
        account_keywords = ["balance", "statement", "transaction", "checking", "savings", "deposit", "withdrawal"]
        if any(kw in text for kw in account_keywords):
            return "AccountAgent", "💰 Rule Match: Account Keyword Detected"
            
        return None, None

    def analyze_email(self, email_content):
        # PHASE 1: Fast Rule-Based Triage (Save API Call)
        agent_name, reason = self.rule_based_triage(email_content)
        if agent_name:
            # Return a fake log so the UI still shows what happened
            logs = [f"⚡ Triage: Fast-tracked to {agent_name} ({reason})"]
            return agent_name, logs

        # PHASE 2: LLM Fallback (For ambiguous queries)
        prompt = f"""
        You are the Triage Dispatcher for a bank. Your job is to route incoming emails to the correct specialist agent.
        
        Available Agents:
        1. CardAgent: Handles lost/stolen cards, fraud alerts, blocked cards, and travel notifications. PRIORITY: CRITICAL.
        2. LoanAgent: Handles loan applications, mortgage rates, credit scores, and lending inquiries.
        3. AccountAgent: Handles balance checks, transaction history, statement requests, and general account questions.
        
        Incoming Email: "{email_content}"
        
        Instructions:
        - Analyze the intent of the email.
        - CRITICAL RULE 1: If the email contains ANY mention of a lost card, stolen card, fraud, or unauthorized transaction, you MUST route to "CardAgent".
        - CRITICAL RULE 2: If the user asks to "apply" for anything or mentions "rates", "mortgage", or "credit score", route to "LoanAgent".
        - Output ONLY the name of the agent to route to (e.g., "CardAgent").
        - If the email is NOT related to banking (e.g., weather, sports, personal life, coding), output "None".
        """
        # Clean the response to ensure we just get the agent name
        response_text, logs = self.think(prompt)
        response = response_text.strip()
        
        # Fallback safety if LLM is chatty or doesn't follow format
        if "CardAgent" in response: return "CardAgent", logs
        if "LoanAgent" in response: return "LoanAgent", logs
        if "AccountAgent" in response: return "AccountAgent", logs
        if "None" in response: return "None", logs  # Preserve None for non-banking queries
        
        # If response is empty or unclear, default to AccountAgent
        if not response or len(response.strip()) == 0:
            return "AccountAgent", logs
        
        return "AccountAgent", logs  # Final fallback

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
        response_text, logs = self.think(prompt)
        return response_text.strip(), logs

