"""Inventory of security test-case definitions.

The inventory indexes existing TestCase definitions. It does not execute tests and
does not infer implementation, evidence, result, or verification status from a
definition. Those lifecycle states are explicit fields on InventoryRecord.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Iterator

from a_framework.test_architecture import TestCase


class ImplementationState(str, Enum):
    UNKNOWN = "UNKNOWN"
    PLANNED = "PLANNED"
    IMPLEMENTED = "IMPLEMENTED"


class ExecutionState(str, Enum):
    NOT_EXECUTED = "NOT_EXECUTED"
    EXECUTED = "EXECUTED"
    BLOCKED = "BLOCKED"


class EvidenceState(str, Enum):
    NOT_ASSESSED = "NOT_ASSESSED"
    AVAILABLE = "AVAILABLE"
    MISSING = "MISSING"


class EvaluationState(str, Enum):
    NOT_EVALUATED = "NOT_EVALUATED"
    PASS = "PASS"
    FAIL = "FAIL"
    INCONCLUSIVE = "INCONCLUSIVE"


class VerificationState(str, Enum):
    NOT_VERIFIED = "NOT_VERIFIED"
    VERIFIED = "VERIFIED"


@dataclass(frozen=True, slots=True)
class InventoryRecord:
    """Inventory lifecycle metadata for one existing TestCase definition.

    All lifecycle defaults are deliberately non-claiming. A record's existence
    means only that the case is listed in the inventory.
    """
    test_case: TestCase
    implementation: ImplementationState = ImplementationState.UNKNOWN
    execution: ExecutionState = ExecutionState.NOT_EXECUTED
    evidence: EvidenceState = EvidenceState.NOT_ASSESSED
    evaluation: EvaluationState = EvaluationState.NOT_EVALUATED
    verification: VerificationState = VerificationState.NOT_VERIFIED
    blocker: str | None = None
    notes: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.test_case, TestCase):
            raise TypeError("test_case must be an instance of TestCase")
        for field_name, enum_type in (
            ("implementation", ImplementationState),
            ("execution", ExecutionState),
            ("evidence", EvidenceState),
            ("evaluation", EvaluationState),
            ("verification", VerificationState),
        ):
            value = getattr(self, field_name)
            if not isinstance(value, enum_type):
                try:
                    object.__setattr__(self, field_name, enum_type(value))
                except (TypeError, ValueError) as exc:
                    raise ValueError(f"{field_name} must be a valid {enum_type.__name__}") from exc
        if self.blocker is not None and (not isinstance(self.blocker, str) or not self.blocker.strip()):
            raise ValueError("blocker must be None or a non-empty string")
        if not isinstance(self.notes, str):
            raise TypeError("notes must be a string")
        if self.blocker is not None:
            object.__setattr__(self, "blocker", self.blocker.strip())
        object.__setattr__(self, "notes", self.notes.strip())


class TestInventory:
    """Unique, queryable registry of TestCase definitions."""

    __test__ = False  # Prevent pytest from treating this production class as a test class.

    def __init__(self, records: Iterable[InventoryRecord] = ()) -> None:
        self._records: dict[str, InventoryRecord] = {}
        for record in records:
            self.add(record)

    def add(self, record: InventoryRecord) -> None:
        if not isinstance(record, InventoryRecord):
            raise TypeError("record must be an InventoryRecord")
        test_case_id = record.test_case.test_case_id
        if test_case_id in self._records:
            raise ValueError(f"Duplicate test_case_id in inventory: {test_case_id}")
        self._records[test_case_id] = record

    def get(self, test_case_id: str) -> InventoryRecord:
        try:
            return self._records[test_case_id]
        except KeyError as exc:
            raise KeyError(f"Unknown test_case_id: {test_case_id}") from exc

    def by_domain(self, domain: str) -> tuple[InventoryRecord, ...]:
        normalized = domain.strip().casefold()
        if not normalized:
            raise ValueError("domain must be a non-empty string")
        return tuple(
            record for record in self._records.values()
            if record.test_case.domain.casefold() == normalized
        )

    def incomplete_definitions(self) -> tuple[InventoryRecord, ...]:
        """Return cases failing the A1 completeness check, if the model supports it."""
        incomplete = []
        for record in self._records.values():
            case = record.test_case
            checker = getattr(case, "definition_issues", None)
            if callable(checker) and checker():
                incomplete.append(record)
        return tuple(incomplete)

    def __iter__(self) -> Iterator[InventoryRecord]:
        return iter(self._records.values())

    def __len__(self) -> int:
        return len(self._records)

    def to_dicts(self) -> list[dict[str, object]]:
        """Return JSON-compatible inventory rows without implying execution."""
        rows: list[dict[str, object]] = []
        for record in self._records.values():
            case = record.test_case
            rows.append({
                "test_case_id": case.test_case_id,
                "name": case.name,
                "domain": case.domain,
                "objective": case.objective,
                "assessment_objective": getattr(case, "assessment_objective", ""),
                "security_objective": getattr(case, "security_objective", ""),
                "target_model": getattr(case, "target_model", ""),
                "attack_surface": getattr(case, "attack_surface", ""),
                "attack_hypothesis": getattr(case, "attack_hypothesis", ""),
                "preconditions": list(case.preconditions),
                "inputs": dict(case.inputs),
                "test_steps": list(getattr(case, "test_steps", ())),
                "expected_behaviour": getattr(case, "expected_behaviour", ""),
                "evaluation_criteria": list(getattr(case, "evaluation_criteria", ())),
                "security_oracle": getattr(case, "security_oracle", ""),
                "tags": list(case.tags),
                "definition_issues": list(case.definition_issues()) if callable(getattr(case, "definition_issues", None)) else [],
                "implementation": record.implementation.value,
                "execution": record.execution.value,
                "evidence": record.evidence.value,
                "evaluation": record.evaluation.value,
                "verification": record.verification.value,
                "blocker": record.blocker,
                "notes": record.notes,
            })
        return rows
