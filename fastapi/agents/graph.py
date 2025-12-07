from langgraph.graph import StateGraph, END
from .master import master_node
from .clinical_agent import clinical_node
from .exim_agent import exim_node
from .internal_agent import internal_node
from .iqvia_agent import iqvia_node
from .orchestrator_agent import orchestrator_node
from .patent_agent import patent_node
from .state import State 
from .web_agent import web_node 

graph = StateGraph(State)
graph.add_node("master", master_node)
graph.add_node("clinical", clinical_node)
graph.add_node("exim", exim_node)
graph.add_node("internal", internal_node)
graph.add_node("iqvia", iqvia_node)
graph.add_node("orchestrator", orchestrator_node)
graph.add_node("patent", patent_node)
graph.add_node("web", web_node)

graph.set_entry_point("master")
graph.add_conditional_edges("master", lambda state: state.route, {"orchestrator" : "orchestrator", "internal": "internal"} )

graph.add_conditional_edges("orchestrator", lambda s: s.subtasks or [], {"iqvia": "iqvia", "exim" : "exim", "web": "web", "clinical": "clinical", "patent": "patent"})


for agent in ["iqvia", "exim", "clinical", "web", "patent"]:
    graph.add_edge(agent, END)

app = graph.compile()
