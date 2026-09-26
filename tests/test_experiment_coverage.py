import inspect
from dataclasses import fields

import pytest

from runtime_validity._experiment_mapping import (
    CoverageValue,
    MappingResult,
    derive_coverage,
)
from runtime_validity._experiment_observation import (
    Observation,
    ObservationFailureReason,
    ObservationStatus,
)


def available_coverage_observation(
    present_witness_ids: frozenset[str],
) -> Observation[CoverageValue]:
    return Observation(
        observation_attempted=True,
        observation_status=ObservationStatus.AVAILABLE,
        observed_value=CoverageValue(present_witness_ids=present_witness_ids),
    )


def test_deliberate_non_observation_derives_not_evaluated() -> None:
    result = derive_coverage(
        required_witness_ids=frozenset({"W1", "W2"}),
        observation=Observation[CoverageValue](observation_attempted=False),
    )

    assert result is MappingResult.NOT_EVALUATED


def test_unavailable_observation_derives_non_evaluable() -> None:
    result = derive_coverage(
        required_witness_ids=frozenset({"W1", "W2"}),
        observation=Observation[CoverageValue](
            observation_attempted=True,
            observation_status=ObservationStatus.UNAVAILABLE,
            observation_failure_reason=(
                ObservationFailureReason.OBSERVATION_SOURCE_MISSING
            ),
        ),
    )

    assert result is MappingResult.NON_EVALUABLE


def test_all_required_witnesses_present_derives_preserved() -> None:
    result = derive_coverage(
        required_witness_ids=frozenset({"W1", "W2"}),
        observation=available_coverage_observation(frozenset({"W1", "W2"})),
    )

    assert result is MappingResult.PRESERVED


def test_missing_second_required_witness_derives_invalidated() -> None:
    result = derive_coverage(
        required_witness_ids=frozenset({"W1", "W2"}),
        observation=available_coverage_observation(frozenset({"W1"})),
    )

    assert result is MappingResult.INVALIDATED


def test_missing_first_required_witness_derives_invalidated() -> None:
    result = derive_coverage(
        required_witness_ids=frozenset({"W1", "W2"}),
        observation=available_coverage_observation(frozenset({"W2"})),
    )

    assert result is MappingResult.INVALIDATED


def test_available_empty_inventory_derives_invalidated() -> None:
    result = derive_coverage(
        required_witness_ids=frozenset({"W1", "W2"}),
        observation=available_coverage_observation(frozenset()),
    )

    assert result is MappingResult.INVALIDATED


def test_extra_present_witnesses_do_not_invalidate_coverage() -> None:
    result = derive_coverage(
        required_witness_ids=frozenset({"W1", "W2"}),
        observation=available_coverage_observation(
            frozenset({"W1", "W2", "W3"})
        ),
    )

    assert result is MappingResult.PRESERVED


def test_unavailable_inventory_is_distinct_from_available_empty_inventory() -> None:
    unavailable = Observation[CoverageValue](
        observation_attempted=True,
        observation_status=ObservationStatus.UNAVAILABLE,
        observation_failure_reason=(
            ObservationFailureReason.OBSERVATION_SOURCE_MISSING
        ),
    )

    unavailable_result = derive_coverage(
        required_witness_ids=frozenset({"W1", "W2"}),
        observation=unavailable,
    )
    empty_result = derive_coverage(
        required_witness_ids=frozenset({"W1", "W2"}),
        observation=available_coverage_observation(frozenset()),
    )

    assert unavailable_result is MappingResult.NON_EVALUABLE
    assert empty_result is MappingResult.INVALIDATED


def test_available_observation_rejects_non_coverage_payload() -> None:
    observation = Observation(
        observation_attempted=True,
        observation_status=ObservationStatus.AVAILABLE,
        observed_value=frozenset({"W1", "W2"}),
    )

    with pytest.raises(ValueError, match="requires a coverage value"):
        derive_coverage(
            required_witness_ids=frozenset({"W1", "W2"}),
            observation=observation,  # type: ignore[arg-type]
        )


def test_identical_coverage_inputs_produce_identical_result() -> None:
    observation = available_coverage_observation(frozenset({"W1", "W2"}))

    first = derive_coverage(
        required_witness_ids=frozenset({"W1", "W2"}),
        observation=observation,
    )
    second = derive_coverage(
        required_witness_ids=frozenset({"W1", "W2"}),
        observation=observation,
    )

    assert first is second is MappingResult.PRESERVED


def test_unavailable_failure_reason_does_not_change_mapping_result() -> None:
    source_missing = Observation[CoverageValue](
        observation_attempted=True,
        observation_status=ObservationStatus.UNAVAILABLE,
        observation_failure_reason=(
            ObservationFailureReason.OBSERVATION_SOURCE_MISSING
        ),
    )
    incomplete = Observation[CoverageValue](
        observation_attempted=True,
        observation_status=ObservationStatus.UNAVAILABLE,
        observation_failure_reason=ObservationFailureReason.INCOMPLETE,
    )

    source_missing_result = derive_coverage(
        required_witness_ids=frozenset({"W1", "W2"}),
        observation=source_missing,
    )
    incomplete_result = derive_coverage(
        required_witness_ids=frozenset({"W1", "W2"}),
        observation=incomplete,
    )

    assert source_missing_result is MappingResult.NON_EVALUABLE
    assert incomplete_result is MappingResult.NON_EVALUABLE


def test_coverage_interface_has_no_scenario_or_expected_result_input() -> None:
    assert tuple(inspect.signature(derive_coverage).parameters) == (
        "required_witness_ids",
        "observation",
    )


def test_coverage_representation_contains_only_present_witness_ids() -> None:
    assert tuple(field.name for field in fields(CoverageValue)) == (
        "present_witness_ids",
    )


def test_coverage_value_rejects_mutable_present_inventory() -> None:
    with pytest.raises(ValueError, match="must be a frozenset"):
        CoverageValue(present_witness_ids={"W1", "W2"})  # type: ignore[arg-type]


def test_coverage_value_rejects_non_string_present_witness_id() -> None:
    with pytest.raises(ValueError, match="present witness IDs must be strings"):
        CoverageValue(
            present_witness_ids=frozenset({"W1", 2}),  # type: ignore[arg-type]
        )


def test_coverage_derivation_rejects_mutable_required_inventory() -> None:
    observation = available_coverage_observation(frozenset({"W1", "W2"}))

    with pytest.raises(ValueError, match="must be a frozenset"):
        derive_coverage(
            required_witness_ids={"W1", "W2"},  # type: ignore[arg-type]
            observation=observation,
        )


def test_coverage_derivation_rejects_non_string_required_witness_id() -> None:
    observation = available_coverage_observation(frozenset({"W1", "W2"}))

    with pytest.raises(ValueError, match="required witness IDs must be strings"):
        derive_coverage(
            required_witness_ids=frozenset({"W1", 2}),  # type: ignore[arg-type]
            observation=observation,
        )


def test_empty_required_inventory_uses_subset_semantics() -> None:
    result = derive_coverage(
        required_witness_ids=frozenset(),
        observation=available_coverage_observation(frozenset()),
    )

    assert result is MappingResult.PRESERVED
