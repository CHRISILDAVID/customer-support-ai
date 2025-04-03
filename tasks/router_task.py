# tasks/router_task.py

from crewai import Task
from agents.escalation_router_agent import EscalationRouterAgent

class EscalationRouterTask:
    def __init__(self, actions: str):
        self.agent = EscalationRouterAgent().get()
        self.actions = actions

    def build(self):
        return Task(
            description=(
                "Given the following list of action items, determine if any require escalation. "
                "If escalation is needed, identify the appropriate department or team based on internal routing rules:\n\n"
                f"{self.actions}"
            ),
            expected_output=(
                "The name of the team or department to handle the escalation, if needed. "
                "Return 'No escalation needed' if there are no escalations."
            ),
            agent=self.agent
        )
