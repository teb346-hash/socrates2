"""
Backend server implementation for Socrates
"""

import socket
import threading
import time
import logging
import sys
import os
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from audio.recorder import AudioRecorder
from ai.mock_ai import MockAIProvider
from ai.openai_provider import OpenAIProvider


class BackendServer:
    """Backend server that runs on backqwerPC"""
    
    def __init__(self, port: int, password: str):
        self.port = port
        self.password = password
        self.socket: Optional[socket.socket] = None
        self.client_socket: Optional[socket.socket] = None
        self.running = False
        self.audio_recorder = AudioRecorder()
        
        # Try to use OpenAI provider, fallback to mock
        try:
            self.ai_provider = OpenAIProvider()
            self.logger.info("Using OpenAI provider")
        except Exception as e:
            self.logger.warning(f"OpenAI not available, using mock provider: {e}")
            self.ai_provider = MockAIProvider()
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def start(self):
        """Start the backend server"""
        self.running = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.socket.bind(('localhost', self.port))
            self.socket.listen(1)
            self.logger.info(f"Backend server listening on port {self.port}")
            
            while self.running:
                try:
                    self.logger.info("Waiting for frontend connection...")
                    self.client_socket, addr = self.socket.accept()
                    self.logger.info(f"Frontend connected from {addr}")
                    
                    # Handle client connection
                    self._handle_client()
                    
                except socket.error as e:
                    if self.running:
                        self.logger.error(f"Socket error: {e}")
                        time.sleep(1)
                        
        except Exception as e:
            self.logger.error(f"Server error: {e}")
        finally:
            self.stop()
    
    def _handle_client(self):
        """Handle client connection and messages"""
        try:
            # Send welcome message
            self._send_message("BACKEND_READY")
            
            while self.running and self.client_socket:
                try:
                    # Receive message from frontend
                    data = self.client_socket.recv(1024).decode('utf-8')
                    if not data:
                        break
                    
                    self.logger.info(f"Received: {data}")
                    self._process_message(data)
                    
                except socket.timeout:
                    continue
                except socket.error as e:
                    self.logger.error(f"Client communication error: {e}")
                    break
                    
        except Exception as e:
            self.logger.error(f"Client handling error: {e}")
        finally:
            if self.client_socket:
                self.client_socket.close()
                self.client_socket = None
    
    def _process_message(self, message: str):
        """Process incoming messages from frontend"""
        if message == "START_RECORDING":
            self._start_recording()
        elif message == "STOP_RECORDING":
            self._stop_recording()
        elif message == "GET_ANSWER":
            self._get_answer()
        elif message == "PING":
            self._send_message("PONG")
    
    def _start_recording(self):
        """Start recording audio from speakers"""
        try:
            self.audio_recorder.start_recording()
            self._send_message("RECORDING_STARTED")
            self.logger.info("Started recording")
        except Exception as e:
            self.logger.error(f"Failed to start recording: {e}")
            self._send_message("RECORDING_ERROR")
    
    def _stop_recording(self):
        """Stop recording and process audio"""
        try:
            audio_data = self.audio_recorder.stop_recording()
            self._send_message("RECORDING_STOPPED")
            self.logger.info("Stopped recording")
            
            # Process audio and get AI response
            if audio_data:
                self._process_audio(audio_data)
            
        except Exception as e:
            self.logger.error(f"Failed to stop recording: {e}")
            self._send_message("RECORDING_ERROR")
    
    def _process_audio(self, audio_data):
        """Process recorded audio and get AI response"""
        try:
            # For now, use mock AI response
            # In real implementation, this would transcribe audio and send to OpenAI
            response = self.ai_provider.get_response("Mock audio transcription")
            self._send_message(f"AI_RESPONSE:{response}")
            self.logger.info("Sent AI response")
            
        except Exception as e:
            self.logger.error(f"Failed to process audio: {e}")
            self._send_message("AI_ERROR")
    
    def _get_answer(self):
        """Get answer for current question"""
        try:
            response = self.ai_provider.get_response("Current question")
            self._send_message(f"AI_RESPONSE:{response}")
        except Exception as e:
            self.logger.error(f"Failed to get answer: {e}")
            self._send_message("AI_ERROR")
    
    def _send_message(self, message: str):
        """Send message to frontend"""
        if self.client_socket:
            try:
                self.client_socket.send(message.encode('utf-8'))
            except socket.error as e:
                self.logger.error(f"Failed to send message: {e}")
    
    def stop(self):
        """Stop the backend server"""
        self.running = False
        if self.client_socket:
            self.client_socket.close()
        if self.socket:
            self.socket.close()
        self.audio_recorder.cleanup()
        self.logger.info("Backend server stopped")
