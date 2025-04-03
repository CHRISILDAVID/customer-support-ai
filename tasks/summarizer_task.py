# tasks/summarizer_task.py

from crewai import Task
from agents.summarizer_agent import SummarizerAgent

class SummarizerTask:
    def __init__(self, input_conversation: str):
        self.agent = SummarizerAgent().get()
        self.input_conversation = input_conversation

    def build(self):
        return Task(
            description=(
                "Summarize the following customer support conversation. Extract the main issue, "
                "any important context (e.g. account details, technical specs), and what the customer needs help with:\n\n"
                f"{self.input_conversation}"
            ),
            expected_output=(
                "A short summary (3-5 sentences max) capturing the customer's main issue, "
                "relevant details, and tone of the conversation (urgent, confused, angry, etc.)."
            ),
            agent=self.agent
        )
