"""Unit tests for framework behavior and evidence-integrity controls.
"""
from pathlib import Path
import sys
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "a_framework"))
from evidence import (
    ContextClassification, EvidenceLifecycle, EvidenceRecord, EvidenceRepository,
    EvidenceValidationError, EvidenceValidator, ResultStatus, build_artifact_reference,
)


def make_pass_record(artifact: Path, evidence_id: str = "EV-TEST-001") -> EvidenceRecord:
    return EvidenceRecord(
        evidence_id=evidence_id, test_id="TEST-EVIDENCE-001", execution_id="EXEC-EVIDENCE-001",
        target="synthetic test target", environment="local unit-test environment",
        preconditions=["test artifact available"], input={"value": "synthetic"},
        expected_behaviour="stored observation remains unchanged",
        actual_observation="stored observation was read back unchanged",
        execution_status=ResultStatus.PASS, result=ResultStatus.PASS,
        timestamp="2026-09-25T00:00:00+00:00",
        artifacts=[build_artifact_reference(artifact, "text")], tooling="pytest",
        execution_method="local unit test",
        context_classification=[ContextClassification.LOCAL, ContextClassification.SYNTHETIC],
        provenance={"origin": "unit-test-generated artifact"},
    )


# Framework behavior tests

def test_framework_accepts_well_formed_synthetic_record(tmp_path: Path):
    artifact = tmp_path / "observation.txt"
    artifact.write_text("observed value\n", encoding="utf-8")
    record = make_pass_record(artifact)
    assert EvidenceValidator().validate(record) == []
    assert record.expected_behaviour != record.actual_observation


def test_lifecycle_allows_valid_path_and_rejects_reverse_transition():
    record = EvidenceRecord(evidence_id="EV-TEST-LIFECYCLE")
    record.transition_to(EvidenceLifecycle.VALIDATED)
    record.transition_to(EvidenceLifecycle.ACTIVE)
    with pytest.raises(ValueError, match="Invalid evidence lifecycle transition"):
        record.transition_to(EvidenceLifecycle.CREATED)


def test_repository_round_trip_and_no_overwrite(tmp_path: Path):
    artifact = tmp_path / "artifact.txt"
    artifact.write_text("evidence\n", encoding="utf-8")
    record = EvidenceRecord(evidence_id="EV-TEST-REPO", artifacts=[build_artifact_reference(artifact, "text")])
    repository = EvidenceRepository(tmp_path / "records")
    path = repository.save(record)
    loaded = repository.load(record.evidence_id)
    assert path.is_file()
    assert loaded.evidence_id == record.evidence_id
    assert loaded.artifacts[0].sha256 == record.artifacts[0].sha256
    with pytest.raises(FileExistsError):
        repository.save(record)


def test_pass_without_execution_metadata_is_rejected():
    issues = EvidenceValidator().validate(EvidenceRecord(evidence_id="EV-TEST-EMPTY", result=ResultStatus.PASS))
    assert "PASS/FAIL requires execution_id" in issues
    assert "PASS/FAIL requires actual_observation" in issues
    assert "PASS/FAIL requires at least one artifact" in issues
    assert "PASS/FAIL requires test_id" in issues


# Evidence integrity tests

def test_artifact_tampering_is_detected(tmp_path: Path):
    artifact = tmp_path / "evidence.txt"
    artifact.write_text("original evidence\n", encoding="utf-8")
    record = make_pass_record(artifact, "EV-TEST-TAMPER")
    artifact.write_text("tampered evidence with changed length\n", encoding="utf-8")
    issues = EvidenceValidator().validate(record)
    assert f"artifact SHA-256 mismatch: {artifact}" in issues
    assert f"artifact size mismatch: {artifact}" in issues


def test_missing_artifact_is_detected(tmp_path: Path):
    artifact = tmp_path / "evidence.txt"
    artifact.write_text("evidence\n", encoding="utf-8")
    record = make_pass_record(artifact, "EV-TEST-MISSING")
    artifact.unlink()
    assert f"artifact file missing: {artifact}" in EvidenceValidator().validate(record)


def test_malformed_hash_is_rejected(tmp_path: Path):
    artifact = tmp_path / "evidence.txt"
    artifact.write_text("evidence\n", encoding="utf-8")
    record = make_pass_record(artifact, "EV-TEST-HASH")
    record.artifacts[0].sha256 = "not-a-sha256"
    assert f"artifact SHA-256 has invalid format: {artifact}" in EvidenceValidator().validate(record)


def test_active_record_requires_traceable_identity_and_provenance():
    record = EvidenceRecord(evidence_id="EV-TEST-ACTIVE", evidence_status=EvidenceLifecycle.ACTIVE)
    issues = EvidenceValidator().validate(record)
    assert "validated/associated/active evidence requires provenance" in issues
    assert "validated/associated/active evidence requires context classification" in issues
    assert "validated/associated/active evidence requires test_id" in issues


def test_invalid_association_values_are_rejected():
    record = EvidenceRecord(evidence_id="EV-TEST-ASSOC", associations={"test": ["TEST-1", ""]})
    assert "association values must be a list of non-empty identifiers: test" in EvidenceValidator().validate(record)


def test_repository_refuses_invalid_record_without_writing(tmp_path: Path):
    repository = EvidenceRepository(tmp_path / "records")
    record = EvidenceRecord(evidence_id="EV-TEST-INVALID", result=ResultStatus.PASS)
    with pytest.raises(EvidenceValidationError):
        repository.save(record)
    assert not (tmp_path / "records" / "EV-TEST-INVALID.json").exists()
