from fastapi.testclient import TestClient

from track_a.api import app


client = TestClient(app)


def test_decide_returns_proceed_for_valid_request() -> None:
    response = client.post(
        "/decide",
        json={
            "action_proposal": "send customer notification",
            "prior_decision_id": "decision-123",
            "revalidation_mode": "full",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"outcome": "PROCEED"}


def test_decide_rejects_invalid_revalidation_mode() -> None:
    response = client.post(
        "/decide",
        json={
            "action_proposal": "send customer notification",
            "prior_decision_id": "decision-123",
            "revalidation_mode": "sometimes",
        },
    )

    assert response.status_code == 422