from typing import Literal
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Track-A Runtime Validity API", version="0.1.0")

class DecisionRequest(BaseModel):
    action_proposal: str
    prior_decision_id: str
    revalidation_mode: Literal["none", "full"]

@app.post("/decide")
def decide(request: DecisionRequest) -> dict[str, str]:
    return {"outcome": "PROCEED"}

