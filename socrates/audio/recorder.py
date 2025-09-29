"""
Audio recording functionality for Socrates backend
"""

import pyaudio
import wave
import threading
import time
import logging
from typing import Optional, List
import io


class AudioRecorder:
    """Audio recorder for capturing speaker output"""
    
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.recording = False
        self.stream: Optional[pyaudio.Stream] = None
        self.frames: List[bytes] = []
        self.recording_thread: Optional[threading.Thread] = None
        
        # Audio settings
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 2  # Stereo
        self.rate = 44100
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
    
    def start_recording(self):
        """Start recording audio from speakers"""
        if self.recording:
            return
        
        try:
            # Find the default output device (speakers)
            device_info = self._find_output_device()
            if not device_info:
                raise Exception("No output device found")
            
            self.logger.info(f"Using output device: {device_info['name']}")
            
            # Open audio stream
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                input_device_index=device_info['index'],
                frames_per_buffer=self.chunk
            )
            
            self.recording = True
            self.frames = []
            
            # Start recording thread
            self.recording_thread = threading.Thread(target=self._record_audio, daemon=True)
            self.recording_thread.start()
            
            self.logger.info("Audio recording started")
            
        except Exception as e:
            self.logger.error(f"Failed to start recording: {e}")
            raise
    
    def stop_recording(self) -> Optional[bytes]:
        """Stop recording and return audio data"""
        if not self.recording:
            return None
        
        self.recording = False
        
        if self.recording_thread:
            self.recording_thread.join(timeout=2)
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        
        # Convert frames to audio data
        audio_data = b''.join(self.frames)
        self.logger.info(f"Recording stopped, captured {len(audio_data)} bytes")
        
        return audio_data
    
    def _record_audio(self):
        """Record audio in separate thread"""
        try:
            while self.recording and self.stream:
                data = self.stream.read(self.chunk, exception_on_overflow=False)
                self.frames.append(data)
                
        except Exception as e:
            self.logger.error(f"Recording error: {e}")
    
    def _find_output_device(self) -> Optional[dict]:
        """Find the default output device"""
        try:
            device_count = self.audio.get_device_count()
            
            for i in range(device_count):
                device_info = self.audio.get_device_info_by_index(i)
                
                # Look for output devices (maxOutputChannels > 0)
                if device_info['maxOutputChannels'] > 0:
                    # Prefer default output device
                    if device_info['name'].lower().find('speakers') != -1 or \
                       device_info['name'].lower().find('output') != -1:
                        return device_info
            
            # Fallback to default device
            default_device = self.audio.get_default_output_device_info()
            return default_device
            
        except Exception as e:
            self.logger.error(f"Error finding output device: {e}")
            return None
    
    def save_audio_to_file(self, audio_data: bytes, filename: str):
        """Save audio data to WAV file"""
        try:
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(self.format))
                wf.setframerate(self.rate)
                wf.writeframes(audio_data)
            
            self.logger.info(f"Audio saved to {filename}")
            
        except Exception as e:
            self.logger.error(f"Failed to save audio: {e}")
    
    def cleanup(self):
        """Cleanup audio resources"""
        if self.recording:
            self.stop_recording()
        
        if self.audio:
            self.audio.terminate()
        
        self.logger.info("Audio recorder cleaned up")
