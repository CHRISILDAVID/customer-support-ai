from crewai import Agent
from langchain_ollama import ChatOllama

class SummarizerAgent:
    def __init__(self):
        self.agent = Agent(
            role="Customer Support Conversation Summarizer",
            goal=(
                "Read through customer support conversation transcripts and "
                "generate concise, clear summaries highlighting the issue, relevant details, "
                "and any actions taken or required."
            ),
            backstory=(
                "You are a summarization expert for an AI-driven customer support system. "
                "You help other agents and human support reps by providing clear and accurate "
                "summaries of lengthy customer conversations."
            ),
            verbose=True,
            allow_delegation=False,
            output_json=True,
            tools=[],
            llm=ChatOllama(model="ollama/mistral", temperature=0.3)
        )

    def get(self):
        return self.agent