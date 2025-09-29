"""
Mock AI provider for development and testing
"""

import random
import time
import logging
from typing import List


class MockAIProvider:
    """Mock AI provider that simulates OpenAI responses"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Sample responses for different types of questions
        self.sample_responses = {
            "technical": [
                "Based on the question, here's a comprehensive technical answer that demonstrates deep understanding of the topic...",
                "This is a great technical question. Let me break it down into key components and provide a detailed explanation...",
                "From a technical perspective, the solution involves several important considerations that I'll outline step by step...",
            ],
            "behavioral": [
                "In my experience, I've encountered similar situations. Let me share a specific example and how I handled it...",
                "This is an excellent behavioral question. I'd like to use the STAR method to structure my response...",
                "I can relate to this scenario. Here's how I would approach this situation based on my past experiences...",
            ],
            "general": [
                "That's an interesting question. Let me provide a thoughtful response that addresses all aspects...",
                "I appreciate you asking this. Here's my perspective on this topic with supporting examples...",
                "This is a complex topic that requires careful consideration. Let me share my insights...",
            ]
        }
    
    def get_response(self, question: str) -> str:
        """Get AI response for a given question"""
        try:
            # Simulate processing time
            time.sleep(random.uniform(0.5, 2.0))
            
            # Determine response type based on question content
            response_type = self._classify_question(question)
            
            # Get random response from appropriate category
            responses = self.sample_responses.get(response_type, self.sample_responses["general"])
            response = random.choice(responses)
            
            # Add some variation
            response = self._add_variation(response)
            
            self.logger.info(f"Generated mock response for {response_type} question")
            return response
            
        except Exception as e:
            self.logger.error(f"Error generating mock response: {e}")
            return "I apologize, but I'm having trouble processing that question right now. Could you please rephrase it?"
    
    def _classify_question(self, question: str) -> str:
        """Classify question type based on content"""
        question_lower = question.lower()
        
        technical_keywords = [
            "algorithm", "code", "programming", "software", "system", "database",
            "api", "framework", "architecture", "performance", "optimization",
            "debug", "test", "deploy", "server", "client", "frontend", "backend"
        ]
        
        behavioral_keywords = [
            "experience", "situation", "challenge", "team", "conflict", "leadership",
            "problem", "solution", "learn", "mistake", "success", "failure",
            "collaborate", "communicate", "manage", "prioritize"
        ]
        
        # Count keyword matches
        technical_count = sum(1 for keyword in technical_keywords if keyword in question_lower)
        behavioral_count = sum(1 for keyword in behavioral_keywords if keyword in question_lower)
        
        if technical_count > behavioral_count:
            return "technical"
        elif behavioral_count > 0:
            return "behavioral"
        else:
            return "general"
    
    def _add_variation(self, response: str) -> str:
        """Add variation to make responses more realistic"""
        variations = [
            "Let me think about this... ",
            "That's a great question. ",
            "I'd be happy to share my thoughts on this. ",
            "This is something I've thought about before. ",
        ]
        
        # Randomly add variation prefix
        if random.random() < 0.3:
            prefix = random.choice(variations)
            response = prefix + response.lower()
        
        # Add random follow-up
        follow_ups = [
            " Does this help clarify the concept?",
            " Would you like me to elaborate on any specific aspect?",
            " I hope this provides a good foundation for understanding.",
            " Let me know if you need more details on any part.",
        ]
        
        if random.random() < 0.4:
            follow_up = random.choice(follow_ups)
            response += follow_up
        
        return response
    
    def get_contextual_response(self, context: str, question: str) -> str:
        """Get response considering context"""
        # For mock purposes, just use regular response
        return self.get_response(question)
    
    def is_available(self) -> bool:
        """Check if AI service is available"""
        return True  # Mock is always available
