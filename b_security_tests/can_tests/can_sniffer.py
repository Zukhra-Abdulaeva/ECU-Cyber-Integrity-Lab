"""
==========================================================
CAN Traffic Sniffer analyzer for a configured CAN interface.

Description:
Reads CAN messages via python-can virtual interface, optionally filters specific CAN IDs, 
stores captured traffic and exports the results to CSV.
Captures CAN traffic through python-can, optionally filters arbitration IDs,
and persists a per-execution JSON report plus CSV capture under c_evidence/can.
The capture loop uses a monotonic clock so duration handling is not affected by wall-clock 
adjustments. 

Connect:
A connected bus is required before capture can start.  
source .venv/bin/activate
terminal1: python b_security_tests/can_tests/send_fake_can.py
terminal2: python b_security_tests/can_tests/can_sniffer.py

This module records observations; it does not make a security verdict. Synthetic
traffic on a virtual CAN interface is not evidence of communication with a real ECU.

Requirements:
pip install python-can

sudo apt install can-utils
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0

check: ip link show vcan0 with output: vcan0: <NOARP,UP,LOWER_UP>
==========================================================
"""

import csv
import json
import time
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import can


class CANSniffer:
    """Capture CAN observations and persist a traceable execution report."""

    TEST_CASE_ID = "CAN-SNIFFER-001"

    def __init__(self, channel="vcan0", interface="virtual", evidence_root=None):
        self.channel = channel
        self.interface = interface
        self.bus = None
        self.messages = []

        self.execution_id = (
            f"EXEC-CAN-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}-"
            f"{uuid.uuid4().hex[:8]}"
        )

        self.started_at = None
        self.completed_at = None
        self.configured_duration = None
        self.actual_duration_seconds = None
        self.filter_ids = None
        self.execution_status = "NOT_STARTED"
        self.errors = []
        self.evidence_files = {}

        # Project root: b_security_tests/can_tests/can_sniffer.py
        # -> parents[2] is the repository root.
        self.evidence_root = (
            Path(evidence_root)
            if evidence_root is not None
            else Path(__file__).resolve().parents[2] / "c_evidence" / "can"
        )

    @staticmethod
    def _timestamp():
        """Return a timezone-aware UTC timestamp."""
        return datetime.now(timezone.utc).isoformat()

    def connect(self):
        """Connect to the configured CAN interface."""
        if self.bus is None:
            self.bus = can.interface.Bus(
                channel=self.channel,
                interface=self.interface,
            )

        print(f"[+] Connected to {self.channel} ({self.interface})")

    def receive_messages(self, duration=10, filter_ids=None):
        """Capture CAN traffic for a bounded duration.

        Args:
            duration: Non-negative capture duration in seconds.
            filter_ids: Optional iterable of arbitration IDs to retain.

        Returns:
            A copy of the captured observations.

        Raises:
            ValueError: Invalid duration or CAN identifier filter.
            RuntimeError: No connected CAN bus.
        """
        if (
            not isinstance(duration, (int, float))
            or isinstance(duration, bool)
            or duration < 0
        ):
            raise ValueError("duration must be a non-negative number")

        if self.bus is None:
            raise RuntimeError(
                "CAN bus is not connected; call connect() first"
            )

        normalized_filter = (
            None if filter_ids is None else set(filter_ids)
        )

        if normalized_filter is not None:
            if any(
                not isinstance(can_id, int)
                or isinstance(can_id, bool)
                or not 0 <= can_id <= 0x1FFFFFFF
                for can_id in normalized_filter
            ):
                raise ValueError(
                    "filter_ids must contain valid CAN arbitration IDs"
                )

        self.configured_duration = float(duration)
        self.filter_ids = (
            sorted(normalized_filter)
            if normalized_filter is not None
            else None
        )

        if self.started_at is None:
            self.started_at = self._timestamp()

        start = time.monotonic()
        print(f"[+] Capturing CAN traffic ({duration}s)...")

        while True:
            elapsed = time.monotonic() - start

            if elapsed >= duration:
                break

            remaining = max(0.0, duration - elapsed)

            message = self.bus.recv(timeout=min(1.0, remaining))

            if message is None:
                continue

            if (
                normalized_filter is not None
                and message.arbitration_id not in normalized_filter
            ):
                continue

            self.save_message(message)

            print(
                f"ID: 0x{message.arbitration_id:03X} "
                f"DATA: {bytes(message.data).hex(' ')}"
            )

        self.actual_duration_seconds = round(
            time.monotonic() - start, 6
        )
        self.execution_status = "COMPLETED"

        return list(self.messages)

    def save_message(self, message):
        """Store one CAN message as a normalized observation."""
        self.messages.append(
            {
                "timestamp": self._timestamp(),
                "id": f"0x{message.arbitration_id:X}",
                "arbitration_id": int(message.arbitration_id),
                "is_extended_id": bool(
                    getattr(message, "is_extended_id", False)
                ),
                "dlc": int(
                    getattr(message, "dlc", len(message.data))
                ),
                "data": bytes(message.data).hex(" "),
            }
        )

    def statistics(self):
        """Print and return basic capture statistics."""
        counts = Counter(item["id"] for item in self.messages)

        stats = {
            "message_count": len(self.messages),
            "unique_ids": len(counts),
            "messages_per_id": dict(sorted(counts.items())),
        }

        print("\n========== CAN Statistics ==========")
        print(f"Messages: {stats['message_count']}")
        print(f"Unique IDs: {stats['unique_ids']}")
        print("====================================")

        return stats

    def export_csv(self, filename):
        """Export observations to a CSV file."""
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)

        fieldnames = [
            "timestamp",
            "id",
            "arbitration_id",
            "is_extended_id",
            "dlc",
            "data",
        ]

        with path.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=fieldnames,
            )
            writer.writeheader()
            writer.writerows(self.messages)

        self.evidence_files["csv"] = str(path)
        print(f"[+] CSV exported -> {path}")

        return path

    def build_report(self):
        """Build the report without assigning a security PASS/FAIL verdict."""
        stats = self.statistics()

        return {
            "schema_version": "1.0",
            "execution_id": self.execution_id,
            "test_case_id": self.TEST_CASE_ID,
            "test_name": "CAN Traffic Capture",
            "domain": "CAN",
            "execution_context": {
                "channel": self.channel,
                "interface": self.interface,
                "mode": self.interface.upper()
            },
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "configured_duration_seconds": self.configured_duration,
            "actual_duration_seconds": self.actual_duration_seconds,
            "filter_ids": (
                [f"0x{value:X}" for value in self.filter_ids]
                if self.filter_ids is not None
                else None
            ),
            "execution_status": self.execution_status,
            "observations": self.messages,
            "statistics": stats,
            "errors": self.errors,
            "evidence_files": dict(self.evidence_files),
            "evaluation": {
                "status": "NOT_EVALUATED",
                "rationale": (
                    "Raw CAN observations only; security criteria "
                    "have not been evaluated."
                ),
            },
        }

    def export_report(self, output_dir=None):
        """Persist JSON and CSV in a unique per-execution directory."""
        root = (
            Path(output_dir)
            if output_dir is not None
            else self.evidence_root
        )

        execution_dir = root / self.execution_id
        execution_dir.mkdir(parents=True, exist_ok=True)

        csv_path = execution_dir / "can_capture.csv"
        self.export_csv(csv_path)

        if self.completed_at is None:
            self.completed_at = self._timestamp()

        json_path = execution_dir / "can_report.json"
        self.evidence_files["json"] = str(json_path)

        report = self.build_report()

        with json_path.open("w", encoding="utf-8") as report_file:
            json.dump(
                report,
                report_file,
                indent=2,
                ensure_ascii=False,
            )
            report_file.write("\n")

        print(f"[+] JSON report exported -> {json_path}")

        return json_path

    def close(self):
        """Close the bus if one was opened."""
        if self.bus is not None and hasattr(self.bus, "shutdown"):
            self.bus.shutdown()

        self.bus = None


