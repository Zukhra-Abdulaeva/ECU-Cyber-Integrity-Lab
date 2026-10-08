"""Evidence records and integrity validation for ECU-Cyber-Integrity-Lab.

This module validates evidence structure and stored-artifact integrity.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
from pathlib import Path
import re
from typing import Any


class ResultStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    NOT_RUN = "NOT_RUN"
    INCONCLUSIVE = "INCONCLUSIVE"
    BLOCKED = "BLOCKED"


class ContextClassification(str, Enum):
    REAL = "REAL"
    VIRTUAL = "VIRTUAL"
    SIMULATED = "SIMULATED"
    LOCAL = "LOCAL"
    STATIC = "STATIC"
    SYNTHETIC = "SYNTHETIC"


class EvidenceLifecycle(str, Enum):
    CREATED = "CREATED"
    VALIDATED = "VALIDATED"
    ASSOCIATED = "ASSOCIATED"
    ACTIVE = "ACTIVE"
    SUPERSEDED = "SUPERSEDED"
    ARCHIVED = "ARCHIVED"


ALLOWED_TRANSITIONS: dict[EvidenceLifecycle, set[EvidenceLifecycle]] = {
    EvidenceLifecycle.CREATED: {EvidenceLifecycle.VALIDATED, EvidenceLifecycle.ARCHIVED},
    EvidenceLifecycle.VALIDATED: {EvidenceLifecycle.ASSOCIATED, EvidenceLifecycle.ACTIVE, EvidenceLifecycle.ARCHIVED},
    EvidenceLifecycle.ASSOCIATED: {EvidenceLifecycle.ACTIVE, EvidenceLifecycle.SUPERSEDED, EvidenceLifecycle.ARCHIVED},
    EvidenceLifecycle.ACTIVE: {EvidenceLifecycle.SUPERSEDED, EvidenceLifecycle.ARCHIVED},
    EvidenceLifecycle.SUPERSEDED: {EvidenceLifecycle.ARCHIVED},
    EvidenceLifecycle.ARCHIVED: set(),
}


@dataclass
class ArtifactReference:
    """Reference plus a snapshot of the artifact's integrity metadata."""
    path: str
    artifact_type: str = "UNKNOWN"
    sha256: str | None = None
    size_bytes: int | None = None
    integrity_checked_at: str | None = None

    @classmethod
    def from_path(cls, path: str | Path, artifact_type: str = "UNKNOWN") -> "ArtifactReference":
        p = Path(path)
        if not p.is_file():
            raise FileNotFoundError(p)
        return cls(path=str(p), artifact_type=artifact_type,
                   sha256=calculate_sha256(p), size_bytes=p.stat().st_size,
                   integrity_checked_at=utc_now())


@dataclass
class EvidenceRecord:
    evidence_id: str
    test_id: str | None = None
    execution_id: str | None = None
    target: str | None = None
    environment: str | None = None
    preconditions: list[str] = field(default_factory=list)
    input: Any = None
    expected_behaviour: str | None = None
    actual_observation: str | None = None
    execution_status: ResultStatus = ResultStatus.NOT_RUN
    result: ResultStatus = ResultStatus.NOT_RUN
    timestamp: str | None = None
    artifacts: list[ArtifactReference] = field(default_factory=list)
    tooling: str | None = None
    execution_method: str | None = None
    context_classification: list[ContextClassification] = field(default_factory=list)
    provenance: dict[str, Any] = field(default_factory=dict)
    evidence_status: EvidenceLifecycle = EvidenceLifecycle.CREATED
    associations: dict[str, list[str]] = field(default_factory=dict)
    integrity: dict[str, Any] = field(default_factory=dict)
    supersedes_evidence_id: str | None = None
    superseded_by_evidence_id: str | None = None
    limitation: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["execution_status"] = self.execution_status.value
        data["result"] = self.result.value
        data["evidence_status"] = self.evidence_status.value
        data["context_classification"] = [item.value for item in self.context_classification]
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EvidenceRecord":
        copied = dict(data)
        copied["execution_status"] = ResultStatus(copied.get("execution_status", ResultStatus.NOT_RUN.value))
        copied["result"] = ResultStatus(copied.get("result", ResultStatus.NOT_RUN.value))
        copied["evidence_status"] = EvidenceLifecycle(copied.get("evidence_status", EvidenceLifecycle.CREATED.value))
        copied["context_classification"] = [ContextClassification(v) for v in copied.get("context_classification", [])]
        copied["preconditions"] = list(copied.get("preconditions", []))
        copied["artifacts"] = [ArtifactReference(**item) for item in copied.get("artifacts", [])]
        copied["associations"] = dict(copied.get("associations", {}))
        copied["provenance"] = dict(copied.get("provenance", {}))
        copied["integrity"] = dict(copied.get("integrity", {}))
        return cls(**copied)

    def transition_to(self, new_status: EvidenceLifecycle) -> None:
        if new_status not in ALLOWED_TRANSITIONS[self.evidence_status]:
            raise ValueError(f"Invalid evidence lifecycle transition: {self.evidence_status.value} -> {new_status.value}")
        self.evidence_status = new_status


