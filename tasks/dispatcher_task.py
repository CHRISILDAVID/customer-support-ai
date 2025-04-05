# tasks/dispatcher_task.py

from crewai import Task
from agents.dispatcher_agent import DispatcherAgent

class DispatcherTask:
    def __init__(self, summary: str, actions: str, resolution: str, routing: str, eta: str):
        self.agent = DispatcherAgent().get()
        self.summary = summary
        self.actions = actions
        self.resolution = resolution
        self.routing = routing
        self.eta = eta

    def build(self):
        return Task(
            description=(
                "Aggregate the outputs from all previous steps and prepare a final response for the support team or customer system."
                "Your job is to compile the following information into a final response. "
                "After preparing the message, determine what status it reflects:\n"
                "- If the issue seems completely resolved, respond with status `resolved`.\n"
                "- If the resolution might not be sufficient, mark it `continue`.\n"
                "- If it's unresolved or needs human help, mark it `escalate`.\n\n"
                "Return a JSON with keys: `reply`, `status` (one of: resolved, continue, escalate)\n\n"
                f"Summary:\n{self.summary}\n\n"
                f"Actions:\n{self.actions}\n\n"
                f"Resolution:\n{self.resolution}\n\n"
                f"Routing: (Optional, TBD if escalation)\n{self.routing}\n\n"
                f"ETA:\n{self.eta}"
            ),
            expected_output=(
                '{ "reply": "message to show customer", "status": "resolved" | "continue" | "escalate" }'
            ),
            agent=self.agent
        )
