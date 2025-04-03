# tasks/estimator_task.py

from crewai import Task
from agents.time_estimator_agent import TimeEstimatorAgent

class TimeEstimatorTask:
    def __init__(self, summary: str, actions: str):
        self.agent = TimeEstimatorAgent().get()
        self.summary = summary
        self.actions = actions

    def build(self):
        return Task(
            description=(
                "Given the issue summary and extracted action items, estimate how long it will take "
                "to fully resolve this support request based on historical ticket data and complexity.\n\n"
                f"Summary:\n{self.summary}\n\n"
                f"Actions:\n{self.actions}"
            ),
            expected_output=(
                "A realistic time estimate for resolution. For example: '2-3 business days', "
                "'Under 4 hours', or 'Escalation may take 5+ days'."
            ),
            agent=self.agent
        )
