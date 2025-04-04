# tests/test_agents.py

from agents.resolution_finder_agent import ResolutionFinderAgent
from agents.escalation_router_agent import EscalationRouterAgent
from tools.vector_search_tool import VectorSearchTool
from tools.team_routing_map import TeamRoutingMap
from crewai.tools import tool
from crewai import Task, Crew


# ✅ Tool wrapper for vector search
@tool("vector_search")
def vector_search_tool(query: str) -> str:
    """Searches relevant historical documents using vector similarity."""
    return VectorSearchTool().retrieve(query)


# ✅ Tool wrapper for routing escalation
@tool("route_escalation")
def route_action_tool(query: str) -> str:
    """Routes an action to the appropriate internal team based on routing rules."""
    return TeamRoutingMap().get_team_for_action(query)


def test_resolution_finder_agent():
    print("\n🔍 Testing ResolutionFinderAgent with VectorSearchTool")

    summary = "Customer reports that the app says 'no internet connection' despite working Wi-Fi."
    actions = "Troubleshoot connectivity issue; suggest clearing cache or resetting network permissions."

    agent = ResolutionFinderAgent().get()
    agent.tools = [vector_search_tool]  # ✅ Attach the tool

    task = Task(
        description="Use the vector search tool to retrieve relevant resolutions for: 'no internet connection despite working Wi-Fi'. Only use the tool.",
        expected_output="A relevant set of resolution suggestions retrieved using the tool.",
        agent=agent
    )


    crew = Crew(tasks=[task], verbose=True)
    result = crew.kickoff()

    print("\n✅ Resolution Suggestion:")
    print(result)


def test_escalation_router_agent():
    print("\n🧭 Testing EscalationRouterAgent with TeamRoutingMap")

    actions = [
        "Escalate to billing due to failed refund",
        "Reset user password",
        "Send to tech team for app crash issue"
    ]

    agent = EscalationRouterAgent().get()
    agent.tools = [route_action_tool]  # ✅ Attach the tool

    for action in actions:
        task = Task(
            description=action,
            expected_output="The team this issue should be routed to.",
            agent=agent
        )
        crew = Crew(tasks=[task], verbose=True)
        result = crew.kickoff()
        print(f"\n🔄 Action: {action}\n🏢 Routed To: {result}")


if __name__ == "__main__":
    test_resolution_finder_agent()
    test_escalation_router_agent()
