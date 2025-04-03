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
                "Aggregate the outputs from all previous steps and prepare a final response "
                "for the support team or customer system. Format it clearly and include:\n\n"
                f"Summary:\n{self.summary}\n\n"
                f"Actions:\n{self.actions}\n\n"
                f"Suggested Resolution:\n{self.resolution}\n\n"
                f"Routing Info:\n{self.routing}\n\n"
                f"Estimated Time to Resolution:\n{self.eta}"
            ),
            expected_output=(
                "A structured and complete JSON-style output that can be sent to a downstream system. "
                "It should include all five sections clearly, and be suitable for logging or API delivery."
            ),
            agent=self.agent
        )
