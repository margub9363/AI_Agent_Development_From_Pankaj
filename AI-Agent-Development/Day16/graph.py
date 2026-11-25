from langgraph.graph import(StateGraph, START, END)
from agent.state import AgentState
from node import create_planner_node, create_tool_node, route_after_planner
from agent.planner import planner
from agent.executor import execute_action
from agent.runner import format_answer

def create_planner_node(tools):
    def planner_node(state: AgentState):
        action = planner(state, tools)
        print("\nPlanner Selected:")
        print(action)

        return {
            "action": action,
            "finished": action == "FINISH"
        }
    return planner_node


def build_graph(tools, client):
    builder = StateGraph(AgentState)
    planner_node=create_planner_node(tools)
    tool_node= create_tool_node(client)
    builder.add_node("planner", planner_node)
    builder.add_node("tool", tool_node)
    builder.add_edge(START, "planner")
    builder.add_conditional_edges("planner", route_after_planner, {
        "tool":"tool",
        "finish":END
    })
    builder.add_conditional_edges("tool", route_after_tool, {"continue":"planner","stop":END})
    # builder.add_edge("planner",END)
    return builder.compile()

def route_after_tool(state: AgentState):
    if state["current_step"] >= state["max_steps"]:
        return "stop"

    return "continue"

def answer_node(state: AgentState):
    answer = format_answer(state)
    print("\nFinal Answer:")
    print(answer)
    return {
        "final_answer": answer,
        "finished": True
    }