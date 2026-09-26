from dataclasses import dataclass
from enum import StrEnum

from runtime_validity._experiment_observation import Observation, ObservationStatus


class MappingResult(StrEnum):
    PRESERVED = "PRESERVED"
    INVALIDATED = "INVALIDATED"
    NON_EVALUABLE = "NON_EVALUABLE"
    NOT_EVALUATED = "NOT_EVALUATED"


@dataclass(frozen=True, slots=True)
class FreshnessValue:
    witness_id: str
    age: int

    def __post_init__(self) -> None:
        if type(self.age) is not int:
            raise ValueError("freshness age must use integer/logical units")


@dataclass(frozen=True, slots=True)
class BindingValue:
    effect_id: str

    def __post_init__(self) -> None:
        if type(self.effect_id) is not str:
            raise ValueError("binding effect_id must be a string")


@dataclass(frozen=True, slots=True)
class EligibilityValue:
    authorizing_path_id: str
    authorizing_path_live: bool

    def __post_init__(self) -> None:
        if type(self.authorizing_path_id) is not str:
            raise ValueError("authorizing_path_id must be a string")
        if type(self.authorizing_path_live) is not bool:
            raise ValueError("authorizing_path_live must be a bool")


def derive_freshness(
    *,
    expected_witness_id: str,
    maximum_age: int,
    observation: Observation[FreshnessValue],
) -> MappingResult:
    if type(maximum_age) is not int:
        raise ValueError("maximum age must use integer/logical units")

    if not observation.observation_attempted:
        return MappingResult.NOT_EVALUATED

    if observation.observation_status is ObservationStatus.UNAVAILABLE:
        return MappingResult.NON_EVALUABLE

    value = observation.observed_value
    if not isinstance(value, FreshnessValue):
        raise ValueError("available freshness observation requires a freshness value")

    if value.witness_id != expected_witness_id:
        raise ValueError("freshness observation must retain witness identity")

    if value.age <= maximum_age:
        return MappingResult.PRESERVED

    return MappingResult.INVALIDATED


def derive_binding(
    *,
    expected_effect_id: str,
    observation: Observation[BindingValue],
) -> MappingResult:
    if type(expected_effect_id) is not str:
        raise ValueError("expected effect_id must be a string")

    if not observation.observation_attempted:
        return MappingResult.NOT_EVALUATED

    if observation.observation_status is ObservationStatus.UNAVAILABLE:
        return MappingResult.NON_EVALUABLE

    value = observation.observed_value
    if not isinstance(value, BindingValue):
        raise ValueError("available binding observation requires a binding value")

    if value.effect_id == expected_effect_id:
        return MappingResult.PRESERVED

    return MappingResult.INVALIDATED


def derive_eligibility(
    *,
    expected_authorizing_path_id: str,
    observation: Observation[EligibilityValue],
) -> MappingResult:
    if type(expected_authorizing_path_id) is not str:
        raise ValueError("expected authorizing_path_id must be a string")

    if not observation.observation_attempted:
        return MappingResult.NOT_EVALUATED

    if observation.observation_status is ObservationStatus.UNAVAILABLE:
        return MappingResult.NON_EVALUABLE

    value = observation.observed_value
    if not isinstance(value, EligibilityValue):
        raise ValueError("available eligibility observation requires an eligibility value")

    if value.authorizing_path_id != expected_authorizing_path_id:
        raise ValueError("eligibility observation must retain authorizing path identity")

    if value.authorizing_path_live:
        return MappingResult.PRESERVED

    return MappingResult.INVALIDATED
