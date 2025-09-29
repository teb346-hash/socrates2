# Socrates - AI-Powered Interview Assistant

A sophisticated Python package that provides real-time AI assistance during online interviews through distributed frontend and backend components.

## Installation

```bash
pip install socrates
```

## Usage

### Backend Server (on backqwerPC)

Start the backend server that handles audio recording and AI processing:

```bash
socrates -b [port] [password]
```

Example:
```bash
socrates -b 8080 mypassword123
```

### Frontend Client (on frontzxcvPC)

Start the frontend GUI client that connects to the backend:

```bash
socrates -f [backend_ip] [backend_port] [password]
```

Example:
```bash
socrates -f 192.168.1.100 8080 mypassword123
```

## Features

- **Real-time Audio Recording**: Captures speaker output for question analysis
- **AI-Powered Responses**: Uses OpenAI GPT models for intelligent answers
- **Distributed Architecture**: Frontend and backend run on separate computers
- **GUI Interface**: User-friendly interface for controlling the system
- **Automatic Reconnection**: Handles network disconnections gracefully
- **Mock AI Mode**: Works without OpenAI API for development/testing

## System Requirements

- Python 3.8 or higher
- Two computers with network connectivity
- Audio output device (speakers/headphones)
- Optional: OpenAI API key for real AI responses

## Configuration

### OpenAI API Key

For real AI responses, set your OpenAI API key:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

Without the API key, the system will use mock responses for testing.

## Keyboard Shortcuts (Frontend)

- `Ctrl+R`: Start recording
- `Ctrl+S`: Stop recording  
- `Ctrl+G`: Get answer

## Development

To run from source:

```bash
cd socrates
python -m socrates.cli -b 8080 password
python -m socrates.cli -f localhost 8080 password
```

## Architecture

- **Backend**: Handles audio recording, AI processing, and TCP server
- **Frontend**: Provides GUI interface and TCP client
- **Audio Module**: Manages speaker audio capture
- **AI Module**: Integrates with OpenAI API and provides mock responses

## Disclaimer

This tool is designed for educational and practice purposes. Users should ensure compliance with interview policies and ethical guidelines when using AI assistance tools.
