from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field, StrictBool


app = FastAPI(title="Track A Runtime Validity")


class Obligation(BaseModel):
    obligation_id: str
    kind: Literal["authority_valid"]
    expected: Literal[True]


class PriorDecision(BaseModel):
    decision_id: str
    outcome: Literal["PROCEED"]
    obligations: list[Obligation] = Field(min_length=1)


class RuntimeState(BaseModel):
    authority_valid: StrictBool


class DecisionRequest(BaseModel):
    action_proposal: str
    prior_decision: PriorDecision
    runtime_state: RuntimeState
    revalidation_mode: Literal["none", "full"]


@app.post("/decide")
def decide(request: DecisionRequest) -> dict[str, str]:
    if request.revalidation_mode == "full":
        for obligation in request.prior_decision.obligations:
            if (
                obligation.kind == "authority_valid"
                and request.runtime_state.authority_valid != obligation.expected
            ):
                return {"outcome": "HOLD"}

    return {"outcome": "PROCEED"}