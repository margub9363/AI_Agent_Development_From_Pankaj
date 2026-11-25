from agent.planner import planner
from agent.state import AgentState
from agent.executor import execute_action

def create_planner_node(tools):

    def planner_node(state: AgentState):
        action = planner(state, tools)
        print("\n Planner Selected:")
        print(action)
        # return {
        #     "actions":state["actions"],
        #     "observations":state["observations"],
        #     "current_step":state["current_step"],
        #     "finished":action == "FINISH", # This is changed now
        #     "final_answer": state["final_answer"]
        # }
        return {
            "action": action,
            "finished": action == "FINISH"
        }
    return planner_node

def create_tool_node(client):
    async def tool_node(state: AgentState):
        action = state["action"]
        observation  = await execute_action(action, client)
        print("\nTool Observation:")
        print(observation)
        return {
            "observations":(
                state["observations"]+[{
                    "step":state["current_step"],
                    "action":action,
                    "observation": observation
                }]
            ),
            "actions":(
                state["actions"]+[action]
            ),
            "current_step":(
                state["current_step"]+1
            )
        }
    return tool_node

def route_after_planner(state: AgentState):
    if state["action"] == "FINISH":
        return "finish"
    return "tool"

def route_after_tool (state:AgentState):
    if state["current_step"] >= state["max_steps"]:
        return "stop"
    return "continue"