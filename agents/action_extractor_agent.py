# agents/action_extractor_agent.py

from crewai import Agent
from langchain_community.chat_models import ChatOllama

class ActionExtractorAgent:
    def __init__(self):
        self.agent = Agent(
            role="Customer Support Action Item Extractor",
            goal=(
                "Analyze customer support conversations and extract clear action items such as "
                "follow-ups, tasks to be completed, escalations needed, and resolutions promised."
            ),
            backstory=(
                "You are an AI assistant helping customer support teams identify key actions from long and messy conversations. "
                "You ensure nothing falls through the cracks, and each action is well-defined for the next stage of processing."
            ),
            verbose=True,
            allow_delegation=False,
            tools=[],  # Later: add ticket creation or task assignment tools
            llm=ChatOllama(model="ollama/mistral", temperature=0.3)
        )

    def get(self):
        return self.agent
