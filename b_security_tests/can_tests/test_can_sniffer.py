"""Core CAN sniffer tests using synthetic messages and a controlled fake bus.

These tests validate local capture logic. They do not communicate with a real
vehicle bus or establish ECU-level security validation.
"""

import csv
from datetime import datetime

import pytest
from can import Message

from b_security_tests.can_tests.can_sniffer import CANSniffer


class FakeBus:
    """Minimal deterministic replacement for python-can Bus.recv()."""

    def __init__(self, messages):
        self._messages = iter(messages)
        self.calls = 0

    def recv(self, timeout=1):
        self.calls += 1
        return next(self._messages, None)


class FakeClock:
    """Monotonic test clock that advances by a fixed step per read."""

    def __init__(self, step=0.25):
        self.value = 0.0
        self.step = step

    def __call__(self):
        current = self.value
        self.value += self.step
        return current


def can_message(arbitration_id, data=b"\x01\x02"):
    return Message(
        arbitration_id=arbitration_id,
        data=data,
        is_extended_id=False,
    )


def test_save_message_normalizes_identifier_payload_and_dlc():
    sniffer = CANSniffer()
    message = can_message(0x100, b"\x01\x02\x03\x04")

    sniffer.save_message(message)

    assert len(sniffer.messages) == 1
    saved = sniffer.messages[0]
    assert saved["id"] == "0x100"
    assert saved["dlc"] == 4
    assert saved["data"] == "01 02 03 04"
    datetime.fromisoformat(saved["timestamp"])


def test_receive_messages_captures_only_requested_can_ids(monkeypatch):
    sniffer = CANSniffer()
    sniffer.bus = FakeBus(
        [
            can_message(0x100, b"\x10"),
            can_message(0x200, b"\x20"),
            can_message(0x100, b"\x11"),
        ]
    )
    monkeypatch.setattr(
        "b_security_tests.can_tests.can_sniffer.time.monotonic",
        FakeClock(step=0.25),
    )

    sniffer.receive_messages(duration=1, filter_ids={0x100})

    assert [item["id"] for item in sniffer.messages] == ["0x100", "0x100"]
    assert [item["data"] for item in sniffer.messages] == ["10", "11"]


def test_receive_messages_captures_all_ids_when_filter_is_none(monkeypatch):
    sniffer = CANSniffer()
    sniffer.bus = FakeBus([can_message(0x100), can_message(0x200)])
    monkeypatch.setattr(
        "b_security_tests.can_tests.can_sniffer.time.monotonic",
        FakeClock(step=0.25),
    )

    sniffer.receive_messages(duration=1, filter_ids=None)

    assert [item["id"] for item in sniffer.messages] == ["0x100", "0x200"]


def test_receive_messages_requires_connected_bus():
    with pytest.raises(RuntimeError, match=r"connect\(\) first"):
        CANSniffer().receive_messages(duration=0.1)


def test_receive_messages_rejects_negative_duration():
    sniffer = CANSniffer()
    sniffer.bus = FakeBus([])

    with pytest.raises(ValueError, match="non-negative"):
        sniffer.receive_messages(duration=-1)


def test_export_csv_writes_header_and_captured_rows(tmp_path):
    sniffer = CANSniffer()
    sniffer.save_message(can_message(0x123, b"\xAA\xBB"))
    output = tmp_path / "can_capture.csv"

    sniffer.export_csv(output)

    with output.open(newline="", encoding="utf-8") as csvfile:
        rows = list(csv.DictReader(csvfile))

    assert len(rows) == 1
    assert rows[0]["id"] == "0x123"
    assert rows[0]["dlc"] == "2"
    assert rows[0]["data"] == "aa bb"


def test_statistics_reports_total_and_unique_identifier_counts(capsys):
    sniffer = CANSniffer()
    sniffer.save_message(can_message(0x100))
    sniffer.save_message(can_message(0x100))
    sniffer.save_message(can_message(0x200))

    sniffer.statistics()

    output = capsys.readouterr().out
    assert "Messages: 3" in output
    assert "Unique IDs: 2" in output
