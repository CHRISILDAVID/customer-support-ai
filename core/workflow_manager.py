# core/workflow_manager.py

import json
from typing import Dict, Any, Optional
from crewai import Crew

from core.conversation_state import ConversationState
from tasks.summarizer_task import SummarizerTask
from tasks.extractor_task import ActionExtractorTask
from tasks.resolver_task import ResolutionFinderTask
from tasks.router_task import EscalationRouterTask
from tasks.estimator_task import TimeEstimatorTask
from tasks.dispatcher_task import DispatcherTask


class WorkflowManager:
    """
    Manages the execution of the customer support workflow.
    Handles the orchestration of tasks, error handling, and conditional paths.
    """
    
    def __init__(self):
        self.state = ConversationState()
    
    def process_customer_message(self, message: str) -> Dict[str, Any]:
        """
        Process a new customer message through the support workflow.
        
        Args:
            message: The customer's message
            
        Returns:
            Dict containing the response and status
        """
        # Update conversation state
        self.state.add_customer_message(message)
        
        try:
            # Step 1: Summarize the conversation
            summary = self._run_summarizer()
            self.state.update_processing_results(summary=summary)
            
            # Step 2: Extract actions from summary
            actions = self._run_action_extractor(summary)
            self.state.update_processing_results(actions=actions)
            
            # Step 3: Find resolution
            resolution = self._run_resolution_finder(summary, actions)
            self.state.update_processing_results(resolution=resolution)
            
            # Step 4: Estimate time to resolve
            eta = self._run_time_estimator(summary, actions)
            self.state.update_processing_results(eta=eta)
            
            # Step 5: Check if escalation is needed based on actions
            if self._needs_escalation(actions):
                routing = self._run_escalation_router(actions)
                self.state.update_processing_results(routing=routing)
            else:
                routing = "No escalation needed"
                self.state.update_processing_results(routing=routing)
            
            # Step 6: Generate final response
            response = self._run_dispatcher(summary, actions, resolution, routing, eta)
            
            # Parse the response
            parsed_response = self._parse_agent_output(response)
            reply = parsed_response.get("reply", "[No reply generated]")
            status = parsed_response.get("status", "continue")
            
            # Update state with the final status and add system message
            self.state.update_processing_results(status=status)
            self.state.add_system_message(reply)
            
            return {
                "reply": reply,
                "status": status,
                "summary": summary,
                "actions": actions,
                "resolution": resolution,
                "routing": routing,
                "eta": eta
            }
            
        except Exception as e:
            error_msg = f"An error occurred during processing: {str(e)}"
            self.state.add_system_message(f"I apologize, but I encountered an issue while processing your request. {error_msg}")
            return {
                "reply": f"I apologize, but I encountered an issue while processing your request. Our team has been notified.",
                "status": "error",
                "error": error_msg
            }
    
    def _parse_agent_output(self, output: str) -> Dict[str, Any]:
        """Safely parse agent output to extract structured data"""
        if not output:
            return {"reply": "", "status": "continue"}
            
        try:
            # First try to parse as JSON
            if isinstance(output, str):
                # Clean the output if it contains markdown code blocks
                if "```json" in output:
                    output = output.split("```json")[1].split("```")[0].strip()
                elif "```" in output:
                    output = output.split("```")[1].split("```")[0].strip()
                
                return json.loads(output)
            elif isinstance(output, dict):
                return output
        except json.JSONDecodeError:
            # If not valid JSON, return the raw output as reply
            pass
        
        return {"reply": output, "status": "continue"}
    
    def _needs_escalation(self, actions: str) -> bool:
        """Determine if the actions require escalation"""
        escalation_keywords = [
            "escalate", "escalation", "supervisor", "manager", 
            "tier 2", "tier 3", "specialist", "expert"
        ]
        
        return any(keyword in actions.lower() for keyword in escalation_keywords)
    
    def _run_summarizer(self) -> str:
        """Run the summarizer task"""
        task = SummarizerTask(self.state.get_formatted_conversation()).build()
        crew = Crew(tasks=[task], verbose=True)
        return crew.kickoff()
    
    def _run_action_extractor(self, summary: str) -> str:
        """Run the action extractor task"""
        task = ActionExtractorTask(summary).build()
        crew = Crew(tasks=[task], verbose=True)
        return crew.kickoff()
    
    def _run_resolution_finder(self, summary: str, actions: str) -> str:
        """Run the resolution finder task"""
        task = ResolutionFinderTask(summary=summary, actions=actions).build()
        crew = Crew(tasks=[task], verbose=True)
        return crew.kickoff()
    
    def _run_time_estimator(self, summary: str, actions: str) -> str:
        """Run the time estimator task"""
        task = TimeEstimatorTask(summary=summary, actions=actions).build()
        crew = Crew(tasks=[task], verbose=True)
        return crew.kickoff()
    
    def _run_escalation_router(self, actions: str) -> str:
        """Run the escalation router task"""
        task = EscalationRouterTask(actions=actions).build()
        crew = Crew(tasks=[task], verbose=True)
        return crew.kickoff()
    
    def _run_dispatcher(self, summary: str, actions: str, resolution: str, routing: str, eta: str) -> str:
        """Run the dispatcher task"""
        task = DispatcherTask(
            summary=summary,
            actions=actions,
            resolution=resolution,
            routing=routing,
            eta=eta
        ).build()
        crew = Crew(tasks=[task], verbose=True)
        return crew.kickoff()
