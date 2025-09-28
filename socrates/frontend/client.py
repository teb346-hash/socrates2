"""
Frontend client implementation for Socrates
"""

import socket
import threading
import time
import logging
import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import Optional


class FrontendClient:
    """Frontend client that runs on frontzxcvPC"""
    
    def __init__(self, backend_ip: str, backend_port: int, password: str):
        self.backend_ip = backend_ip
        self.backend_port = backend_port
        self.password = password
        self.socket: Optional[socket.socket] = None
        self.running = False
        self.connected = False
        
        # GUI components
        self.root: Optional[tk.Tk] = None
        self.connection_label: Optional[ttk.Label] = None
        self.answer_text: Optional[scrolledtext.ScrolledText] = None
        self.start_button: Optional[ttk.Button] = None
        self.stop_button: Optional[ttk.Button] = None
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def start(self):
        """Start the frontend client"""
        self.running = True
        
        # Start GUI in main thread
        self._create_gui()
        
        # Start connection thread
        connection_thread = threading.Thread(target=self._connection_loop, daemon=True)
        connection_thread.start()
        
        # Start GUI main loop
        self.root.mainloop()
    
    def _create_gui(self):
        """Create the GUI interface"""
        self.root = tk.Tk()
        self.root.title("Socrates - AI Interview Assistant")
        self.root.geometry("600x400")
        
        # Connection status
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(status_frame, text="Connection Status:").pack(side=tk.LEFT)
        self.connection_label = ttk.Label(status_frame, text="Disconnected", foreground="red")
        self.connection_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Answer display
        answer_frame = ttk.LabelFrame(self.root, text="AI Response")
        answer_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.answer_text = scrolledtext.ScrolledText(answer_frame, height=15, wrap=tk.WORD)
        self.answer_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Control buttons
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.start_button = ttk.Button(control_frame, text="Start Recording", command=self._start_recording)
        self.start_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.stop_button = ttk.Button(control_frame, text="Stop Recording", command=self._stop_recording, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(control_frame, text="Get Answer", command=self._get_answer).pack(side=tk.LEFT, padx=(0, 5))
        
        # Keyboard shortcuts
        self.root.bind('<Control-r>', lambda e: self._start_recording())
        self.root.bind('<Control-s>', lambda e: self._stop_recording())
        self.root.bind('<Control-g>', lambda e: self._get_answer())
        
        # Update button states
        self._update_button_states()
    
    def _connection_loop(self):
        """Main connection loop"""
        while self.running:
            try:
                if not self.connected:
                    self._connect_to_backend()
                
                if self.connected and self.socket:
                    # Listen for messages from backend
                    try:
                        data = self.socket.recv(1024).decode('utf-8')
                        if not data:
                            self._disconnect()
                            continue
                        
                        self.logger.info(f"Received: {data}")
                        self._process_backend_message(data)
                        
                    except socket.timeout:
                        continue
                    except socket.error as e:
                        self.logger.error(f"Socket error: {e}")
                        self._disconnect()
                        
            except Exception as e:
                self.logger.error(f"Connection loop error: {e}")
                self._disconnect()
                time.sleep(2)  # Wait before reconnecting
    
    def _connect_to_backend(self):
        """Connect to backend server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(1.0)
            self.socket.connect((self.backend_ip, self.backend_port))
            
            # Wait for welcome message
            data = self.socket.recv(1024).decode('utf-8')
            if data == "BACKEND_READY":
                self.connected = True
                self._update_connection_status("Connected", "green")
                self.logger.info("Connected to backend")
            else:
                self._disconnect()
                
        except Exception as e:
            self.logger.error(f"Failed to connect: {e}")
            self._disconnect()
    
    def _disconnect(self):
        """Disconnect from backend"""
        self.connected = False
        if self.socket:
            self.socket.close()
            self.socket = None
        self._update_connection_status("Disconnected", "red")
        self._update_button_states()
    
    def _process_backend_message(self, message: str):
        """Process messages from backend"""
        if message.startswith("AI_RESPONSE:"):
            response = message[12:]  # Remove "AI_RESPONSE:" prefix
            self._display_answer(response)
        elif message == "RECORDING_STARTED":
            self._update_button_states()
            self._display_answer("Recording started...")
        elif message == "RECORDING_STOPPED":
            self._update_button_states()
            self._display_answer("Recording stopped, processing...")
        elif message == "RECORDING_ERROR":
            self._display_answer("Error: Recording failed")
        elif message == "AI_ERROR":
            self._display_answer("Error: AI processing failed")
        elif message == "PONG":
            pass  # Keep-alive response
    
    def _display_answer(self, answer: str):
        """Display AI answer in the GUI"""
        if self.answer_text:
            self.answer_text.insert(tk.END, f"{answer}\n\n")
            self.answer_text.see(tk.END)
    
    def _start_recording(self):
        """Send start recording command to backend"""
        if self.connected:
            self._send_message("START_RECORDING")
    
    def _stop_recording(self):
        """Send stop recording command to backend"""
        if self.connected:
            self._send_message("STOP_RECORDING")
    
    def _get_answer(self):
        """Send get answer command to backend"""
        if self.connected:
            self._send_message("GET_ANSWER")
    
    def _send_message(self, message: str):
        """Send message to backend"""
        if self.connected and self.socket:
            try:
                self.socket.send(message.encode('utf-8'))
            except socket.error as e:
                self.logger.error(f"Failed to send message: {e}")
                self._disconnect()
    
    def _update_connection_status(self, status: str, color: str):
        """Update connection status in GUI"""
        if self.connection_label:
            self.connection_label.config(text=status, foreground=color)
    
    def _update_button_states(self):
        """Update button states based on connection and recording status"""
        if self.start_button and self.stop_button:
            if self.connected:
                self.start_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.NORMAL)
            else:
                self.start_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.DISABLED)
    
    def stop(self):
        """Stop the frontend client"""
        self.running = False
        if self.socket:
            self.socket.close()
        if self.root:
            self.root.quit()
        self.logger.info("Frontend client stopped")
