"""
Agent Evaluation Module
Implements comprehensive evaluation metrics for the BankAssist multi-agent system.
Inspired by Google's Agents Development Kit (ADK) evaluation functions.
"""

import time
from collections import defaultdict
from datetime import datetime


class AgentEvaluator:
    """
    Evaluates agent system performance using ADK-style metrics:
    - Routing Accuracy
    - Response Quality
    - Compliance Rate
    - Latency Tracking
    - Per-Agent Performance
    """
    
    def __init__(self):
        self.metrics = {
            'total_requests': 0,
            'routing_attempts': 0,
            'routing_correct': 0,
            'compliance_approved': 0,
            'compliance_rejected': 0,
            'response_times': [],
            'quality_scores': [],
            'agent_stats': defaultdict(lambda: {
                'requests': 0,
                'avg_time': 0,
                'compliance_pass': 0,
                'compliance_fail': 0,
                'total_time': 0
            })
        }
        self.interaction_log = []
    
    def evaluate_routing(self, email_content, routed_agent):
        """
        Evaluate routing accuracy by checking if agent matches expected intent.
        Uses keyword-based ground truth for validation.
        """
        self.metrics['routing_attempts'] += 1
        
        # Ground truth determination
        email_lower = email_content.lower()
        expected_agent = None
        
        # Security keywords (highest priority)
        security_keywords = ['lost', 'stolen', 'fraud', 'unauthorized', 'suspicious', 'hacked', 'compromised']
        if any(kw in email_lower for kw in security_keywords):
            expected_agent = 'CardAgent'
        # Loan keywords
        elif any(kw in email_lower for kw in ['loan', 'mortgage', 'credit', 'borrow', 'financing', 'rate']):
            expected_agent = 'LoanAgent'
        # Account keywords
        elif any(kw in email_lower for kw in ['balance', 'transaction', 'account', 'statement', 'deposit', 'withdrawal']):
            expected_agent = 'AccountAgent'
        else:
            expected_agent = 'AccountAgent'  # Default
        
        is_correct = (routed_agent == expected_agent)
        
        if is_correct:
            self.metrics['routing_correct'] += 1
        
        return {
            'expected': expected_agent,
            'actual': routed_agent,
            'is_correct': is_correct,
            'accuracy': (self.metrics['routing_correct'] / self.metrics['routing_attempts']) * 100
        }
    
    def evaluate_response_quality(self, response, agent_type):
        """
        Score response quality (0-100) based on:
        - Length appropriateness (20 points)
        - Professional tone indicators (30 points)
        - Information richness (30 points)
        - Structure and formatting (20 points)
        """
        score = 0
        
        # 1. Length Check (20 points)
        word_count = len(response.split())
        if 50 <= word_count <= 300:
            score += 20
        elif 30 <= word_count < 50 or 300 < word_count <= 500:
            score += 15
        elif word_count < 30:
            score += 5
        else:
            score += 10
        
        # 2. Professional Tone (30 points)
        professional_indicators = ['dear', 'thank you', 'sincerely', 'regards', 'please', 'appreciate']
        tone_score = sum(2 for indicator in professional_indicators if indicator.lower() in response.lower())
        score += min(tone_score, 30)
        
        # 3. Information Richness (30 points)
        info_indicators = ['$', 'account', 'card', 'transaction', 'balance', 'customer', 'security', 'loan', 'rate']
        info_score = sum(3 for indicator in info_indicators if indicator.lower() in response.lower())
        score += min(info_score, 30)
        
        # 4. Structure (20 points)
        has_subject = 'subject:' in response.lower()
        has_greeting = any(g in response.lower() for g in ['dear', 'hello', 'hi'])
        has_closing = any(c in response.lower() for c in ['sincerely', 'regards', 'best', 'team'])
        
        structure_score = (has_subject * 7) + (has_greeting * 7) + (has_closing * 6)
        score += structure_score
        
        self.metrics['quality_scores'].append(score)
        
        return min(score, 100)  # Cap at 100
    
    def evaluate_compliance(self, auditor_result):
        """
        Track compliance rate based on Auditor verdicts.
        """
        self.metrics['total_requests'] += 1
        
        if 'APPROVED' in auditor_result:
            self.metrics['compliance_approved'] += 1
            return {
                'status': 'APPROVED',
                'compliance_rate': (self.metrics['compliance_approved'] / self.metrics['total_requests']) * 100
            }
        else:
            self.metrics['compliance_rejected'] += 1
            return {
                'status': 'REJECTED',
                'compliance_rate': (self.metrics['compliance_approved'] / self.metrics['total_requests']) * 100,
                'reason': auditor_result
            }
    
    def track_latency(self, agent_name, duration):
        """
        Track response time latency for performance monitoring.
        """
        self.metrics['response_times'].append(duration)
        
        # Update agent-specific stats
        agent_stat = self.metrics['agent_stats'][agent_name]
        agent_stat['total_time'] += duration
        agent_stat['requests'] += 1
        agent_stat['avg_time'] = agent_stat['total_time'] / agent_stat['requests']
    
    def log_interaction(self, email, agent, response, duration, routing_eval, compliance_eval, quality_score):
        """
        Log detailed interaction for analysis.
        """
        self.interaction_log.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'email_snippet': email[:50] + '...',
            'agent': agent,
            'routing_correct': routing_eval['is_correct'],
            'expected_agent': routing_eval['expected'],
            'compliance': compliance_eval['status'],
            'quality_score': quality_score,
            'latency': round(duration, 2)
        })
    
    def get_agent_performance_breakdown(self):
        """
        Return detailed per-agent performance metrics.
        """
        performance = []
        for agent_name, stats in self.metrics['agent_stats'].items():
            if stats['requests'] > 0:
                compliance_rate = (stats['compliance_pass'] / stats['requests']) * 100 if stats['requests'] > 0 else 0
                performance.append({
                    'agent': agent_name,
                    'requests': stats['requests'],
                    'avg_latency': round(stats['avg_time'], 2),
                    'compliance_rate': round(compliance_rate, 1)
                })
        return performance
    
    def get_summary_metrics(self):
        """
        Returns summary metrics for dashboard display.
        """
        routing_accuracy = (self.metrics['routing_correct'] / self.metrics['routing_attempts'] * 100) if self.metrics['routing_attempts'] > 0 else 0
        compliance_rate = (self.metrics['compliance_approved'] / self.metrics['total_requests'] * 100) if self.metrics['total_requests'] > 0 else 0
        avg_quality = sum(self.metrics['quality_scores']) / len(self.metrics['quality_scores']) if self.metrics['quality_scores'] else 0
        avg_latency = sum(self.metrics['response_times']) / len(self.metrics['response_times']) if self.metrics['response_times'] else 0
        
        return {
            'routing_accuracy': round(routing_accuracy, 1),
            'compliance_rate': round(compliance_rate, 1),
            'avg_quality_score': round(avg_quality, 1),
            'avg_latency': round(avg_latency, 2),
            'total_evaluations': self.metrics['total_requests']
        }
