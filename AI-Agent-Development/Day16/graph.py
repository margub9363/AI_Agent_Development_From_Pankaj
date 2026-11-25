from langgraph.graph import(StateGraph, START, END)
from agent.state import AgentState
from node import create_planner_node

def build_graph(tools):
    builder = StateGraph(AgentState)
    planner_node=create_planner_node(tools)
    builder.add_node("planner", planner_node)
    builder.add_edge(START, "planner")
    builder.add_edge("planner",END)
    return builder.compile()