import pytest

from runtime_validity._experiment_observation import (
    Observation,
    ObservationFailureReason,
    ObservationStatus,
)


def test_deliberate_non_observation_is_valid_without_observation_data() -> None:
    observation = Observation[object](observation_attempted=False)

    assert observation.observation_status is None
    assert observation.observation_failure_reason is None
    assert observation.observed_value is None


def test_deliberate_non_observation_rejects_available_status() -> None:
    with pytest.raises(ValueError):
        Observation[object](
            observation_attempted=False,
            observation_status=ObservationStatus.AVAILABLE,
        )


def test_deliberate_non_observation_rejects_unavailable_status() -> None:
    with pytest.raises(ValueError):
        Observation[object](
            observation_attempted=False,
            observation_status=ObservationStatus.UNAVAILABLE,
        )


def test_deliberate_non_observation_rejects_observed_value() -> None:
    with pytest.raises(ValueError):
        Observation(observation_attempted=False, observed_value="witness")


def test_deliberate_non_observation_rejects_failure_reason() -> None:
    with pytest.raises(ValueError):
        Observation[object](
            observation_attempted=False,
            observation_failure_reason=(
                ObservationFailureReason.OBSERVATION_SOURCE_MISSING
            ),
        )


def test_attempted_available_observation_with_value_is_valid() -> None:
    observation = Observation(
        observation_attempted=True,
        observation_status=ObservationStatus.AVAILABLE,
        observed_value="witness",
    )

    assert observation.observed_value == "witness"
    assert observation.observation_failure_reason is None


def test_attempted_available_observation_rejects_missing_value() -> None:
    with pytest.raises(ValueError):
        Observation[object](
            observation_attempted=True,
            observation_status=ObservationStatus.AVAILABLE,
        )


def test_attempted_available_observation_rejects_failure_reason() -> None:
    with pytest.raises(ValueError):
        Observation(
            observation_attempted=True,
            observation_status=ObservationStatus.AVAILABLE,
            observation_failure_reason=(
                ObservationFailureReason.OBSERVATION_SOURCE_MISSING
            ),
            observed_value="witness",
        )


def test_attempted_unavailable_observation_with_failure_reason_is_valid() -> None:
    observation = Observation[object](
        observation_attempted=True,
        observation_status=ObservationStatus.UNAVAILABLE,
        observation_failure_reason=(
            ObservationFailureReason.OBSERVATION_SOURCE_MISSING
        ),
    )

    assert observation.observed_value is None
    assert (
        observation.observation_failure_reason
        is ObservationFailureReason.OBSERVATION_SOURCE_MISSING
    )


def test_attempted_unavailable_observation_rejects_observed_value() -> None:
    with pytest.raises(ValueError):
        Observation(
            observation_attempted=True,
            observation_status=ObservationStatus.UNAVAILABLE,
            observation_failure_reason=(
                ObservationFailureReason.OBSERVATION_SOURCE_MISSING
            ),
            observed_value="witness",
        )


def test_attempted_unavailable_observation_rejects_missing_failure_reason() -> None:
    with pytest.raises(ValueError):
        Observation[object](
            observation_attempted=True,
            observation_status=ObservationStatus.UNAVAILABLE,
        )


def test_attempted_observation_rejects_missing_status() -> None:
    with pytest.raises(ValueError):
        Observation(observation_attempted=True, observed_value="witness")


def test_unavailable_observation_rejects_unbounded_failure_reason() -> None:
    with pytest.raises(ValueError):
        Observation[object](
            observation_attempted=True,
            observation_status=ObservationStatus.UNAVAILABLE,
            observation_failure_reason="UNKNOWN",  # type: ignore[arg-type]
        )


def test_observation_rejects_non_boolean_attempted_value() -> None:
    with pytest.raises(ValueError):
        Observation(
            observation_attempted=1,  # type: ignore[arg-type]
            observation_status=ObservationStatus.AVAILABLE,
            observed_value="witness",
        )


def test_observation_rejects_raw_unavailable_status() -> None:
    with pytest.raises(ValueError):
        Observation[object](
            observation_attempted=True,
            observation_status="UNAVAILABLE",  # type: ignore[arg-type]
            observation_failure_reason=(
                ObservationFailureReason.OBSERVATION_SOURCE_MISSING
            ),
        )
