from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import json
from .state import State
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=groq_key)
def exim_node(state: State):
    query = state.user_input
    prompt = f"""
You are an EXIM (Export-Import) analytics generator for pharma APIs.

Generate realistic synthetic EXIM data based on the user query.

STRICT RULES:
- Output ONLY raw JSON.
- NO markdown.
- NO backticks.
- NO comments.
- Use ONLY the following JSON format:

{{
  "import_volume_mt": [
    {{"year": 2021, "value": <number>}},
    {{"year": 2022, "value": <number>}},
    {{"year": 2023, "value": <number>}}
  ],
  "export_volume_mt": [
    {{"year": 2021, "value": <number>}},
    {{"year": 2022, "value": <number>}},
    {{"year": 2023, "value": <number>}}
  ],
  "top_import_sources": [
    {{"country": "", "percent": <number>}},
    {{"country": "", "percent": <number>}},
    {{"country": "", "percent": <number>}}
  ],
  "dependency_risk": "",
  "sourcing_insights": ["", "", ""]
}}

User query:
{query}
"""

    res = llm.invoke(prompt).content.strip()
    if res.startswith("```"):
        res = res.replace("```json", "").replace("```", "").strip()
    return {"exim": res}
