# api/routes/predict.py

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any

from api.models import CustomerMessage, SupportResponse
from workflows.support_workflow import SupportWorkflow
from api.main import get_conversation, active_conversations

router = APIRouter(
    prefix="/predict",
    tags=["prediction"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=SupportResponse)
async def predict(message: CustomerMessage):
    """
    Process a customer message and return a support response.
    This is a stateless endpoint that doesn't maintain conversation history.
    For conversation-aware processing, use the /conversations endpoints.
    """
    # Create a temporary workflow for this prediction
    workflow = SupportWorkflow()
    
    # Process the message
    result = workflow.process_message(message.message)
    
    # Return the response
    return result

@router.post("/batch", response_model=Dict[str, SupportResponse])
async def batch_predict(messages: Dict[str, CustomerMessage]):
    """
    Process multiple customer messages in a batch.
    Each message is processed independently (stateless).
    
    The input should be a dictionary with message IDs as keys and CustomerMessage objects as values.
    The output will be a dictionary with the same keys and SupportResponse objects as values.
    """
    results = {}
    
    for msg_id, message in messages.items():
        # Create a temporary workflow for this prediction
        workflow = SupportWorkflow()
        
        # Process the message
        result = workflow.process_message(message.message)
        
        # Add to results
        results[msg_id] = result
    
    return results

@router.post("/conversation/{conversation_id}", response_model=SupportResponse)
async def predict_with_conversation(
    message: CustomerMessage,
    conversation: SupportWorkflow = Depends(get_conversation)
):
    """
    Process a customer message in the context of an existing conversation.
    This is an alternative to using the /conversations/{conversation_id}/messages endpoint.
    """
    # Process the message
    result = conversation.process_message(message.message)
    
    # Add conversation ID to the response
    result["conversation_id"] = message.conversation_id
    
    return result
