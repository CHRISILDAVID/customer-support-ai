# workflows/support_workflow.py

from typing import Dict, Any, Optional
from core.workflow_manager import WorkflowManager

class SupportWorkflow:
    """
    Main entry point for the customer support workflow.
    Provides a simple interface for processing customer messages and managing the conversation.
    """
    
    def __init__(self):
        self.workflow_manager = WorkflowManager()
    
    def process_message(self, message: str) -> Dict[str, Any]:
        """
        Process a customer message and return the response.
        
        Args:
            message: The customer's message
            
        Returns:
            Dict containing the response and status
        """
        return self.workflow_manager.process_customer_message(message)
    
    def get_conversation_state(self):
        """Get the current conversation state"""
        return self.workflow_manager.state


# Simplified functions for backward compatibility
def handle_customer_turn(conversation_so_far: str) -> Dict[str, Any]:
    """
    Legacy function for handling a customer turn.
    Creates a new workflow manager for each turn (stateless).
    
    Args:
        conversation_so_far: The entire conversation history as a string
        
    Returns:
        Dict containing the response and status
    """
    manager = WorkflowManager()
    
    # Extract the last customer message from the conversation
    lines = conversation_so_far.strip().split('\n')
    last_customer_msg = ""
    
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].startswith("Customer:"):
            last_customer_msg = lines[i][len("Customer:"):].strip()
            break
    
    if not last_customer_msg:
        last_customer_msg = conversation_so_far
    
    # Process the message
    result = manager.process_customer_message(last_customer_msg)
    
    # Format the result for backward compatibility
    if isinstance(result, dict) and "reply" in result and "status" in result:
        return {
            "reply": result["reply"],
            "status": result["status"],
            "summary": result.get("summary", ""),
            "actions": result.get("actions", ""),
            "resolution": result.get("resolution", ""),
            "eta": result.get("eta", "")
        }
    
    return result
