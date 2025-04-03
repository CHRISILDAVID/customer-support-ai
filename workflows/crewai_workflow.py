# workflows/crewai_workflow.py

from crewai import Crew
from tasks.summarizer_task import SummarizerTask
from tasks.extractor_task import ActionExtractorTask
from tasks.resolver_task import ResolutionFinderTask
from tasks.router_task import EscalationRouterTask
from tasks.estimator_task import TimeEstimatorTask
from tasks.dispatcher_task import DispatcherTask
from tools.vector_search_tool import VectorSearchTool

def run_workflow(conversation_text: str):
    # 🔍 Load vector search tool
    vector_tool = VectorSearchTool().retrieve

    # 🧠 Step 1: Summarize
    summarizer_task = SummarizerTask(conversation_text).build()

    # 🧠 Step 2: Extract Actions
    extractor_task = ActionExtractorTask(summarizer_task.output).build()

    # 🧠 Step 3: Find Resolution (with vector tool)
    resolver_task = ResolutionFinderTask(
        summary=summarizer_task.output,
        actions=extractor_task.output
    ).build()
    resolver_task.tools = [vector_tool]

    # 🧠 Step 4: Route if Escalation Required
    router_task = EscalationRouterTask(actions=extractor_task.output).build()

    # 🧠 Step 5: Estimate Resolution Time
    estimator_task = TimeEstimatorTask(
        summary=summarizer_task.output,
        actions=extractor_task.output
    ).build()

    # ✅ Step 6: Final Dispatch
    dispatcher_task = DispatcherTask(
        summary=summarizer_task.output,
        actions=extractor_task.output,
        resolution=resolver_task.output,
        routing=router_task.output,
        eta=estimator_task.output
    ).build()

    # 🧠 CrewAI pipeline
    crew = Crew(
        tasks=[
            summarizer_task,
            extractor_task,
            resolver_task,
            router_task,
            estimator_task,
            dispatcher_task
        ],
        verbose=True
    )

    # 🚀 Execute the multi-agent workflow
    result = crew.kickoff()
    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run CrewAI Multi-Agent Customer Support Pipeline")
    parser.add_argument("--file", type=str, required=True, help="Path to customer conversation file (txt)")
    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        conversation_text = f.read()

    output = run_workflow(conversation_text)
    print("\n📦 Final Support Response:\n", output)
