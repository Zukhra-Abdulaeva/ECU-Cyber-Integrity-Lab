"""This module defines test-case, execution-context, observation and result
data models for security-test architecture.
The implementation includes:
TestCase: a standardised model for security test cases
ExecutionContext: target, environment and context classification
Observation: standardised observations with timestamps and sources
TestResult: standardised test results with ResultStatus
ExecutionRecord: unique execution ID and execution status
ExecutionStatus: separate status management for the progress of an execution
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, ClassVar, Mapping
from uuid import uuid4

from a_framework.evidence import ContextClassification, ResultStatus


def _utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


def _non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


class ExecutionStatus(str, Enum):
    """Lifecycle status of an execution, distinct from its evaluated result."""

    NOT_STARTED = "NOT_STARTED"
    INITIALIZED = "INITIALIZED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"
    CANCELLED = "CANCELLED"


@dataclass(frozen=True, slots=True)
class TestCase:
    """A normalized, domain-independent security test-case definition."""

    __test__: ClassVar[bool] = False

    test_case_id: str
    name: str
    domain: str
    objective: str
    description: str = ""
    preconditions: tuple[str, ...] = ()
    inputs: Mapping[str, Any] = field(default_factory=dict)
    tags: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for field_name in ("test_case_id", "name", "domain", "objective"):
            object.__setattr__(self, field_name, _non_empty(getattr(self, field_name), field_name))
        object.__setattr__(self, "preconditions", tuple(self.preconditions))
        object.__setattr__(self, "tags", tuple(self.tags))
        object.__setattr__(self, "inputs", dict(self.inputs))
        object.__setattr__(self, "metadata", dict(self.metadata))


@dataclass(frozen=True, slots=True)
class ExecutionContext:
    """Context in which a test is intended to run against a target or model."""

    target_id: str
    classification: ContextClassification
    environment: str = "unspecified"
    target_type: str = "ECU"
    software_version: str | None = None
    hardware_version: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "target_id", _non_empty(self.target_id, "target_id"))
        object.__setattr__(self, "environment", _non_empty(self.environment, "environment"))
        object.__setattr__(self, "target_type", _non_empty(self.target_type, "target_type"))
        if not isinstance(self.classification, ContextClassification):
            try:
                object.__setattr__(self, "classification", ContextClassification(self.classification))
            except (TypeError, ValueError) as exc:
                raise ValueError("classification must be a valid ContextClassification") from exc
        object.__setattr__(self, "metadata", dict(self.metadata))


@dataclass(frozen=True, slots=True)
class Observation:
    """Raw or normalized output observed during execution; not an evaluation."""

    value: Any
    source: str
    observed_at: datetime = field(default_factory=_utc_now)
    media_type: str = "application/json"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "source", _non_empty(self.source, "source"))
        if self.observed_at.tzinfo is None:
            raise ValueError("observed_at must be timezone-aware")
        object.__setattr__(self, "metadata", dict(self.metadata))


@dataclass(frozen=True, slots=True)
class TestResult:
    """Evaluated outcome of a test execution, separate from execution status."""

    __test__: ClassVar[bool] = False

    test_case_id: str
    execution_id: str
    status: ResultStatus
    summary: str
    observations: tuple[Observation, ...] = ()
    started_at: datetime | None = None
    completed_at: datetime | None = None
    evidence_ids: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "test_case_id", _non_empty(self.test_case_id, "test_case_id"))
        object.__setattr__(self, "execution_id", _non_empty(self.execution_id, "execution_id"))
        object.__setattr__(self, "summary", _non_empty(self.summary, "summary"))
        if not isinstance(self.status, ResultStatus):
            try:
                object.__setattr__(self, "status", ResultStatus(self.status))
            except (TypeError, ValueError) as exc:
                raise ValueError("status must be a valid ResultStatus") from exc
        if self.started_at is not None and self.started_at.tzinfo is None:
            raise ValueError("started_at must be timezone-aware")
        if self.completed_at is not None and self.completed_at.tzinfo is None:
            raise ValueError("completed_at must be timezone-aware")
        if self.started_at and self.completed_at and self.completed_at < self.started_at:
            raise ValueError("completed_at cannot precede started_at")
        object.__setattr__(self, "observations", tuple(self.observations))
        object.__setattr__(self, "evidence_ids", tuple(self.evidence_ids))
        object.__setattr__(self, "metadata", dict(self.metadata))

    @property
    def duration_seconds(self) -> float | None:
        """Return execution duration when both timestamps are available."""
        if self.started_at is None or self.completed_at is None:
            return None
        return (self.completed_at - self.started_at).total_seconds()


@dataclass(frozen=True, slots=True)
class ExecutionRecord:
    """Identity and state of one attempt to execute a test case."""

    test_case_id: str
    context: ExecutionContext
    execution_id: str = field(default_factory=lambda: str(uuid4()))
    status: ExecutionStatus = ExecutionStatus.NOT_STARTED
    created_at: datetime = field(default_factory=_utc_now)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "test_case_id", _non_empty(self.test_case_id, "test_case_id"))
        object.__setattr__(self, "execution_id", _non_empty(self.execution_id, "execution_id"))
        if not isinstance(self.status, ExecutionStatus):
            try:
                object.__setattr__(self, "status", ExecutionStatus(self.status))
            except (TypeError, ValueError) as exc:
                raise ValueError("status must be a valid ExecutionStatus") from exc
        for field_name in ("created_at", "started_at", "completed_at"):
            value = getattr(self, field_name)
            if value is not None and value.tzinfo is None:
                raise ValueError(f"{field_name} must be timezone-aware")
        if self.started_at and self.started_at < self.created_at:
            raise ValueError("started_at cannot precede created_at")
        if self.completed_at and self.started_at and self.completed_at < self.started_at:
            raise ValueError("completed_at cannot precede started_at")
        object.__setattr__(self, "metadata", dict(self.metadata))


__all__ = [
    "ExecutionContext",
    "ExecutionRecord",
    "ExecutionStatus",
    "Observation",
    "TestCase",
    "TestResult",
]
