#!/usr/bin/env python3
# main.py - Main entry point for the customer support AI system

import argparse
import os
import sys
from tests.test_conversational_loop import test_interactive_conversation_loop
from workflows.support_workflow import SupportWorkflow
from workflows.crewai_workflow import process_file

def main():
    """
    Main entry point for the customer support AI system.
    Provides a command-line interface for running the system in different modes.
    """
    parser = argparse.ArgumentParser(
        description="Customer Support AI - Multi-Agent Support System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run in interactive mode
  python main.py --interactive
  
  # Process a conversation file
  python main.py --file data/conversations/Network_Connectivity_Issue.txt
  
  # Run the API server
  python main.py --api
        """
    )
    
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--interactive", "-i", action="store_true", 
                           help="Run in interactive conversation mode")
    mode_group.add_argument("--file", "-f", type=str, 
                           help="Process a conversation file")
    mode_group.add_argument("--api", "-a", action="store_true", 
                           help="Start the API server")
    
    parser.add_argument("--debug", "-d", action="store_true",
                       help="Enable debug mode with additional logging")
    
    args = parser.parse_args()
    
    # Set up debug mode if requested
    if args.debug:
        print("🐛 Debug mode enabled")
        # You could set up logging configuration here
    
    # Run in the selected mode
    if args.interactive:
        print("🤖 Starting interactive conversation mode...")
        test_interactive_conversation_loop()
    
    elif args.file:
        if not os.path.exists(args.file):
            print(f"❌ Error: File not found: {args.file}")
            return 1
            
        print(f"📄 Processing conversation file: {args.file}")
        result = process_file(args.file)
        
        # Display the result
        if isinstance(result, dict):
            print("\n📦 Support Response:")
            print(f"Reply: {result.get('reply', '')}")
            print(f"Status: {result.get('status', '')}")
            
            if result.get('status') == 'escalate':
                print(f"Routed to: {result.get('routing', 'Unknown')}")
        else:
            print("\n📦 Support Response:\n", result)
    
    elif args.api:
        try:
            from api.main import start_api_server
            print("🚀 Starting API server...")
            start_api_server()
        except ImportError:
            print("❌ Error: API server dependencies not installed.")
            print("Install with: pip install fastapi uvicorn")
            return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
