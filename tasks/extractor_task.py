# tasks/extractor_task.py

from crewai import Task
from agents.action_extractor_agent import ActionExtractorAgent

class ActionExtractorTask:
    def __init__(self, summary: str):
        self.agent = ActionExtractorAgent().get()
        self.summary = summary

    def build(self):
        return Task(
            description=(
                "From the following customer issue summary, identify and extract all actionable items "
                "such as password resets, escalations, refunds, call scheduling, or follow-ups:\n\n"
                f"{self.summary}"
            ),
            expected_output=(
                "Return a bullet-point list of action items. Each item should be clear and actionable, e.g.,\n"
                "- Escalate to billing team\n"
                "- Reset user password\n"
                "- Follow up in 48 hours\n"
            ),
            agent=self.agent
        )
