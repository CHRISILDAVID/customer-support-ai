# core/conversation_state.py

class ConversationState:
    """
    Manages the state of a customer support conversation across multiple turns.
    Provides structured storage for conversation history and intermediate results.
    """
    
    def __init__(self):
        self.conversation_history = []
        self.current_summary = None
        self.current_actions = None
        self.current_resolution = None
        self.current_routing = None
        self.current_eta = None
        self.status = "continue"  # One of: continue, resolved, escalate
        
    def add_customer_message(self, message):
        """Add a customer message to the conversation history"""
        self.conversation_history.append({"role": "customer", "content": message})
        
    def add_system_message(self, message):
        """Add a system/AI message to the conversation history"""
        self.conversation_history.append({"role": "system", "content": message})
    
    def get_formatted_conversation(self):
        """Get the conversation history formatted as a string"""
        formatted = ""
        for msg in self.conversation_history:
            role = "Customer" if msg["role"] == "customer" else "Support"
            formatted += f"{role}: {msg['content']}\n\n"
        return formatted
    
    def update_processing_results(self, summary=None, actions=None, resolution=None, 
                                 routing=None, eta=None, status=None):
        """Update the current processing results"""
        if summary is not None:
            self.current_summary = summary
        if actions is not None:
            self.current_actions = actions
        if resolution is not None:
            self.current_resolution = resolution
        if routing is not None:
            self.current_routing = routing
        if eta is not None:
            self.current_eta = eta
        if status is not None:
            self.status = status
    
    def reset_turn_state(self):
        """Reset the state for a new turn while preserving conversation history"""
        self.current_summary = None
        self.current_actions = None
        self.current_resolution = None
        self.current_routing = None
        self.current_eta = None
        # Don't reset status as it may need to persist between turns
