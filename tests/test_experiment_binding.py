import inspect
from dataclasses import fields

import pytest

from runtime_validity._experiment_mapping import (
    BindingValue,
    MappingResult,
    derive_binding,
)
from runtime_validity._experiment_observation import (
    Observation,
    ObservationFailureReason,
    ObservationStatus,
)


def available_binding_observation(effect_id: str) -> Observation[BindingValue]:
    return Observation(
        observation_attempted=True,
        observation_status=ObservationStatus.AVAILABLE,
        observed_value=BindingValue(effect_id=effect_id),
    )


def test_deliberate_non_observation_derives_not_evaluated() -> None:
    result = derive_binding(
        expected_effect_id="effect-A",
        observation=Observation[BindingValue](observation_attempted=False),
    )

    assert result is MappingResult.NOT_EVALUATED


def test_unavailable_observation_derives_non_evaluable() -> None:
    result = derive_binding(
        expected_effect_id="effect-A",
        observation=Observation[BindingValue](
            observation_attempted=True,
            observation_status=ObservationStatus.UNAVAILABLE,
            observation_failure_reason=(
                ObservationFailureReason.OBSERVATION_SOURCE_MISSING
            ),
        ),
    )

    assert result is MappingResult.NON_EVALUABLE


def test_same_effect_id_derives_preserved() -> None:
    result = derive_binding(
        expected_effect_id="effect-A",
        observation=available_binding_observation("effect-A"),
    )

    assert result is MappingResult.PRESERVED


def test_different_effect_id_derives_invalidated_without_rejection() -> None:
    result = derive_binding(
        expected_effect_id="effect-A",
        observation=available_binding_observation("effect-B"),
    )

    assert result is MappingResult.INVALIDATED


def test_available_observation_rejects_non_binding_payload() -> None:
    observation = Observation(
        observation_attempted=True,
        observation_status=ObservationStatus.AVAILABLE,
        observed_value="not-a-binding-value",
    )

    with pytest.raises(ValueError, match="requires a binding value"):
        derive_binding(
            expected_effect_id="effect-A",
            observation=observation,  # type: ignore[arg-type]
        )


def test_identical_binding_inputs_produce_identical_result() -> None:
    observation = available_binding_observation("effect-A")

    first = derive_binding(
        expected_effect_id="effect-A",
        observation=observation,
    )
    second = derive_binding(
        expected_effect_id="effect-A",
        observation=observation,
    )

    assert first is second is MappingResult.PRESERVED


def test_unavailable_failure_reason_does_not_change_mapping_result() -> None:
    source_missing = Observation[BindingValue](
        observation_attempted=True,
        observation_status=ObservationStatus.UNAVAILABLE,
        observation_failure_reason=(
            ObservationFailureReason.OBSERVATION_SOURCE_MISSING
        ),
    )
    inaccessible = Observation[BindingValue](
        observation_attempted=True,
        observation_status=ObservationStatus.UNAVAILABLE,
        observation_failure_reason=ObservationFailureReason.INACCESSIBLE,
    )

    source_missing_result = derive_binding(
        expected_effect_id="effect-A",
        observation=source_missing,
    )
    inaccessible_result = derive_binding(
        expected_effect_id="effect-A",
        observation=inaccessible,
    )

    assert source_missing_result is MappingResult.NON_EVALUABLE
    assert inaccessible_result is MappingResult.NON_EVALUABLE


def test_binding_interface_has_no_scenario_or_expected_result_input() -> None:
    assert tuple(inspect.signature(derive_binding).parameters) == (
        "expected_effect_id",
        "observation",
    )


def test_binding_representation_requires_no_target_path_or_policy_state() -> None:
    assert tuple(field.name for field in fields(BindingValue)) == ("effect_id",)


def test_binding_value_rejects_non_string_effect_id() -> None:
    with pytest.raises(ValueError, match="effect_id must be a string"):
        BindingValue(effect_id=1)  # type: ignore[arg-type]


def test_binding_derivation_rejects_non_string_expected_effect_id() -> None:
    observation = available_binding_observation("effect-A")

    with pytest.raises(ValueError, match="expected effect_id must be a string"):
        derive_binding(
            expected_effect_id=1,  # type: ignore[arg-type]
            observation=observation,
        )
