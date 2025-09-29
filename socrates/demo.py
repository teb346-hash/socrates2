#!/usr/bin/env python3
"""
Demonstration script for Socrates package
"""

import sys
import os
import time
import threading

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai.mock_ai import MockAIProvider


def demonstrate_ai_responses():
    """Demonstrate AI response generation"""
    print("🤖 Socrates AI Assistant Demo")
    print("=" * 50)
    
    ai = MockAIProvider()
    
    # Sample interview questions
    questions = [
        {
            "type": "Technical",
            "question": "Explain the difference between REST and GraphQL APIs"
        },
        {
            "type": "Behavioral", 
            "question": "Tell me about a time you had to work with a difficult team member"
        },
        {
            "type": "General",
            "question": "Why do you want to work at our company?"
        }
    ]
    
    for i, q in enumerate(questions, 1):
        print(f"\n📝 Question {i} ({q['type']}):")
        print(f"   {q['question']}")
        print("\n🤔 Thinking...")
        time.sleep(1)  # Simulate thinking time
        
        response = ai.get_response(q['question'])
        print(f"\n💡 AI Response:")
        print(f"   {response}")
        print("-" * 50)


def demonstrate_system_architecture():
    """Demonstrate system architecture"""
    print("\n🏗️  Socrates System Architecture")
    print("=" * 50)
    
    print("""
    📱 Frontend (frontzxcvPC)          🖥️  Backend (backqwerPC)
    ┌─────────────────────┐            ┌─────────────────────┐
    │  GUI Interface      │            │  Audio Recorder     │
    │  - Answer Display   │◄──────────►│  - Speaker Capture  │
    │  - Control Buttons  │   TCP      │  - AI Processing    │
    │  - Connection Status│   Socket   │  - Response Gen    │
    └─────────────────────┘            └─────────────────────┘
    
    🔄 Communication Flow:
    1. Frontend sends "START_RECORDING" command
    2. Backend captures speaker audio
    3. Frontend sends "STOP_RECORDING" command  
    4. Backend processes audio with AI
    5. Backend sends AI response to frontend
    6. Frontend displays answer to user
    """)


def demonstrate_usage():
    """Demonstrate usage commands"""
    print("\n🚀 Usage Commands")
    print("=" * 50)
    
    print("""
    On backqwerPC (Interview Computer):
    └─ socrates -b 8080 mypassword123
    
    On frontzxcvPC (Support Computer):  
    └─ socrates -f 192.168.1.100 8080 mypassword123
    
    🎯 Features:
    • Real-time audio recording from speakers
    • AI-powered response generation
    • Automatic reconnection handling
    • Keyboard shortcuts (Ctrl+R, Ctrl+S, Ctrl+G)
    • Mock AI mode for development/testing
    """)


if __name__ == "__main__":
    print("🎓 Socrates - AI-Powered Interview Assistant")
    print("=" * 60)
    
    demonstrate_ai_responses()
    demonstrate_system_architecture() 
    demonstrate_usage()
    
    print("\n✅ Demo completed!")
    print("📦 Package is ready for installation and use!")
