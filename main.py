from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from langgraph_workflow import create_langgraph_workflow, AgentState

# Placeholder for API Key authentication
API_KEY = "your-super-secret-api-key"
api_key_header = APIKeyHeader(name="X-API-Key")

async def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key == API_KEY:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
    )

app = FastAPI(title="NetOps Agentic Co-Pilot API")

class NetworkLog(BaseModel):
    timestamp: str
    device_id: str
    error_code: str
    description: str

@app.post("/diagnose", dependencies=[Depends(get_api_key)])
async def diagnose_network_log(log: NetworkLog):
    """
    Accepts a network log JSON and triggers the LangGraph workflow for diagnosis.
    """
    try:
        workflow = create_langgraph_workflow()
        initial_state = AgentState(network_log=log.dict())
        result = workflow.invoke(initial_state)
        return result.final_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
