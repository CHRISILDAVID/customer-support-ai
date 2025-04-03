from crewai.tools import tool
import json
import os

class TeamRoutingMap:
    def __init__(self, rules_path: str = "data/team_routing_rules.json"):
        if not os.path.exists(rules_path):
            raise FileNotFoundError(f"Missing team routing config: {rules_path}")
        with open(rules_path, "r") as file:
            self.routing_rules = json.load(file)

    def get_team_for_action(self, action_item: str) -> str:
        for keyword, team in self.routing_rules.items():
            if keyword.lower() in action_item.lower():
                return team
        return "General Support"

    def route_bulk(self, action_items: list) -> dict:
        return {item: self.get_team_for_action(item) for item in action_items}

    @tool("TeamRouter")
    def route(self, query: str) -> str:
        """
        Routes a single escalation action to the correct internal team using a routing map.
        """
        return self.get_team_for_action(query)
