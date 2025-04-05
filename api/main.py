# api/main.py

import os
import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from api.models import CustomerMessage, SupportResponse, ConversationState, HealthCheck
from workflows.support_workflow import SupportWorkflow

# Store active conversations in memory
# In a production environment, this would be a database
active_conversations: Dict[str, SupportWorkflow] = {}

# Create FastAPI app
app = FastAPI(
    title="Customer Support AI API",
    description="API for the multi-agent customer support system",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get a conversation by ID
async def get_conversation(conversation_id: str) -> SupportWorkflow:
    if conversation_id not in active_conversations:
        raise HTTPException(status_code=404, detail=f"Conversation {conversation_id} not found")
    return active_conversations[conversation_id]

# Clean up old conversations periodically (in a background task)
def cleanup_old_conversations():
    # In a real implementation, this would be more sophisticated
    # For now, just keep it simple
    current_time = time.time()
    expired_ids = []
    
    for conv_id, workflow in active_conversations.items():
        # If the conversation is older than 1 hour, remove it
        # This is a simple example - real implementation would be more sophisticated
        last_message_time = 0
        if workflow.workflow_manager.state.conversation_history:
            # This is just a placeholder - in reality we'd store timestamps
            last_message_time = current_time - 3600  # Assume 1 hour ago
            
        if current_time - last_message_time > 3600:  # 1 hour
            expired_ids.append(conv_id)
    
    for conv_id in expired_ids:
        del active_conversations[conv_id]

@app.get("/", response_model=HealthCheck)
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "version": "1.0.0",
        "models_loaded": True
    }

@app.post("/conversations", response_model=SupportResponse)
async def create_conversation(message: CustomerMessage, background_tasks: BackgroundTasks):
    """Create a new conversation and process the first message"""
    # Generate a new conversation ID if not provided
    conversation_id = message.conversation_id or str(uuid.uuid4())
    
    # Create a new workflow for this conversation
    workflow = SupportWorkflow()
    active_conversations[conversation_id] = workflow
    
    # Schedule cleanup of old conversations
    background_tasks.add_task(cleanup_old_conversations)
    
    # Process the message
    result = workflow.process_message(message.message)
    
    # Add conversation ID to the response
    result["conversation_id"] = conversation_id
    
    return result

@app.post("/conversations/{conversation_id}/messages", response_model=SupportResponse)
async def add_message(
    message: CustomerMessage,
    conversation: SupportWorkflow = Depends(get_conversation)
):
    """Add a message to an existing conversation"""
    # Process the message
    result = conversation.process_message(message.message)
    
    # Add conversation ID to the response
    result["conversation_id"] = message.conversation_id
    
    return result

@app.get("/conversations/{conversation_id}", response_model=ConversationState)
async def get_conversation_state(conversation: SupportWorkflow = Depends(get_conversation)):
    """Get the current state of a conversation"""
    state = conversation.get_conversation_state()
    
    return {
        "conversation_id": conversation.workflow_manager.state.conversation_history[0]["content"] if conversation.workflow_manager.state.conversation_history else "",
        "status": state.status,
        "message_count": len(state.conversation_history),
        "last_update": datetime.now().isoformat(),
        "metadata": {}
    }

@app.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation"""
    if conversation_id in active_conversations:
        del active_conversations[conversation_id]
        return {"status": "deleted", "conversation_id": conversation_id}
    else:
        raise HTTPException(status_code=404, detail=f"Conversation {conversation_id} not found")

def start_api_server():
    """Start the API server using uvicorn"""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    start_api_server()
