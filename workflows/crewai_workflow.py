# workflows/crewai_workflow.py
"""
Legacy workflow implementation for backward compatibility.
New code should use the support_workflow.py module instead.
"""

import json
from typing import Dict, Any, Optional
from workflows.support_workflow import SupportWorkflow, handle_customer_turn as new_handle_customer_turn

# Re-export the handle_customer_turn function from support_workflow
handle_customer_turn = new_handle_customer_turn

def escalate_and_respond(summary: str, actions: str, resolution: str, eta: str) -> Dict[str, Any]:
    """
    When dispatcher decides the issue requires escalation, route it to the right team
    and return a final response using Dispatcher.
    
    This function is maintained for backward compatibility.
    New code should use the WorkflowManager directly.
    """
    # Create a new workflow instance
    workflow = SupportWorkflow()
    
    # We need to initialize the state with the current context
    state = workflow.get_conversation_state()
    state.update_processing_results(
        summary=summary,
        actions=actions,
        resolution=resolution,
        eta=eta
    )
    
    # Process a dummy message to trigger the escalation path
    dummy_message = "Please escalate this issue to the appropriate team."
    result = workflow.process_message(dummy_message)
    
    return result

def process_file(file_path: str) -> Dict[str, Any]:
    """
    Process a conversation file and return the support response.
    
    Args:
        file_path: Path to the conversation file
        
    Returns:
        Dict containing the response and status
    """
    with open(file_path, "r", encoding="utf-8") as f:
        conversation_text = f.read()
    
    return handle_customer_turn(conversation_text)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run CrewAI Multi-Agent Customer Support Pipeline")
    parser.add_argument("--file", type=str, required=True, help="Path to customer conversation file (txt)")
    args = parser.parse_args()

    result = process_file(args.file)
    
    # Format the output for display
    if isinstance(result, dict):
        print("\n📦 Final Support Response:")
        print(f"Reply: {result.get('reply', '')}")
        print(f"Status: {result.get('status', '')}")
        
        if result.get('status') == 'escalate':
            print(f"Routed to: {result.get('routing', 'Unknown')}")
    else:
        print("\n📦 Final Support Response:\n", result)
