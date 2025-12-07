from .state import State 
def orchestrator_node(state: State):
    if not state.subtasks:
        return {"response" : "No agents selected"}
    return {"__next__" : state.subtasks}
