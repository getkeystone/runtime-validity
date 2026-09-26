import ast
import inspect

import pytest

import runtime_validity._experiment_mapping as experiment_mapping
from runtime_validity._experiment_mapping import (
    FreshnessValue,
    MappingResult,
    derive_freshness,
)
from runtime_validity._experiment_observation import (
    Observation,
    ObservationFailureReason,
    ObservationStatus,
)


def available_freshness_observation(
    *, witness_id: str, age: int
) -> Observation[FreshnessValue]:
    return Observation(
        observation_attempted=True,
        observation_status=ObservationStatus.AVAILABLE,
        observed_value=FreshnessValue(witness_id=witness_id, age=age),
    )


def test_mapping_result_contains_only_frozen_experiment_results() -> None:
    assert {result.value for result in MappingResult} == {
        "PRESERVED",
        "INVALIDATED",
        "NON_EVALUABLE",
        "NOT_EVALUATED",
    }


def test_deliberate_non_observation_derives_not_evaluated() -> None:
    result = derive_freshness(
        expected_witness_id="witness-A",
        maximum_age=2,
        observation=Observation[FreshnessValue](observation_attempted=False),
    )

    assert result is MappingResult.NOT_EVALUATED


def test_unavailable_observation_derives_non_evaluable() -> None:
    result = derive_freshness(
        expected_witness_id="witness-A",
        maximum_age=2,
        observation=Observation[FreshnessValue](
            observation_attempted=True,
            observation_status=ObservationStatus.UNAVAILABLE,
            observation_failure_reason=(
                ObservationFailureReason.OBSERVATION_SOURCE_MISSING
            ),
        ),
    )

    assert result is MappingResult.NON_EVALUABLE


def test_same_witness_below_maximum_age_derives_preserved() -> None:
    result = derive_freshness(
        expected_witness_id="witness-A",
        maximum_age=2,
        observation=available_freshness_observation(
            witness_id="witness-A", age=1
        ),
    )

    assert result is MappingResult.PRESERVED


def test_same_witness_at_maximum_age_derives_preserved() -> None:
    result = derive_freshness(
        expected_witness_id="witness-A",
        maximum_age=2,
        observation=available_freshness_observation(
            witness_id="witness-A", age=2
        ),
    )

    assert result is MappingResult.PRESERVED


def test_same_witness_above_maximum_age_derives_invalidated() -> None:
    result = derive_freshness(
        expected_witness_id="witness-A",
        maximum_age=2,
        observation=available_freshness_observation(
            witness_id="witness-A", age=3
        ),
    )

    assert result is MappingResult.INVALIDATED


def test_different_witness_identity_is_rejected() -> None:
    observation = available_freshness_observation(
        witness_id="witness-B", age=3
    )

    with pytest.raises(ValueError, match="retain witness identity"):
        derive_freshness(
            expected_witness_id="witness-A",
            maximum_age=2,
            observation=observation,
        )


def test_identical_freshness_inputs_produce_identical_result() -> None:
    observation = available_freshness_observation(
        witness_id="witness-A", age=2
    )

    first = derive_freshness(
        expected_witness_id="witness-A",
        maximum_age=2,
        observation=observation,
    )
    second = derive_freshness(
        expected_witness_id="witness-A",
        maximum_age=2,
        observation=observation,
    )

    assert first is second is MappingResult.PRESERVED


def test_unavailable_failure_reason_does_not_change_mapping_result() -> None:
    source_missing = Observation[FreshnessValue](
        observation_attempted=True,
        observation_status=ObservationStatus.UNAVAILABLE,
        observation_failure_reason=(
            ObservationFailureReason.OBSERVATION_SOURCE_MISSING
        ),
    )
    malformed = Observation[FreshnessValue](
        observation_attempted=True,
        observation_status=ObservationStatus.UNAVAILABLE,
        observation_failure_reason=ObservationFailureReason.MALFORMED,
    )

    source_missing_result = derive_freshness(
        expected_witness_id="witness-A",
        maximum_age=2,
        observation=source_missing,
    )
    malformed_result = derive_freshness(
        expected_witness_id="witness-A",
        maximum_age=2,
        observation=malformed,
    )

    assert source_missing_result is MappingResult.NON_EVALUABLE
    assert malformed_result is MappingResult.NON_EVALUABLE


def test_derivation_interface_has_no_scenario_or_expected_result_input() -> None:
    assert tuple(inspect.signature(derive_freshness).parameters) == (
        "expected_witness_id",
        "maximum_age",
        "observation",
    )


def test_freshness_module_has_no_wall_clock_import() -> None:
    tree = ast.parse(inspect.getsource(experiment_mapping))
    imported_modules = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported_modules.update(
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    )

    assert "time" not in imported_modules
    assert "datetime" not in imported_modules


def test_available_observation_rejects_non_freshness_payload() -> None:
    observation = Observation(
        observation_attempted=True,
        observation_status=ObservationStatus.AVAILABLE,
        observed_value="not-a-freshness-value",
    )

    with pytest.raises(ValueError, match="requires a freshness value"):
        derive_freshness(
            expected_witness_id="witness-A",
            maximum_age=2,
            observation=observation,  # type: ignore[arg-type]
        )


def test_freshness_value_rejects_boolean_age() -> None:
    with pytest.raises(ValueError, match="integer/logical units"):
        FreshnessValue(witness_id="witness-A", age=True)


def test_freshness_value_rejects_floating_point_age() -> None:
    with pytest.raises(ValueError, match="integer/logical units"):
        FreshnessValue(witness_id="witness-A", age=1.0)  # type: ignore[arg-type]


def test_freshness_derivation_rejects_boolean_maximum_age() -> None:
    observation = available_freshness_observation(
        witness_id="witness-A", age=1
    )

    with pytest.raises(ValueError, match="integer/logical units"):
        derive_freshness(
            expected_witness_id="witness-A",
            maximum_age=True,
            observation=observation,
        )


def test_freshness_derivation_rejects_floating_point_maximum_age() -> None:
    observation = available_freshness_observation(
        witness_id="witness-A", age=1
    )

    with pytest.raises(ValueError, match="integer/logical units"):
        derive_freshness(
            expected_witness_id="witness-A",
            maximum_age=2.0,  # type: ignore[arg-type]
            observation=observation,
        )
