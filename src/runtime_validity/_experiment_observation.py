from dataclasses import dataclass
from enum import StrEnum
from typing import Generic, TypeVar


class ObservationStatus(StrEnum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"


class ObservationFailureReason(StrEnum):
    OBSERVATION_SOURCE_MISSING = "OBSERVATION_SOURCE_MISSING"
    INACCESSIBLE = "INACCESSIBLE"
    MALFORMED = "MALFORMED"
    INCOMPLETE = "INCOMPLETE"
    OTHER_DECLARED_FAILURE = "OTHER_DECLARED_FAILURE"


ObservedValue = TypeVar("ObservedValue")


@dataclass(frozen=True, slots=True)
class Observation(Generic[ObservedValue]):
    observation_attempted: bool
    observation_status: ObservationStatus | None = None
    observation_failure_reason: ObservationFailureReason | None = None
    observed_value: ObservedValue | None = None

    def __post_init__(self) -> None:
        if type(self.observation_attempted) is not bool:
            raise ValueError("observation_attempted must be a bool")

        if not self.observation_attempted:
            if self.observation_status is not None:
                raise ValueError("unattempted observation cannot have a status")
            if self.observation_failure_reason is not None:
                raise ValueError(
                    "unattempted observation cannot have a failure reason"
                )
            if self.observed_value is not None:
                raise ValueError("unattempted observation cannot have a value")
            return

        if self.observation_status is None:
            raise ValueError("attempted observation requires a status")
        if not isinstance(self.observation_status, ObservationStatus):
            raise ValueError("observation_status must be bounded")

        if self.observation_status is ObservationStatus.AVAILABLE:
            if self.observed_value is None:
                raise ValueError("available observation requires a value")
            if self.observation_failure_reason is not None:
                raise ValueError(
                    "available observation cannot have a failure reason"
                )
            return

        if self.observed_value is not None:
            raise ValueError("unavailable observation cannot have a value")
        if self.observation_failure_reason is None:
            raise ValueError(
                "unavailable observation requires a failure reason"
            )
        if not isinstance(
            self.observation_failure_reason, ObservationFailureReason
        ):
            raise ValueError("observation failure reason must be bounded")
