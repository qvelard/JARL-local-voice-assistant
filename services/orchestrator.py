"""
Orchestrator module for planning via LLM.
"""
from typing import Any, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
from services.utils import logger, load_config
import requests

app = FastAPI()

class PlanRequest(BaseModel):
    user_input: str

class PlanResponse(BaseModel):
    plan: Dict[str, Any]

class Orchestrator:
    """
    Handles prompt assembly, LLM call, and plan validation.
    """
    def __init__(self) -> None:
        self.config = load_config()
        self.llm_url: str = self.config.get('orchestrator', {}).get('llm_url', 'http://localhost:8001/generate')

    def assemble_prompt(self, user_input: str) -> str:
        """
        Assembles a prompt for the LLM.
        """
        return f"Plan the following: {user_input}"

    def call_llm(self, prompt: str) -> Dict[str, Any]:
        """
        Calls the LLM endpoint and returns the plan.
        """
        try:
            logger.info(f"Calling LLM at {self.llm_url}")
            resp = requests.post(self.llm_url, json={"prompt": prompt}, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise

    def validate_plan(self, plan: Dict[str, Any]) -> bool:
        """
        Validates the plan JSON structure.
        """
        try:
            PlanResponse(plan=plan)
            return True
        except ValidationError as e:
            logger.error(f"Plan validation failed: {e}")
            return False

orchestrator = Orchestrator()

@app.post("/plan", response_model=PlanResponse)
async def plan_endpoint(req: PlanRequest):
    try:
        prompt = orchestrator.assemble_prompt(req.user_input)
        plan = orchestrator.call_llm(prompt)
        if not orchestrator.validate_plan(plan):
            raise HTTPException(status_code=400, detail="Invalid plan format")
        return PlanResponse(plan=plan)
    except Exception as e:
        logger.error(f"/plan endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 