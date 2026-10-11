"""Unified execution contract for the security-test architecture.

This module executes one already-selected domain adapter operation and returns
its observations in a common result object. Test selection, scheduling,
coordination, retries, and overall run orchestration belong to the runner.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping

from a_framework.domain_adapter import DomainAdapter
from a_framework.test_architecture import ExecutionStatus, Observation


def _utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


@dataclass(frozen=True, slots=True)
class ExecutionOutcome:
    """Outcome of one adapter operation, before test evaluation.
    ``observations`` contains domain output normalized by the adapter. This
    object is deliberately not a ``TestResult``: it does not express PASS/FAIL
    evaluation.
    """

    status: ExecutionStatus
    observations: tuple[Observation, ...] = ()
    started_at: datetime = field(default_factory=_utc_now)
    completed_at: datetime = field(default_factory=_utc_now)
    error: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.status, ExecutionStatus):
            try:
                object.__setattr__(
                    self, "status", ExecutionStatus(self.status)
                )
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    "status must be a valid ExecutionStatus"
                ) from exc

        if self.started_at.tzinfo is None or self.completed_at.tzinfo is None:
            raise ValueError("execution timestamps must be timezone-aware")

        if self.completed_at < self.started_at:
            raise ValueError("completed_at cannot precede started_at")

        object.__setattr__(self, "observations", tuple(self.observations))

        if not all(
            isinstance(item, Observation) for item in self.observations
        ):
            raise TypeError(
                "observations must contain only Observation instances"
            )

        object.__setattr__(self, "metadata", dict(self.metadata))

        if self.status == ExecutionStatus.FAILED and not self.error:
            raise ValueError(
                "a failed execution outcome must include an error"
            )

        if self.status != ExecutionStatus.FAILED and self.error is not None:
            raise ValueError(
                "error is only valid for a failed execution outcome"
            )

    @property
    def duration_seconds(self) -> float:
        """Elapsed time for this adapter operation in seconds."""
        return (self.completed_at - self.started_at).total_seconds()


class ExecutionInterface(ABC):
    """Contract for executing one operation through a selected domain adapter.

    Implementations must not choose test cases or adapters, schedule multiple
    operations, evaluate observations, or create evidence records.
    """

    @abstractmethod
    def execute(
        self,
        adapter: DomainAdapter,
        inputs: Mapping[str, Any],
    ) -> ExecutionOutcome:
        """Execute one adapter operation and return a normalized outcome."""
        raise NotImplementedError


class AdapterExecutionInterface(ExecutionInterface):
    """Default execution-interface implementation for ``DomainAdapter``."""

    def execute(
        self,
        adapter: DomainAdapter,
        inputs: Mapping[str, Any],
    ) -> ExecutionOutcome:
        if not isinstance(adapter, DomainAdapter):
            raise TypeError("adapter must be a DomainAdapter instance")

        if not isinstance(inputs, Mapping):
            raise TypeError("inputs must be a mapping")

        started_at = _utc_now()

        try:
            raw_output = adapter.run(dict(inputs))
            observation = adapter.get_observation(raw_output)

            if not isinstance(observation, Observation):
                raise TypeError(
                    "adapter.get_observation() must return an Observation instance"
                )


        except Exception as exc:
            completed_at = _utc_now()

            if adapter.status != ExecutionStatus.FAILED:
                adapter.mark_failed()

            return ExecutionOutcome(
                status=ExecutionStatus.FAILED,
                started_at=started_at,
                completed_at=max(completed_at, started_at),
                error=f"{type(exc).__name__}: {exc}",
                metadata={"domain": adapter.domain},
            )

        completed_at = _utc_now()

        return ExecutionOutcome(
            status=ExecutionStatus.COMPLETED,
            observations=(observation,),
            started_at=started_at,
            completed_at=max(completed_at, started_at),
            metadata={"domain": adapter.domain},
        )


__all__ = [
    "AdapterExecutionInterface",
    "ExecutionInterface",
    "ExecutionOutcome",
]