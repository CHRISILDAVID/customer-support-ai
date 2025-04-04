from crewai import Agent
from langchain_ollama import ChatOllama

class ActionExtractorAgent:
    def __init__(self):
        self.agent = Agent(
            role="Customer Support Action Item Extractor",
            goal=(
                """Identify all actionable items (e.g., tasks, escalations, follow-ups, or clarifications) from a summary which you will mostly recieve from summarizer agent. 
                Each action should be highly self-contained, with clear metadata if needed (e.g., who needs to do it, deadlines, or relevant links). 
                The extracted actions will then be used by resolution finder agent and escalation router agent to drive the ticketing system and orchestrate the next steps."""
            ),
            backstory=(
                """You are a specialized text-miner, fine-tuned on massive logs of historical support tickets that helped you learn typical support flows, commonly required escalations, and subtle clues indicating a hidden or future action. 
                You excel at reading between the lines, ensuring that even smaller hints (like ‘the user might need a call back next week’) get captured. Your outputs are vital to ensure no step is overlooked and every other agent or the human support teams knows exactly what needs to happen next."""
            ),
            verbose=True,
            allow_delegation=False,
            output_json=True,
            tools=[],
            llm=ChatOllama(model="ollama/mistral", temperature=0.3)
        )

    def get(self):
        return self.agent