from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph
from agents.research_agent import research_agent_fn
from agents.answer_agent import answer_drafter_fn

# Enhanced state schema with sources
class ResearchState(TypedDict):
    input: str
    research_data: str
    answer: str
    sources: List[Dict[str, Any]]

# Create the state graph with schema
graph = StateGraph(ResearchState)

# Register nodes
graph.add_node("ResearchAgent", research_agent_fn)
graph.add_node("AnswerDrafterAgent", answer_drafter_fn)

# Define flow
graph.set_entry_point("ResearchAgent")
graph.add_edge("ResearchAgent", "AnswerDrafterAgent")
graph.set_finish_point("AnswerDrafterAgent")

# Compile the graph
app = graph.compile()