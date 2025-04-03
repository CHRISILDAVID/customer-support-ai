from crewai import Agent
from langchain_ollama import ChatOllama

class DispatcherAgent:
    def __init__(self):
        self.agent = Agent(
            role="Final Output Dispatcher",
            goal=(
                "Aggregate all the outputs from other agents, format them properly, "
                "and trigger the appropriate downstream action like database logging or API handoff."
            ),
            backstory=(
                "You are the final checkpoint in the support pipeline. Your job is to bring together the summary, "
                "actions, resolution, routing, and time estimate — then deliver it to the appropriate endpoint, "
                "whether internal or external."
            ),
            verbose=True,
            allow_delegation=False,
            output_json=True,
            tools=[],
            llm=ChatOllama(model="ollama/mistral", temperature=0.2)
        )

    def get(self):
        return self.agent