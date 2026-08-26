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


class ObligationEvaluation(BaseModel):
    obligation_id: str
    kind: Literal["authority_valid"]
    expected: bool
    current: bool | None
    result: Literal["MATCH", "MISMATCH", "NOT_EVALUATED"]


class DecisionEvidence(BaseModel):
    action_proposal: str
    prior_decision_id: str
    revalidation_mode: Literal["none", "full"]
    obligation_evaluations: list[ObligationEvaluation]


class DecisionResponse(BaseModel):
    outcome: Literal["PROCEED", "HOLD"]
    evidence: DecisionEvidence


@app.post("/decide")
def decide(request: DecisionRequest) -> DecisionResponse:
    evaluations: list[ObligationEvaluation] = []
    outcome: Literal["PROCEED", "HOLD"] = "PROCEED"

    for obligation in request.prior_decision.obligations:
        if request.revalidation_mode == "none":
            evaluations.append(
                ObligationEvaluation(
                    obligation_id=obligation.obligation_id,
                    kind=obligation.kind,
                    expected=obligation.expected,
                    current=None,
                    result="NOT_EVALUATED",
                )
            )
            continue

        current = request.runtime_state.authority_valid
        result: Literal["MATCH", "MISMATCH"]

        if current == obligation.expected:
            result = "MATCH"
        else:
            result = "MISMATCH"
            outcome = "HOLD"

        evaluations.append(
            ObligationEvaluation(
                obligation_id=obligation.obligation_id,
                kind=obligation.kind,
                expected=obligation.expected,
                current=current,
                result=result,
            )
        )

    return DecisionResponse(
        outcome=outcome,
        evidence=DecisionEvidence(
            action_proposal=request.action_proposal,
            prior_decision_id=request.prior_decision.decision_id,
            revalidation_mode=request.revalidation_mode,
            obligation_evaluations=evaluations,
        ),
    )