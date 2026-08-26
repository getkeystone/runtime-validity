from datetime import datetime
from uuid import UUID, uuid4

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
            "runtime_state": {
                "authority_valid": True,
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
            "runtime_state": {
                "authority_valid": True,
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
