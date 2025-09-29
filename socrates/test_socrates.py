#!/usr/bin/env python3
"""
Test script for Socrates package
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from socrates.ai.mock_ai import MockAIProvider
from socrates.audio.recorder import AudioRecorder


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


def test_audio_recorder():
    """Test audio recorder (without actually recording)"""
    print("\nTesting Audio Recorder...")
    try:
        recorder = AudioRecorder()
        print("Audio recorder initialized successfully")
        
        # Test device detection
        device_info = recorder._find_output_device()
        if device_info:
            print(f"Found output device: {device_info['name']}")
        else:
            print("No output device found")
        
        recorder.cleanup()
        print("Audio recorder cleaned up")
        
    except Exception as e:
        print(f"Audio recorder test failed: {e}")


if __name__ == "__main__":
    print("Socrates Package Test")
    print("=" * 50)
    
    test_mock_ai()
    test_audio_recorder()
    
    print("\n" + "=" * 50)
    print("Test completed!")