REQUIRED_FIELDS = (
    "evidence_id", "test_id", "execution_id", "target", "environment",
    "preconditions", "input", "expected_behaviour", "actual_observation",
    "execution_status", "result", "timestamp", "artifacts", "tooling",
    "execution_method", "context_classification", "provenance", "evidence_status", "associations",
)


class EvidenceValidationError(ValueError):
    """Raised when an evidence record is structurally invalid."""


class EvidenceValidator:
    """Validate record consistency and current artifact integrity, not security truth."""
    _SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

    def validate(self, record: EvidenceRecord) -> list[str]:
        issues: list[str] = []
        if not isinstance(record.evidence_id, str) or not record.evidence_id.strip():
            issues.append("evidence_id is empty")

        if record.result in {ResultStatus.PASS, ResultStatus.FAIL}:
            if not record.execution_id:
                issues.append("PASS/FAIL requires execution_id")
            if not record.actual_observation:
                issues.append("PASS/FAIL requires actual_observation")
            if not record.artifacts:
                issues.append("PASS/FAIL requires at least one artifact")
            if not record.test_id:
                issues.append("PASS/FAIL requires test_id")
            if not record.expected_behaviour:
                issues.append("PASS/FAIL requires expected_behaviour")
            if not record.timestamp:
                issues.append("PASS/FAIL requires timestamp")

        if record.evidence_status in {EvidenceLifecycle.VALIDATED, EvidenceLifecycle.ASSOCIATED, EvidenceLifecycle.ACTIVE}:
            if not record.provenance:
                issues.append("validated/associated/active evidence requires provenance")
            if not record.context_classification:
                issues.append("validated/associated/active evidence requires context classification")
            if not record.test_id:
                issues.append("validated/associated/active evidence requires test_id")

        for key, values in record.associations.items():
            if not isinstance(key, str) or not key.strip():
                issues.append("association type must not be empty")
            if not isinstance(values, list) or any(not isinstance(v, str) or not v.strip() for v in values):
                issues.append(f"association values must be a list of non-empty identifiers: {key}")

        for artifact in record.artifacts:
            if not artifact.path:
                issues.append("artifact path is empty")
                continue
            if not artifact.sha256:
                issues.append(f"artifact integrity hash missing: {artifact.path}")
                continue
            if not self._SHA256_RE.fullmatch(artifact.sha256):
                issues.append(f"artifact SHA-256 has invalid format: {artifact.path}")
                continue
            path = Path(artifact.path)
            if not path.is_file():
                issues.append(f"artifact file missing: {artifact.path}")
                continue
            actual_hash = calculate_sha256(path)
            if actual_hash != artifact.sha256:
                issues.append(f"artifact SHA-256 mismatch: {artifact.path}")
            if artifact.size_bytes is not None and path.stat().st_size != artifact.size_bytes:
                issues.append(f"artifact size mismatch: {artifact.path}")

        return issues

    def assert_valid(self, record: EvidenceRecord) -> None:
        issues = self.validate(record)
        if issues:
            raise EvidenceValidationError("; ".join(issues))


class EvidenceRepository:
    """JSON-backed evidence storage; existing records are never overwritten."""
    def __init__(self, root: str | Path = "c_evidence/records") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, evidence_id: str) -> Path:
        if not evidence_id or evidence_id.strip() != evidence_id or evidence_id in {".", ".."}:
            raise ValueError("Invalid evidence identifier")
        safe_id = evidence_id.replace("/", "_").replace("\\", "_")
        return self.root / f"{safe_id}.json"

    def save(self, record: EvidenceRecord) -> Path:
        EvidenceValidator().assert_valid(record)
        path = self._path(record.evidence_id)
        if path.exists():
            raise FileExistsError(f"Evidence record already exists: {record.evidence_id}. Create a new identifier; do not overwrite history.")
        path.write_text(json.dumps(record.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return path

    def load(self, evidence_id: str) -> EvidenceRecord:
        path = self._path(evidence_id)
        if not path.is_file():
            raise FileNotFoundError(path)
        return EvidenceRecord.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def list_ids(self) -> list[str]:
        return sorted(p.stem for p in self.root.glob("*.json"))


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def calculate_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_artifact_reference(path: str | Path, artifact_type: str = "UNKNOWN") -> ArtifactReference:
    return ArtifactReference.from_path(path, artifact_type=artifact_type)
