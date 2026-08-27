from collections.abc import Iterator
from datetime import datetime, timezone
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from runtime_validity.api import (
    RuntimeState,
    app,
    authority_transitions,
    get_current_runtime_state,
    set_current_runtime_state,
)


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_test_state() -> Iterator[None]:
    app.dependency_overrides.clear()

    set_current_runtime_state(authority_valid=True)
    authority_transitions.clear()

    yield

    set_current_runtime_state(authority_valid=True)
    authority_transitions.clear()

    app.dependency_overrides.clear()


def test_decide_returns_proceed_with_server_authority_match_evidence() -> None:
    app.dependency_overrides[get_current_runtime_state] = lambda: RuntimeState(
        authority_valid=True
    )

    response = client.post(
        "/decide",
        json={
            "action_proposal": "send customer notification",
            "prior_decision": {
                "decision_id": "decision-123",
                "outcome": "PROCEED",
                "obligations": [
                    {
                        "obligation_id": "authority-1",
                        "kind": "authority_valid",
                        "expected": True,
                    }
                ],
            },
            "revalidation_mode": "full",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["outcome"] == "PROCEED"
    assert body["evidence"]["action_proposal"] == "send customer notification"
    assert body["evidence"]["prior_decision_id"] == "decision-123"
    assert body["evidence"]["revalidation_mode"] == "full"
    assert body["evidence"]["obligation_evaluations"] == [
        {
            "obligation_id": "authority-1",
            "kind": "authority_valid",
            "expected": True,
            "current": True,
            "result": "MATCH",
        }
    ]


def test_decide_returns_hold_with_server_authority_mismatch_evidence() -> None:
    app.dependency_overrides[get_current_runtime_state] = lambda: RuntimeState(
        authority_valid=False
    )

    response = client.post(
        "/decide",
        json={
            "action_proposal": "send customer notification",
            "prior_decision": {
                "decision_id": "decision-123",
                "outcome": "PROCEED",
                "obligations": [
                    {
                        "obligation_id": "authority-1",
                        "kind": "authority_valid",
                        "expected": True,
                    }
                ],
            },
            "revalidation_mode": "full",
        },
    )

    assert response.status_code == 200
    assert response.json()["outcome"] == "HOLD"
    assert response.json()["evidence"]["obligation_evaluations"] == [
        {
            "obligation_id": "authority-1",
            "kind": "authority_valid",
            "expected": True,
            "current": False,
            "result": "MISMATCH",
        }
    ]


def test_decide_records_not_evaluated_when_revalidation_is_none() -> None:
    app.dependency_overrides[get_current_runtime_state] = lambda: RuntimeState(
        authority_valid=False
    )

    response = client.post(
        "/decide",
        json={
            "action_proposal": "send customer notification",
            "prior_decision": {
                "decision_id": "decision-123",
                "outcome": "PROCEED",
                "obligations": [
                    {
                        "obligation_id": "authority-1",
                        "kind": "authority_valid",
                        "expected": True,
                    }
                ],
            },
            "revalidation_mode": "none",
        },
    )

    assert response.status_code == 200
    assert response.json()["outcome"] == "PROCEED"
    assert response.json()["evidence"]["obligation_evaluations"] == [
        {
            "obligation_id": "authority-1",
            "kind": "authority_valid",
            "expected": True,
            "current": None,
            "result": "NOT_EVALUATED",
        }
    ]


def test_decide_returns_record_metadata() -> None:
    response = client.post(
        "/decide",
        json={
            "action_proposal": "send customer notification",
            "prior_decision": {
                "decision_id": "decision-123",
                "outcome": "PROCEED",
                "obligations": [
                    {
                        "obligation_id": "authority-1",
                        "kind": "authority_valid",
                        "expected": True,
                    }
                ],
            },
            "revalidation_mode": "full",
        },
    )

    assert response.status_code == 200

    evidence = response.json()["evidence"]

    UUID(evidence["record_id"])

    created_at = datetime.fromisoformat(
        evidence["created_at"].replace("Z", "+00:00")
    )

    assert created_at.utcoffset() is not None
    assert created_at.utcoffset().total_seconds() == 0
    assert evidence["schema_version"] == "1"


def test_decide_rejects_caller_supplied_runtime_state() -> None:
    response = client.post(
        "/decide",
        json={
            "action_proposal": "send customer notification",
            "prior_decision": {
                "decision_id": "decision-123",
                "outcome": "PROCEED",
                "obligations": [
                    {
                        "obligation_id": "authority-1",
                        "kind": "authority_valid",
                        "expected": True,
                    }
                ],
            },
            "runtime_state": {
                "authority_valid": False,
            },
            "revalidation_mode": "full",
        },
    )

    assert response.status_code == 422


def test_decide_rejects_invalid_revalidation_mode() -> None:
    response = client.post(
        "/decide",
        json={
            "action_proposal": "send customer notification",
            "prior_decision": {
                "decision_id": "decision-123",
                "outcome": "PROCEED",
                "obligations": [
                    {
                        "obligation_id": "authority-1",
                        "kind": "authority_valid",
                        "expected": True,
                    }
                ],
            },
            "revalidation_mode": "sometimes",
        },
    )

    assert response.status_code == 422


def test_decide_rejects_unsupported_obligation_kind() -> None:
    response = client.post(
        "/decide",
        json={
            "action_proposal": "send customer notification",
            "prior_decision": {
                "decision_id": "decision-123",
                "outcome": "PROCEED",
                "obligations": [
                    {
                        "obligation_id": "authority-1",
                        "kind": "whatever",
                        "expected": True,
                    }
                ],
            },
            "revalidation_mode": "full",
        },
    )

    assert response.status_code == 422


def test_decide_rejects_prior_decision_without_obligations() -> None:
    response = client.post(
        "/decide",
        json={
            "action_proposal": "send customer notification",
            "prior_decision": {
                "decision_id": "decision-123",
                "outcome": "PROCEED",
                "obligations": [],
            },
            "revalidation_mode": "full",
        },
    )

    assert response.status_code == 422


def test_decide_record_can_be_retrieved_by_record_id() -> None:
    create_response = client.post(
        "/decide",
        json={
            "action_proposal": "send customer notification",
            "prior_decision": {
                "decision_id": "decision-123",
                "outcome": "PROCEED",
                "obligations": [
                    {
                        "obligation_id": "authority-1",
                        "kind": "authority_valid",
                        "expected": True,
                    }
                ],
            },
            "revalidation_mode": "full",
        },
    )

    assert create_response.status_code == 200

    created_record = create_response.json()
    record_id = created_record["evidence"]["record_id"]

    retrieve_response = client.get(f"/records/{record_id}")

    assert retrieve_response.status_code == 200
    assert retrieve_response.json() == created_record


def test_get_record_returns_404_for_unknown_record_id() -> None:
    unknown_record_id = uuid4()

    response = client.get(f"/records/{unknown_record_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Decision record not found"}


def test_get_record_rejects_malformed_record_id() -> None:
    response = client.get("/records/not-a-uuid")

    assert response.status_code == 422


def test_full_revalidation_detects_authority_change_before_execution() -> None:
    set_current_runtime_state(authority_valid=True)

    request = {
        "action_proposal": "send customer notification",
        "prior_decision": {
            "decision_id": "decision-authority-change",
            "outcome": "PROCEED",
            "obligations": [
                {
                    "obligation_id": "authority-1",
                    "kind": "authority_valid",
                    "expected": True,
                }
            ],
        },
        "revalidation_mode": "full",
    }

    set_current_runtime_state(authority_valid=False)

    response = client.post("/decide", json=request)

    assert response.status_code == 200
    assert response.json()["outcome"] == "HOLD"
    assert response.json()["evidence"]["obligation_evaluations"] == [
        {
            "obligation_id": "authority-1",
            "kind": "authority_valid",
            "expected": True,
            "current": False,
            "result": "MISMATCH",
        }
    ]


def test_no_revalidation_does_not_evaluate_authority_change_before_execution() -> None:
    set_current_runtime_state(authority_valid=True)

    request = {
        "action_proposal": "send customer notification",
        "prior_decision": {
            "decision_id": "decision-authority-change",
            "outcome": "PROCEED",
            "obligations": [
                {
                    "obligation_id": "authority-1",
                    "kind": "authority_valid",
                    "expected": True,
                }
            ],
        },
        "revalidation_mode": "none",
    }

    set_current_runtime_state(authority_valid=False)

    response = client.post("/decide", json=request)

    assert response.status_code == 200
    assert response.json()["outcome"] == "PROCEED"
    assert response.json()["evidence"]["obligation_evaluations"] == [
        {
            "obligation_id": "authority-1",
            "kind": "authority_valid",
            "expected": True,
            "current": None,
            "result": "NOT_EVALUATED",
        }
    ]


def test_authority_change_creates_transition_record_with_metadata() -> None:
    transition = set_current_runtime_state(authority_valid=False)

    assert transition is not None

    assert isinstance(transition.transition_id, UUID)

    assert transition.occurred_at.utcoffset() is not None
    assert transition.occurred_at.utcoffset().total_seconds() == 0

    assert transition.previous_authority_valid is True
    assert transition.current_authority_valid is False


def test_authority_transition_can_be_retrieved_by_transition_id() -> None:
    transition = set_current_runtime_state(authority_valid=False)

    assert transition is not None

    response = client.get(
        f"/authority-transitions/{transition.transition_id}"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["transition_id"] == str(transition.transition_id)
    assert body["previous_authority_valid"] is True
    assert body["current_authority_valid"] is False

    occurred_at = datetime.fromisoformat(
        body["occurred_at"].replace("Z", "+00:00")
    )

    assert occurred_at == transition.occurred_at


def test_get_authority_transition_returns_404_for_unknown_transition_id() -> None:
    unknown_transition_id = uuid4()

    response = client.get(
        f"/authority-transitions/{unknown_transition_id}"
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Authority transition not found"
    }


def test_get_authority_transition_rejects_malformed_transition_id() -> None:
    response = client.get("/authority-transitions/not-a-uuid")

    assert response.status_code == 422


def test_setting_same_authority_value_creates_no_transition() -> None:
    transition = set_current_runtime_state(authority_valid=True)

    assert transition is None
    assert authority_transitions == {}


def test_retained_authority_transition_is_stable_after_later_change() -> None:
    first_transition = set_current_runtime_state(authority_valid=False)

    assert first_transition is not None

    first_transition_id = first_transition.transition_id
    first_occurred_at = first_transition.occurred_at

    second_transition = set_current_runtime_state(authority_valid=True)

    assert second_transition is not None
    assert second_transition.transition_id != first_transition_id
    assert second_transition.previous_authority_valid is False
    assert second_transition.current_authority_valid is True

    response = client.get(
        f"/authority-transitions/{first_transition_id}"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["transition_id"] == str(first_transition_id)
    assert body["previous_authority_valid"] is True
    assert body["current_authority_valid"] is False

    retrieved_occurred_at = datetime.fromisoformat(
        body["occurred_at"].replace("Z", "+00:00")
    )

    assert retrieved_occurred_at == first_occurred_at


def test_decide_rejects_caller_supplied_authority_transition() -> None:
    response = client.post(
        "/decide",
        json={
            "action_proposal": "send customer notification",
            "prior_decision": {
                "decision_id": "decision-123",
                "outcome": "PROCEED",
                "obligations": [
                    {
                        "obligation_id": "authority-1",
                        "kind": "authority_valid",
                        "expected": True,
                    }
                ],
            },
            "authority_transition": {
                "transition_id": str(uuid4()),
                "occurred_at": datetime.now(timezone.utc).isoformat(),
                "previous_authority_valid": True,
                "current_authority_valid": False,
            },
            "revalidation_mode": "full",
        },
    )

    assert response.status_code == 422
