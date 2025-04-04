# tests/test_workflows.py

import os
from workflows.crewai_workflow import run_workflow

def extract_first_customer_message(file_path: str) -> str:
    """Parses the first line spoken by the customer from a .txt file conversation log."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        if line.strip().lower().startswith("customer:"):
            return line.split(":", 1)[1].strip()
    
    raise ValueError("No customer message found in file.")

def test_workflow_with_sample_conversation():
    file_path = "data/conversations/Network Connectivity Issue.txt"
    
    print(f"🔍 Loading test conversation from: {file_path}")
    first_message = extract_first_customer_message(file_path)
    
    print(f"\n🧪 Running CrewAI multi-agent workflow on initial customer message:\n\"{first_message}\"")
    result = run_workflow(first_message)

    print("\n✅ Final Multi-Agent Output:\n")
    print(result)

if __name__ == "__main__":
    test_workflow_with_sample_conversation()
