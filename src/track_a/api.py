from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(title="Track A Runtime Validity")


class Obligation(BaseModel):
    obligation_id: str
    kind: Literal["authority_valid"]
    expected: Literal[True]


class PriorDecision(BaseModel):
    decision_id: str
    outcome: Literal["PROCEED"]
    obligations: list[Obligation] = Field(min_length=1)


class DecisionRequest(BaseModel):
    action_proposal: str
    prior_decision: PriorDecision
    revalidation_mode: Literal["none", "full"]


@app.post("/decide")
def decide(request: DecisionRequest) -> dict[str, str]:
    return {"outcome": "PROCEED"}