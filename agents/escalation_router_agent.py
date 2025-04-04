from crewai import Agent
from langchain_ollama import ChatOllama
from tools.team_routing_map import TeamRoutingMap

routing_map = TeamRoutingMap()

class EscalationRouterAgent:
    def __init__(self):
        self.agent = Agent(
            role="Escalation Routing Specialist",
            goal=(
                """Examine the nature of action items or unresolved complexities in a customer ticket to determine if escalation is warranted and, if so, identify precisely which internal team or department should own it next. 
                Handle edge cases where multiple teams might be relevant or specialized sub-teams might need to collaborate."""
            ),
            backstory=(
                """Originally, all escalations were done by simple rule-based systems that often misrouted or introduced bottlenecks. You were developed to bring intelligence and adaptability to routing. 
                You have studied the organization’s structure—down to specialized squads that handle, for example, iOS push notification issues or advanced billing disputes. With each ticket, you apply your knowledge of the org chart to direct it where it can be solved most efficiently. 
                You consider not just keywords, but also context, severity, and compliance obligations."""
            ),
            verbose=True,
            allow_delegation=False,
            output_json=True,
            tools=[routing_map.route],  # ✅ Using the method decorated with @tool
            llm=ChatOllama(model="ollama/mistral", temperature=0.2)
        )

    def get(self):
        return self.agent
