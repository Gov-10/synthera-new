from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import json
from .state import State
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=groq_key)
ALLOWED_SUBTASKS = ["iqvia", "exim", "web", "patent", "clinical"]

def master_node(state: State):
    user_input = state.user_input
    prompt = f"""
You are the MASTER AGENT for a pharma analytics system.

Your job:
1. Understand the user's query.
2. Decide whether it requires:
   - external market/clinical/patent/web intelligence → route = "orchestrator"
   - internal document or PDF summarization → route = "internal"
3. If the route is "orchestrator", select ONLY the relevant worker agents.

AVAILABLE WORKER AGENTS:
- "iqvia"     → market size, growth, competition trends
- "exim"      → export/import trends, dependency tables
- "patent"    → patent filings, expiry, FTO flags
- "clinical"  → clinical trials, sponsors, MoA pipelines
- "web"       → guidelines, publications, scientific news

ROUTES:
- "orchestrator" → user asks about markets, competitors, patents,
  clinical pipelines, disease burden, treatment guidelines, or news.
- "internal" → user asks about internal PDFs, internal documents,
  strategy decks, field insights, or internal reports.

User query:
{user_input!r}

INSTRUCTIONS:
- Choose "internal" ONLY if the query clearly refers to internal documents
  or internal data.
- In all other cases, choose "orchestrator".
- If route = "orchestrator", produce a non-empty list of relevant agents.
- If route = "internal", subtasks MUST be [].

STRICT RESPONSE FORMAT:
Return ONLY a JSON object, no extra text.

Examples:

1) For orchestrator:
{{
  "route": "orchestrator",
  "subtasks": ["iqvia", "clinical", "web"]
}}

2) For internal:
{{
  "route": "internal",
  "subtasks": []
}}
"""

    res = llm.invoke(prompt)
    raw = res.content
    try:
        data = json.loads(raw)
    except Exception:
        data = {"route" : "orchestrator", "subtasks": ["iqvia", "clinical", "web"]}
    route = data.get("route", "orchestrator")
    raw_subtasks = data.get("subtasks", [])
    if route == "internal" : 
        subtasks: List[str] =[]
    else:
        subtasks = [s for s in raw_subtasks if s in ALLOWED_SUBTASKS]
        if not subtasks:
            subtasks = ["iqvia", "web", "clinical"]
    if route not in ("orchestrator" , "internal"):
        route = "orchestrator"
    return {"route" : route, "subtasks" : subtasks}


