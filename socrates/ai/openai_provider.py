"""
OpenAI integration for Socrates
"""

import openai
import logging
from typing import Optional
import os


class OpenAIProvider:
    """OpenAI API provider for real AI responses"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        
        # Get API key from environment or parameter
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        # Initialize OpenAI client
        openai.api_key = self.api_key
        self.client = openai.OpenAI(api_key=self.api_key)
        
        # System prompt for interview assistance
        self.system_prompt = """You are an AI assistant helping a candidate during an interview. 
        Provide clear, concise, and professional responses that help the candidate answer questions effectively.
        Focus on:
        - Technical accuracy
        - Clear explanations
        - Professional tone
        - Structured responses
        - Relevant examples when appropriate
        
        Keep responses concise but comprehensive. Avoid overly long explanations unless specifically requested."""
    
    def get_response(self, question: str, context: Optional[str] = None) -> str:
        """Get AI response for a given question"""
        try:
            # Prepare messages
            messages = [{"role": "system", "content": self.system_prompt}]
            
            if context:
                messages.append({"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"})
            else:
                messages.append({"role": "user", "content": question})
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7,
                timeout=30
            )
            
            answer = response.choices[0].message.content.strip()
            self.logger.info("Generated OpenAI response")
            return answer
            
        except Exception as e:
            self.logger.error(f"Error getting OpenAI response: {e}")
            return f"I apologize, but I'm having trouble processing that question right now. Error: {str(e)}"
    
    def get_contextual_response(self, context: str, question: str) -> str:
        """Get response considering context"""
        return self.get_response(question, context)
    
    def transcribe_audio(self, audio_file_path: str) -> str:
        """Transcribe audio file to text"""
        try:
            with open(audio_file_path, 'rb') as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            
            self.logger.info("Audio transcribed successfully")
            return transcript.strip()
            
        except Exception as e:
            self.logger.error(f"Error transcribing audio: {e}")
            return f"Error transcribing audio: {str(e)}"
    
    def is_available(self) -> bool:
        """Check if OpenAI service is available"""
        try:
            # Simple test call
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1,
                timeout=5
            )
            return True
        except Exception as e:
            self.logger.error(f"OpenAI service unavailable: {e}")
            return False
