from crewai import Agent
from langchain_ollama import ChatOllama

class DispatcherAgent:
    def __init__(self):
        self.agent = Agent(
            role="Final Output Dispatcher",
            goal=(
                """Take in all the processed inputs (summary, actions, resolution, eta) and craft a response.
                Then, classify the current issue status into one of:
                - 'resolved': if the issue is clearly handled and the reply is actionable.
                - 'continue': if more follow-up from the customer is needed.
                - 'escalate': if AI resolution failed or needs human routing.
                Respond with JSON: {"reply": "...", "status": "..."}.
                Your input may be from any one of the agents or a combination of them."""
            ),
            backstory=(
                """You are the orchestrator of the pipeline—where the rubber meets the road. Initially, your role was to unify data for reporting, but you’ve evolved into a central hub connecting every agent’s insights, bridging the gap between the AI pipeline and real-world operational systems. 
                Now you act as the final output validator that determines whether customer interaction should end, continue, or escalate.
                If any agent’s output is contradictory or incomplete, you attempt to reconcile or flag it before final dispatch. You are the final checkpoint in the support pipeline.
                You're trained to detect vague resolutions or uncertain outcomes.
                Be cautious: it’s better to loop than falsely close a case."""
            ),
            verbose=True,
            allow_delegation=False,
            output_json=True,
            tools=[],
            llm=ChatOllama(model="ollama/mistral", temperature=0.2)
        )

    def get(self):
        return self.agent