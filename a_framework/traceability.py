"""Traceability links between security objectives, test cases,
executions, evaluated results, and Phase-4 evidence references.

This module tracks relationships only. It does not execute tests,
evaluate results, or manage evidence lifecycle transitions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping
from uuid import uuid4

from a_framework.test_architecture import TestResult


def _non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


@dataclass(frozen=True, slots=True)
class TraceabilityRecord:
    """References linking one objective to test execution and evidence."""

    objective_id: str
    test_case_id: str
    execution_id: str | None = None
    result: TestResult | None = None
    evidence_ids: tuple[str, ...] = ()
    traceability_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("objective_id", "test_case_id", "traceability_id"):
            object.__setattr__(
                self, name, _non_empty(getattr(self, name), name)
            )

        if self.execution_id is not None:
            object.__setattr__(
                self,
                "execution_id",
                _non_empty(self.execution_id, "execution_id"),
            )

        if self.created_at.tzinfo is None:
            raise ValueError("created_at must be timezone-aware")

        if self.result is not None:
            if not isinstance(self.result, TestResult):
                raise TypeError("result must be a TestResult instance")
            if self.execution_id is None:
                raise ValueError("result requires execution_id")
            if self.result.test_case_id != self.test_case_id:
                raise ValueError(
                    "result test_case_id does not match traceability record"
                )
            if self.result.execution_id != self.execution_id:
                raise ValueError(
                    "result execution_id does not match traceability record"
                )

        evidence_ids = tuple(
            _non_empty(value, "evidence_id")
            for value in self.evidence_ids
        )
        if evidence_ids and self.execution_id is None:
            raise ValueError("evidence references require execution_id")
        if len(evidence_ids) != len(set(evidence_ids)):
            raise ValueError("evidence_ids must not contain duplicates")

        object.__setattr__(self, "evidence_ids", evidence_ids)
        object.__setattr__(self, "metadata", dict(self.metadata))


class TraceabilityRegistry:
    """In-memory index of traceability records; no result/evidence ownership."""

    def __init__(self) -> None:
        self._records: dict[str, TraceabilityRecord] = {}

    def add(self, record: TraceabilityRecord) -> None:
        if not isinstance(record, TraceabilityRecord):
            raise TypeError("record must be a TraceabilityRecord instance")
        if record.traceability_id in self._records:
            raise ValueError(
                f"Duplicate traceability_id: {record.traceability_id}"
            )
        self._records[record.traceability_id] = record

    def get(self, traceability_id: str) -> TraceabilityRecord | None:
        return self._records.get(traceability_id)

    def for_objective(self, objective_id: str) -> tuple[TraceabilityRecord, ...]:
        return tuple(
            record for record in self._records.values()
            if record.objective_id == objective_id
        )

    def for_test_case(self, test_case_id: str) -> tuple[TraceabilityRecord, ...]:
        return tuple(
            record for record in self._records.values()
            if record.test_case_id == test_case_id
        )

    def for_execution(self, execution_id: str) -> tuple[TraceabilityRecord, ...]:
        return tuple(
            record for record in self._records.values()
            if record.execution_id == execution_id
        )

    def for_evidence(self, evidence_id: str) -> tuple[TraceabilityRecord, ...]:
        return tuple(
            record for record in self._records.values()
            if evidence_id in record.evidence_ids
        )


__all__ = [
    "TraceabilityRecord",
    "TraceabilityRegistry",
]
