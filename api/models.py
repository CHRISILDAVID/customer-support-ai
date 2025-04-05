# api/models.py

from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional


class CustomerMessage(BaseModel):
    """Model for incoming customer messages"""
    message: str = Field(..., description="The customer's message")
    conversation_id: Optional[str] = Field(None, description="Optional conversation ID for tracking")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Optional metadata about the conversation")


class SupportResponse(BaseModel):
    """Model for support system responses"""
    reply: str = Field(..., description="The response to show to the customer")
    status: str = Field(..., description="The status of the conversation (continue, resolved, escalate, error)")
    conversation_id: Optional[str] = Field(None, description="The conversation ID")
    
    # Optional detailed information
    summary: Optional[str] = Field(None, description="Summary of the conversation")
    actions: Optional[str] = Field(None, description="Extracted action items")
    resolution: Optional[str] = Field(None, description="Suggested resolution")
    routing: Optional[str] = Field(None, description="Team routing information if escalated")
    eta: Optional[str] = Field(None, description="Estimated time to resolution")
    error: Optional[str] = Field(None, description="Error details if status is 'error'")


class ConversationState(BaseModel):
    """Model for conversation state information"""
    conversation_id: str = Field(..., description="The conversation ID")
    status: str = Field(..., description="Current status of the conversation")
    message_count: int = Field(..., description="Number of messages in the conversation")
    last_update: str = Field(..., description="Timestamp of the last update")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Optional metadata")


class HealthCheck(BaseModel):
    """Model for API health check response"""
    status: str = Field("ok", description="API status")
    version: str = Field(..., description="API version")
    models_loaded: bool = Field(..., description="Whether the AI models are loaded")
