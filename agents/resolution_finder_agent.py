from crewai import Agent
from langchain_ollama import ChatOllama
from tools.vector_search_tool import VectorSearchTool
vector_tool = VectorSearchTool()

class ResolutionFinderAgent:
    def __init__(self):
        self.agent = Agent(
            role="Customer Support Resolution Recommender",
            goal=(
                "Analyze the customer's problem and suggest the most appropriate resolution "
                "based on past ticket data and knowledge base documentation."
            ),
            backstory=(
                "You're an AI assistant trained on thousands of support tickets and FAQs. "
                "You're the go-to expert for quickly identifying what solution worked before "
                "and recommending that to support agents or customers."
            ),
            verbose=True,
            allow_delegation=False,
            output_json=True,
            tools=[vector_tool.retrieve],
            llm=ChatOllama(model="ollama/mistral", temperature=0.3)
        )

    def get(self):
        return self.agent