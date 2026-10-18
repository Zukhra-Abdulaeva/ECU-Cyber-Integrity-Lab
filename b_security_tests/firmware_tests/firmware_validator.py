"""
Firmware Integrity Validator

Description:
SHA-256 metadata, firmware integrity verification, firmware comparison,
and JSON evidence reporting for local firmware artifacts.

Scope:
Static artifact analysis only. A matching SHA-256 digest does not establish
authenticity unless the expected digest comes from a trusted, independently
controlled source.

source .venv/bin/activate
python b_security_tests/firmware_tests/firmware_validator.py
"""

import argparse
import hashlib
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path


_SHA256_PATTERN = re.compile(r"^[0-9a-fA-F]{64}$")


def utc_now():
    """Return the current UTC timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


class FirmwareValidator:
    """Perform reproducible SHA-256 checks on firmware artifacts."""

    TEST_CASE_ID = "FIRMWARE-VALIDATOR-001"

    def __init__(self, evidence_root=None):
        self.results = []
        self.errors = []
        self.evidence_files = {}

        self.started_at = utc_now()
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        self.execution_id = (
            f"EXEC-FW-{timestamp}-{uuid.uuid4().hex[:8].upper()}"
        )

        project_root = Path(__file__).resolve().parents[2]
        self.evidence_root = (
            Path(evidence_root)
            if evidence_root is not None
            else project_root / "c_evidence" / "firmware"
        )

    @staticmethod
    def sha256(filename):
        """Calculate SHA-256 using bounded memory."""
        digest = hashlib.sha256()

        with open(filename, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                digest.update(chunk)

        return digest.hexdigest()

    def firmware_information(self, filename):
        """Return file metadata and its SHA-256 digest."""
        path = Path(filename)
        stat = path.stat()

        return {
            "file": path.name,
            "size_bytes": stat.st_size,
            "modified": datetime.fromtimestamp(
                stat.st_mtime,
                tz=timezone.utc,
            ).isoformat(),
            "sha256": self.sha256(path),
        }

    def verify_integrity(self, filename, expected_hash):
        """Compare a file's digest against an expected SHA-256 digest."""
        if (
            not isinstance(expected_hash, str)
            or not _SHA256_PATTERN.fullmatch(expected_hash)
        ):
            raise ValueError(
                "expected_hash must be a 64-character SHA-256 hex digest"
            )

        current_hash = self.sha256(filename)
        passed = current_hash.casefold() == expected_hash.casefold()

        result = {
            "timestamp": utc_now(),
            "test": "Firmware Integrity",
            "file": os.fspath(filename),
            "status": "PASS" if passed else "FAIL",
            "expected_hash": expected_hash.lower(),
            "calculated_hash": current_hash,
            "comparison": "MATCH" if passed else "MISMATCH",
        }

        self.results.append(result)
        return result

    def compare_firmware(self, firmware_a, firmware_b):
        """
        Compare two firmware artifacts.

        IDENTICAL/DIFFERENT describes hash equality only; it is not by itself
        a security verdict.
        """
        hash_a = self.sha256(firmware_a)
        hash_b = self.sha256(firmware_b)
        identical = hash_a == hash_b

        result = {
            "timestamp": utc_now(),
            "test": "Firmware Comparison",
            "firmware_a": os.fspath(firmware_a),
            "firmware_b": os.fspath(firmware_b),
            "identical": identical,
            "hash_a": hash_a,
            "hash_b": hash_b,
            "comparison": "IDENTICAL" if identical else "DIFFERENT",
        }

        self.results.append(result)
        return result

    def print_information(self, filename):
        """Print file metadata to the console."""
        info = self.firmware_information(filename)

        print("\n========== Firmware ==========")
        print(f"File      : {info['file']}")
        print(f"Size      : {info['size_bytes']} Bytes")
        print(f"Modified  : {info['modified']}")
        print(f"SHA256    : {info['sha256']}")
        print("==============================\n")

    def record_error(self, operation, error):
        """Record an operation error for the evidence report."""
        self.errors.append({
            "timestamp": utc_now(),
            "operation": operation,
            "error_type": type(error).__name__,
            "message": str(error),
        })

    def _evaluation_status(self):
        """Derive a status from recorded integrity checks only."""
        if self.errors:
            return "NOT_EVALUATED"

        integrity_statuses = [
            result["status"]
            for result in self.results
            if result.get("test") == "Firmware Integrity"
            and result.get("status") in {"PASS", "FAIL"}
        ]

        if not integrity_statuses:
            return "NOT_EVALUATED"

        if "FAIL" in integrity_statuses:
            return "FAIL"

        return "PASS"

    def export_json(self, filename=None):
        """
        Export a JSON report.

        Default location:
        c_evidence/firmware/<execution_id>/firmware_report.json
        """
        if filename is None:
            run_dir = self.evidence_root / self.execution_id
            run_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            output_path = run_dir / f"firmware_report_{timestamp}.json"
        else:
            output_path = Path(filename)
            output_path.parent.mkdir(parents=True, exist_ok=True)         

        self.evidence_files["json"] = str(output_path)

        report = {
            "schema_version": "1.0",
            "execution_id": self.execution_id,
            "test_case_id": self.TEST_CASE_ID,
            "started_at": self.started_at,
            "generated": utc_now(),
            "execution_status": "ERROR" if self.errors else "COMPLETED",
            "assessment": "Firmware Integrity Validation",
            "scope": "STATIC_ARTIFACT_ANALYSIS",
            "evaluation_status": self._evaluation_status(),
            "results": self.results,
            "errors": self.errors,
            "evidence_files": dict(self.evidence_files),
            "limitations": [
                "SHA-256 equality alone does not establish authenticity.",
                "Analysis is limited to the local artifacts and recorded checks.",
                (
                    "Firmware comparison reports equality or difference; "
                    "it does not independently determine firmware security."
                ),
            ],
        }

        with output_path.open("w", encoding="utf-8") as file:
            json.dump(report, file, indent=4, ensure_ascii=False)

        print(f"[+] Report exported -> {output_path}")
        return report

