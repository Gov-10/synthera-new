from fastapi import FastAPI, HTTPException, Depends 
from pydantic import BaseModel
from agents.graph import app
import traceback
from auth import CustomAuth, get_current_user
from fastapi.middleware.cors import CORSMiddleware
class Query(BaseModel):
    user_input: str


fast_app = FastAPI()
@fast_app.post("/agent-run")
def run_agent(payload: Query, user=Depends(get_current_user)):
    user = request.auth
    try:
        result = app.invoke({"user_input": payload.user_input, "user_email" : user["email"] , "user_id" : user["sub"] })
        return {"status": "success", "data": result}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Agent execution failed: {str(e)}"
        )

fast_app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

