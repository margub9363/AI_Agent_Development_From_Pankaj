from agent.planner import planner
from agent.state import AgentState


def create_planner_node(tools):

    def planner_node(state: AgentState):
        action = planner(state, tools)
        print("\n Planner Selected:")
        print(action)
        return {
            "actions":state["actions"],
            "observations":state["observations"],
            "current_step":state["current_step"],
            "finished":action == "FINISH", # This is changed now
            "final_answer": state["final_answer"]
        }
    return planner_node

