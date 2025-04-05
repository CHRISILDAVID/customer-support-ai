# tests/test_conversational_loop.py

from workflows.support_workflow import SupportWorkflow
import json

def test_interactive_conversation_loop():
    """
    Run an interactive conversation loop with the customer support system.
    Maintains conversation state between turns for a more coherent experience.
    """
    # Initialize the workflow with proper state management
    workflow = SupportWorkflow()
    
    print("🤖 Multi-Agent Support System Loop (Press Ctrl+C to exit)")
    print("💡 Type 'debug' to see the current state of the conversation")
    
    try:
        while True:
            # Get customer input
            new_msg = input("\n🧑 Customer: ")
            
            # Special command for debugging
            if new_msg.lower() == "debug":
                state = workflow.get_conversation_state()
                print("\n🔍 Current Conversation State:")
                print(f"  Status: {state.status}")
                print(f"  History: {len(state.conversation_history)} messages")
                print(f"  Current Summary: {state.current_summary[:100]}..." if state.current_summary else "  Current Summary: None")
                print(f"  Current Actions: {state.current_actions[:100]}..." if state.current_actions else "  Current Actions: None")
                continue
            
            # Process the message through the workflow
            result = workflow.process_message(new_msg)
            
            # Extract response details
            reply = result.get("reply", "[No reply generated]")
            status = result.get("status", "continue")
            
            # Display the response
            print(f"\n🤖 AI Reply: {reply}")
            print(f"🔁 Status: {status}")
            
            # Handle conversation end conditions
            if status == "resolved":
                print("✅ Issue Resolved. Closing conversation.")
                break
                
            if status == "escalate":
                print("🚨 Escalation triggered. Routing to human support...")
                routing = result.get("routing", "General Support")
                print(f"📋 Routed to: {routing}")
                print(f"📝 Summary: {result.get('summary', '')[:150]}...")
                print(f"⏱️ ETA: {result.get('eta', 'Unknown')}")
                break
                
            if status == "error":
                print("⚠️ Error occurred during processing.")
                print(f"Error details: {result.get('error', 'Unknown error')}")
                break
    
    except KeyboardInterrupt:
        print("\n\n👋 Conversation ended by user.")
    
    # Print conversation summary at the end
    print("\n📊 Conversation Summary:")
    state = workflow.get_conversation_state()
    print(f"  Total Messages: {len(state.conversation_history)}")
    print(f"  Final Status: {state.status}")


if __name__ == "__main__":
    test_interactive_conversation_loop()
