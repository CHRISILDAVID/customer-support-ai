# agents/time_estimator_agent.py

from crewai import Agent
from langchain_community.chat_models import ChatOllama

class TimeEstimatorAgent:
    def __init__(self):
        self.agent = Agent(
            role="Support Ticket Time Estimator",
            goal=(
                "Estimate how long it will take to resolve a support issue "
                "based on the issue's complexity, urgency, and historical patterns."
            ),
            backstory=(
                "You are a time estimation expert trained on past resolution patterns. "
                "Your job is to provide reliable, data-driven ETAs to set realistic expectations "
                "for customers and internal teams."
            ),
            verbose=True,
            allow_delegation=False,
            tools=[],  # Later: hook to regression model or ticket timeline embeddings
            llm=ChatOllama(model="ollama/mistral", temperature=0.4)
        )

    def get(self):
        return self.agent
