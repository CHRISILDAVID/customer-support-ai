from crewai import Agent
from langchain_ollama import ChatOllama
from tools.team_routing_map import TeamRoutingMap

routing_map = TeamRoutingMap()

class EscalationRouterAgent:
    def __init__(self):
        self.agent = Agent(
            role="Escalation Routing Specialist",
            goal=(
                "Route escalated tickets to the appropriate department or team "
                "based on the action type and organizational rules."
            ),
            backstory=(
                "You are an expert at understanding which internal team should handle different types "
                "of escalated issues. You rely on a routing map or inference to send tasks to the right place quickly."
            ),
            verbose=True,
            allow_delegation=False,
            output_json=True,
            tools=[routing_map.route],  # ✅ Using the method decorated with @tool
            llm=ChatOllama(model="ollama/mistral", temperature=0.2)
        )

    def get(self):
        return self.agent
