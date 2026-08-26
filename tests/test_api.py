from fastapi.testclient import TestClient

from track_a.api import app


client = TestClient(app)


def test_decide_returns_proceed_with_match_evidence() -> None:
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
                "authority_valid": True,
            },
            "revalidation_mode": "full",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "outcome": "PROCEED",
        "evidence": {
            "action_proposal": "send customer notification",
            "prior_decision_id": "decision-123",
            "revalidation_mode": "full",
            "obligation_evaluations": [
                {
                    "obligation_id": "authority-1",
                    "kind": "authority_valid",
                    "expected": True,
                    "current": True,
                    "result": "MATCH",
                }
            ],
        },
    }


def test_decide_returns_hold_with_mismatch_evidence() -> None:
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


def test_decide_rejects_missing_runtime_state() -> None:
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

    assert response.status_code == 422


def test_decide_rejects_malformed_authority_state() -> None:
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
                "authority_valid": "yes",
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
            "runtime_state": {
                "authority_valid": True,
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
            "runtime_state": {
                "authority_valid": True,
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
            "runtime_state": {
                "authority_valid": True,
            },
            "revalidation_mode": "full",
        },
    )

    assert response.status_code == 422