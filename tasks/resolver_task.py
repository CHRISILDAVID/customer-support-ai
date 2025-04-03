# tasks/resolver_task.py

from crewai import Task
from agents.resolution_finder_agent import ResolutionFinderAgent

class ResolutionFinderTask:
    def __init__(self, summary: str, actions: str):
        self.agent = ResolutionFinderAgent().get()
        self.summary = summary
        self.actions = actions

    def build(self):
        return Task(
            description=(
                "Based on the following customer issue summary and extracted action items, "
                "identify the most likely resolution using prior knowledge, documentation, or historical cases.\n\n"
                f"Summary:\n{self.summary}\n\n"
                f"Actions:\n{self.actions}"
            ),
            expected_output=(
                "A well-structured resolution suggestion that support agents can use directly. "
                "Include links or documentation references if relevant."
            ),
            agent=self.agent
        )