def main():
    """Run a capture and attempt to persist evidence on completion or error."""
    sniffer = CANSniffer(
        channel="vcan0",
        interface="socketcan"
    )
    sniffer.started_at = sniffer._timestamp()

    try:
        sniffer.connect()
        sniffer.receive_messages(duration=10)

    except KeyboardInterrupt:
        sniffer.execution_status = "INTERRUPTED"
        sniffer.errors.append(
            {
                "type": "KeyboardInterrupt",
                "message": "Capture interrupted by user",
            }
        )
        print("[!] Capture interrupted; saving collected evidence.")

    except Exception as exc:
        sniffer.execution_status = "ERROR"
        sniffer.errors.append(
            {
                "type": type(exc).__name__,
                "message": str(exc),
            }
        )
        print(
            f"[!] CAN capture failed: "
            f"{type(exc).__name__}: {exc}"
        )

    finally:
        if sniffer.execution_status == "NOT_STARTED":
            sniffer.execution_status = "ERROR"

        sniffer.completed_at = sniffer._timestamp()

        try:
            sniffer.export_report()
        except Exception as exc:
            print(
                f"[!] Evidence export failed: "
                f"{type(exc).__name__}: {exc}"
            )
            raise
        finally:
            sniffer.close()

    sniffer.statistics()


if __name__ == "__main__":
    main()
