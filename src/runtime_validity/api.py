from datetime import datetime, timezone
from hmac import compare_digest
import os
from typing import Literal
from uuid import UUID, uuid4

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, ConfigDict, Field, StrictBool


app = FastAPI(title="Runtime Validity - Track A")


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


class AuthorityTransition(BaseModel):
    transition_id: UUID
    occurred_at: datetime
    previous_authority_valid: StrictBool
    current_authority_valid: StrictBool


class ExperimentalAuthorityStateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    authority_valid: StrictBool


class DecisionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action_proposal: str
    prior_decision: PriorDecision
    revalidation_mode: Literal["none", "full"]


class ObligationEvaluation(BaseModel):
    obligation_id: str
    kind: Literal["authority_valid"]
    expected: bool
    current: bool | None
    result: Literal["MATCH", "MISMATCH", "NOT_EVALUATED"]


class DecisionEvidence(BaseModel):
    record_id: UUID
    created_at: datetime
    schema_version: Literal["1"]
    action_proposal: str
    prior_decision_id: str
    revalidation_mode: Literal["none", "full"]
    obligation_evaluations: list[ObligationEvaluation]


class DecisionResponse(BaseModel):
    outcome: Literal["PROCEED", "HOLD"]
    evidence: DecisionEvidence


server_runtime_state = RuntimeState(authority_valid=True)

decision_records: dict[UUID, DecisionResponse] = {}

authority_transitions: dict[UUID, AuthorityTransition] = {}


def get_current_runtime_state() -> RuntimeState:
    return server_runtime_state


def set_current_runtime_state(
    *,
    authority_valid: bool,
) -> AuthorityTransition | None:
    global server_runtime_state

    next_runtime_state = RuntimeState(authority_valid=authority_valid)

    previous_authority_valid = server_runtime_state.authority_valid
    current_authority_valid = next_runtime_state.authority_valid

    if previous_authority_valid == current_authority_valid:
        return None

    transition = AuthorityTransition(
        transition_id=uuid4(),
        occurred_at=datetime.now(timezone.utc),
        previous_authority_valid=previous_authority_valid,
        current_authority_valid=current_authority_valid,
    )

    authority_transitions[transition.transition_id] = transition
    server_runtime_state = next_runtime_state

    return transition


def require_experimental_authority_control(
    x_experimental_control_token: str | None = Header(default=None),
) -> None:
    if os.getenv("RUNTIME_VALIDITY_ENABLE_EXPERIMENTAL_CONTROL") != "1":
        raise HTTPException(
            status_code=403,
            detail="Experimental authority control is disabled",
        )

    expected_token = os.getenv(
        "RUNTIME_VALIDITY_EXPERIMENTAL_CONTROL_TOKEN"
    )

    if (
        expected_token is None
        or x_experimental_control_token is None
        or not compare_digest(
            x_experimental_control_token,
            expected_token,
        )
    ):
        raise HTTPException(
            status_code=403,
            detail="Invalid experimental control token",
        )


@app.post("/experimental/authority-state")
def set_experimental_authority_state(
    request: ExperimentalAuthorityStateRequest,
    _control: None = Depends(require_experimental_authority_control),
) -> AuthorityTransition | None:
    return set_current_runtime_state(
        authority_valid=request.authority_valid,
    )


@app.post("/decide")
def decide(
    request: DecisionRequest,
    runtime_state: RuntimeState = Depends(get_current_runtime_state),
) -> DecisionResponse:
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

        current = runtime_state.authority_valid
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

    response = DecisionResponse(
        outcome=outcome,
        evidence=DecisionEvidence(
            record_id=uuid4(),
            created_at=datetime.now(timezone.utc),
            schema_version="1",
            action_proposal=request.action_proposal,
            prior_decision_id=request.prior_decision.decision_id,
            revalidation_mode=request.revalidation_mode,
            obligation_evaluations=evaluations,
        ),
    )

    decision_records[response.evidence.record_id] = response

    return response


@app.get("/records/{record_id}")
def get_record(record_id: UUID) -> DecisionResponse:
    record = decision_records.get(record_id)

    if record is None:
        raise HTTPException(status_code=404, detail="Decision record not found")

    return record


@app.get("/authority-transitions/{transition_id}")
def get_authority_transition(transition_id: UUID) -> AuthorityTransition:
    transition = authority_transitions.get(transition_id)

    if transition is None:
        raise HTTPException(status_code=404, detail="Authority transition not found")

    return transition