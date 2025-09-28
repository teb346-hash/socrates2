#!/usr/bin/env python3
"""
Simple test script for Socrates package components
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai.mock_ai import MockAIProvider


def test_mock_ai():
    """Test mock AI provider"""
    print("Testing Mock AI Provider...")
    ai = MockAIProvider()
    
    test_questions = [
        "What is object-oriented programming?",
        "Tell me about a time you faced a difficult challenge",
        "How do you handle team conflicts?"
    ]
    
    for question in test_questions:
        print(f"\nQuestion: {question}")
        response = ai.get_response(question)
        print(f"Response: {response}")


if __name__ == "__main__":
    print("Socrates Package Component Test")
    print("=" * 50)
    
    test_mock_ai()
    
    print("\n" + "=" * 50)
    print("Test completed!")
