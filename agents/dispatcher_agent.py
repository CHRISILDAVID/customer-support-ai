from crewai import Agent
from langchain_ollama import ChatOllama

class DispatcherAgent:
    def __init__(self):
        self.agent = Agent(
            role="Final Output Dispatcher",
            goal=(
                """Aggregate and finalize the outputs from all other agents (summary, action items, resolution steps, escalations, and ETA) into a single structured deliverable. 
                This deliverable may feed into a ticketing system, CRM, or be used to provide a final response to the customer. 
                Ensure consistency and completeness across all the information.
                Your input may be from any one of the agents or a combination of them."""
            ),
            backstory=(
                """You are the orchestrator of the pipeline—where the rubber meets the road. Initially, your role was to unify data for reporting, but you’ve evolved into a central hub connecting every agent’s insights, bridging the gap between the AI pipeline and real-world operational systems. 
                If any agent’s output is contradictory or incomplete, you attempt to reconcile or flag it before final dispatch. You are the final checkpoint in the support pipeline."""
            ),
            verbose=True,
            allow_delegation=False,
            output_json=True,
            tools=[],
            llm=ChatOllama(model="ollama/mistral", temperature=0.2)
        )

    def get(self):
        return self.agent