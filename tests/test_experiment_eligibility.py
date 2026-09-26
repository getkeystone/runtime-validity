import inspect
from dataclasses import fields

import pytest

from runtime_validity._experiment_mapping import (
    EligibilityValue,
    MappingResult,
    derive_eligibility,
)
from runtime_validity._experiment_observation import (
    Observation,
    ObservationFailureReason,
    ObservationStatus,
)


def available_eligibility_observation(
    *, authorizing_path_id: str, authorizing_path_live: bool
) -> Observation[EligibilityValue]:
    return Observation(
        observation_attempted=True,
        observation_status=ObservationStatus.AVAILABLE,
        observed_value=EligibilityValue(
            authorizing_path_id=authorizing_path_id,
            authorizing_path_live=authorizing_path_live,
        ),
    )


def test_deliberate_non_observation_derives_not_evaluated() -> None:
    result = derive_eligibility(
        expected_authorizing_path_id="path-A",
        observation=Observation[EligibilityValue](observation_attempted=False),
    )

    assert result is MappingResult.NOT_EVALUATED


def test_unavailable_observation_derives_non_evaluable() -> None:
    result = derive_eligibility(
        expected_authorizing_path_id="path-A",
        observation=Observation[EligibilityValue](
            observation_attempted=True,
            observation_status=ObservationStatus.UNAVAILABLE,
            observation_failure_reason=(
                ObservationFailureReason.OBSERVATION_SOURCE_MISSING
            ),
        ),
    )

    assert result is MappingResult.NON_EVALUABLE


def test_same_path_live_derives_preserved() -> None:
    result = derive_eligibility(
        expected_authorizing_path_id="path-A",
        observation=available_eligibility_observation(
            authorizing_path_id="path-A",
            authorizing_path_live=True,
        ),
    )

    assert result is MappingResult.PRESERVED


def test_same_path_not_live_derives_invalidated() -> None:
    result = derive_eligibility(
        expected_authorizing_path_id="path-A",
        observation=available_eligibility_observation(
            authorizing_path_id="path-A",
            authorizing_path_live=False,
        ),
    )

    assert result is MappingResult.INVALIDATED


def test_different_authorizing_path_id_is_rejected() -> None:
    observation = available_eligibility_observation(
        authorizing_path_id="path-B",
        authorizing_path_live=False,
    )

    with pytest.raises(ValueError, match="retain authorizing path identity"):
        derive_eligibility(
            expected_authorizing_path_id="path-A",
            observation=observation,
        )


def test_available_observation_rejects_non_eligibility_payload() -> None:
    observation = Observation(
        observation_attempted=True,
        observation_status=ObservationStatus.AVAILABLE,
        observed_value="not-an-eligibility-value",
    )

    with pytest.raises(ValueError, match="requires an eligibility value"):
        derive_eligibility(
            expected_authorizing_path_id="path-A",
            observation=observation,  # type: ignore[arg-type]
        )


def test_eligibility_value_rejects_integer_liveness() -> None:
    with pytest.raises(ValueError, match="authorizing_path_live must be a bool"):
        EligibilityValue(
            authorizing_path_id="path-A",
            authorizing_path_live=1,  # type: ignore[arg-type]
        )


def test_eligibility_value_rejects_string_liveness() -> None:
    with pytest.raises(ValueError, match="authorizing_path_live must be a bool"):
        EligibilityValue(
            authorizing_path_id="path-A",
            authorizing_path_live="true",  # type: ignore[arg-type]
        )


def test_identical_eligibility_inputs_produce_identical_result() -> None:
    observation = available_eligibility_observation(
        authorizing_path_id="path-A",
        authorizing_path_live=True,
    )

    first = derive_eligibility(
        expected_authorizing_path_id="path-A",
        observation=observation,
    )
    second = derive_eligibility(
        expected_authorizing_path_id="path-A",
        observation=observation,
    )

    assert first is second is MappingResult.PRESERVED


def test_unavailable_failure_reason_does_not_change_mapping_result() -> None:
    source_missing = Observation[EligibilityValue](
        observation_attempted=True,
        observation_status=ObservationStatus.UNAVAILABLE,
        observation_failure_reason=(
            ObservationFailureReason.OBSERVATION_SOURCE_MISSING
        ),
    )
    incomplete = Observation[EligibilityValue](
        observation_attempted=True,
        observation_status=ObservationStatus.UNAVAILABLE,
        observation_failure_reason=ObservationFailureReason.INCOMPLETE,
    )

    source_missing_result = derive_eligibility(
        expected_authorizing_path_id="path-A",
        observation=source_missing,
    )
    incomplete_result = derive_eligibility(
        expected_authorizing_path_id="path-A",
        observation=incomplete,
    )

    assert source_missing_result is MappingResult.NON_EVALUABLE
    assert incomplete_result is MappingResult.NON_EVALUABLE


def test_eligibility_interface_has_no_scenario_or_expected_result_input() -> None:
    assert tuple(inspect.signature(derive_eligibility).parameters) == (
        "expected_authorizing_path_id",
        "observation",
    )


def test_eligibility_representation_requires_only_path_id_and_liveness() -> None:
    assert tuple(field.name for field in fields(EligibilityValue)) == (
        "authorizing_path_id",
        "authorizing_path_live",
    )


def test_eligibility_value_rejects_non_string_path_id() -> None:
    with pytest.raises(ValueError, match="authorizing_path_id must be a string"):
        EligibilityValue(
            authorizing_path_id=1,  # type: ignore[arg-type]
            authorizing_path_live=True,
        )


def test_eligibility_derivation_rejects_non_string_expected_path_id() -> None:
    observation = available_eligibility_observation(
        authorizing_path_id="path-A",
        authorizing_path_live=True,
    )

    with pytest.raises(
        ValueError, match="expected authorizing_path_id must be a string"
    ):
        derive_eligibility(
            expected_authorizing_path_id=1,  # type: ignore[arg-type]
            observation=observation,
        )