def main(argv=None):
    """Run requested checks and export a report."""
    parser = argparse.ArgumentParser(
        description="Validate or compare local firmware artifacts."
    )

    parser.add_argument(
        "--firmware",
        help="Path to the primary firmware artifact",
    )

    parser.add_argument(
        "--expected-sha256",
        help="Expected SHA-256 digest for integrity verification",
    )

    parser.add_argument(
        "--compare-with",
        help="Optional second firmware artifact to compare",
    )

    args = parser.parse_args(argv)

    project_root = Path(__file__).resolve().parents[2]

    default_fw_a = (
        project_root
        / "c_evidence"
        / "firmware"
        / "gateway_ecu.bin"
    )

    default_fw_b = (
        project_root
        / "c_evidence"
        / "firmware"
        / "gateway_ecu_v2.bin"
    )

    validator = FirmwareValidator()

    # Demo mode (no arguments)
    if (
        args.firmware is None
        and args.expected_sha256 is None
        and args.compare_with is None
    ):
        print("[+] No CLI arguments supplied.")
        print("[+] Running default firmware comparison.")

        try:
            validator.print_information(default_fw_a)
        except OSError as error:
            validator.record_error(
                "firmware_information",
                error,
            )

        try:
            validator.compare_firmware(
                default_fw_a,
                default_fw_b,
            )
        except OSError as error:
            validator.record_error(
                "compare_firmware",
                error,
            )

    # Standard CLI mode
    else:
        if not args.expected_sha256 and not args.compare_with:
            parser.error(
                "Provide --expected-sha256, --compare-with, or both."
            )

        if args.expected_sha256:
            try:
                validator.verify_integrity(
                    args.firmware,
                    args.expected_sha256,
                )
            except (OSError, ValueError) as error:
                validator.record_error(
                    "verify_integrity",
                    error,
                )
                print(
                    f"[!] Integrity check error: {error}",
                    file=sys.stderr,
                )

        if args.compare_with:
            try:
                validator.compare_firmware(
                    args.firmware,
                    args.compare_with,
                )
            except OSError as error:
                validator.record_error(
                    "compare_firmware",
                    error,
                )
                print(
                    f"[!] Firmware comparison error: {error}",
                    file=sys.stderr,
                )

    try:
        report = validator.export_json()
    except OSError as error:
        print(
            f"[!] Could not export report: {error}",
            file=sys.stderr,
        )
        return 2

    if report["execution_status"] == "ERROR":
        return 2

    if report["evaluation_status"] == "FAIL":
        return 1

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
