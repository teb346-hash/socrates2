"""
CLI interface for Socrates package
"""

import argparse
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.server import BackendServer
from frontend.client import FrontendClient


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Socrates - AI-Powered Interview Assistant",
        prog="socrates"
    )
    
    subparsers = parser.add_subparsers(dest="mode", help="Run mode")
    
    # Backend mode
    backend_parser = subparsers.add_parser(
        "-b", 
        help="Run backend server",
        description="Start the backend server on backqwerPC"
    )
    backend_parser.add_argument("port", type=int, help="Port to listen on")
    backend_parser.add_argument("password", help="Connection password")
    
    # Frontend mode  
    frontend_parser = subparsers.add_parser(
        "-f",
        help="Run frontend client", 
        description="Start the frontend client on frontzxcvPC"
    )
    frontend_parser.add_argument("backend_ip", help="Backend server IP address")
    frontend_parser.add_argument("backend_port", type=int, help="Backend server port")
    frontend_parser.add_argument("password", help="Connection password")
    
    args = parser.parse_args()
    
    if args.mode == "-b":
        # Start backend server
        server = BackendServer(args.port, args.password)
        try:
            server.start()
        except KeyboardInterrupt:
            print("\nShutting down backend server...")
            server.stop()
    elif args.mode == "-f":
        # Start frontend client
        client = FrontendClient(args.backend_ip, args.backend_port, args.password)
        try:
            client.start()
        except KeyboardInterrupt:
            print("\nShutting down frontend client...")
            client.stop()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
