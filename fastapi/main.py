from fastapi import FastAPI, HTTPException 
from pydantic import BaseModel
from agents.graph import app
import traceback
class Query(BaseModel):
    user_input: str


fast_app = FastAPI()
@fast_app.post("/agent-run")
def run_agent(payload: Query):
    try:
        result = app.invoke({"user_input": payload.user_input})
        return {"status": "success", "data": result}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Agent execution failed: {str(e)}"
        )

