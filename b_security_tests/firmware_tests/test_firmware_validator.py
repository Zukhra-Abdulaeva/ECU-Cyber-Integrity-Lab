import hashlib
import json
from pathlib import Path

import pytest

from b_security_tests.firmware_tests.firmware_validator import FirmwareValidator


def test_sha256_matches_standard_digest(tmp_path):
    artifact = tmp_path / "firmware.bin"
    artifact.write_bytes(b"firmware-test-data")

    assert FirmwareValidator.sha256(artifact) == hashlib.sha256(b"firmware-test-data").hexdigest()


def test_sha256_reads_binary_data(tmp_path):
    artifact = tmp_path / "firmware.bin"
    artifact.write_bytes(bytes(range(256)) * 40)

    assert FirmwareValidator.sha256(artifact) == hashlib.sha256(artifact.read_bytes()).hexdigest()


def test_firmware_information_reports_name_size_and_digest(tmp_path):
    artifact = tmp_path / "ecu_image.bin"
    artifact.write_bytes(b"image")

    info = FirmwareValidator().firmware_information(artifact)

    assert info["file"] == "ecu_image.bin"
    assert info["size_bytes"] == 5
    assert info["sha256"] == hashlib.sha256(b"image").hexdigest()
    assert info["modified"].endswith("+00:00")


def test_integrity_passes_for_matching_digest(tmp_path):
    artifact = tmp_path / "firmware.bin"
    artifact.write_bytes(b"trusted sample")
    digest = hashlib.sha256(b"trusted sample").hexdigest()
    validator = FirmwareValidator()

    result = validator.verify_integrity(artifact, digest.upper())

    assert result["status"] == "PASS"
    assert result["comparison"] == "MATCH"
    assert validator.results == [result]


def test_integrity_fails_for_mismatched_digest(tmp_path):
    artifact = tmp_path / "firmware.bin"
    artifact.write_bytes(b"changed firmware")
    validator = FirmwareValidator()

    result = validator.verify_integrity(artifact, hashlib.sha256(b"original").hexdigest())

    assert result["status"] == "FAIL"
    assert result["comparison"] == "MISMATCH"


@pytest.mark.parametrize("invalid_hash", ["", "abc", "z" * 64, None, 123])
def test_integrity_rejects_invalid_expected_digest(tmp_path, invalid_hash):
    artifact = tmp_path / "firmware.bin"
    artifact.write_bytes(b"image")

    with pytest.raises(ValueError, match="64-character SHA-256"):
        FirmwareValidator().verify_integrity(artifact, invalid_hash)


def test_compare_identical_firmware(tmp_path):
    first = tmp_path / "a.bin"
    second = tmp_path / "b.bin"
    first.write_bytes(b"same")
    second.write_bytes(b"same")

    result = FirmwareValidator().compare_firmware(first, second)

    assert result["identical"] is True
    assert result["hash_a"] == result["hash_b"]


def test_compare_different_firmware(tmp_path):
    first = tmp_path / "a.bin"
    second = tmp_path / "b.bin"
    first.write_bytes(b"version-a")
    second.write_bytes(b"version-b")

    result = FirmwareValidator().compare_firmware(first, second)

    assert result["identical"] is False
    assert result["hash_a"] != result["hash_b"]


def test_missing_file_is_not_silently_accepted(tmp_path):
    with pytest.raises(FileNotFoundError):
        FirmwareValidator().sha256(tmp_path / "missing.bin")


def test_json_export_is_readable_and_contains_scope(tmp_path):
    artifact = tmp_path / "firmware.bin"
    artifact.write_bytes(b"report sample")
    validator = FirmwareValidator()
    validator.verify_integrity(artifact, hashlib.sha256(b"report sample").hexdigest())
    output = tmp_path / "report.json"

    report = validator.export_json(output)
    loaded = json.loads(output.read_text(encoding="utf-8"))

    assert loaded == report
    assert loaded["scope"] == "STATIC_ARTIFACT_ANALYSIS"
    assert loaded["results"][0]["status"] == "PASS"

def test_default_export_uses_timestamped_report_name(tmp_path):
    validator = FirmwareValidator(evidence_root=tmp_path)
    report = validator.export_json()
    execution_dir = tmp_path / validator.execution_id
    files = list(execution_dir.glob("firmware_report_*.json"))

    assert len(files) == 1
    assert files[0].name.startswith("firmware_report_")
    assert files[0].suffix == ".json"

def test_default_export_records_json_evidence_file(tmp_path):
    validator = FirmwareValidator(evidence_root=tmp_path)
    validator.export_json()

    json_path = Path(validator.evidence_files["json"])

    assert json_path.exists()
    assert json_path.name.startswith("firmware_report_")
