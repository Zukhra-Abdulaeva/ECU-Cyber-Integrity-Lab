import json
from types import SimpleNamespace

import pytest

from b_security_tests.uds_tests.uds_security import UDSSecurityTester


class FakeBus:
    def __init__(self, responses=()):
        self.responses = list(responses)
        self.sent = []
        self.timeouts = []
        self.closed = False

    def send(self, message):
        self.sent.append(message)

    def recv(self, timeout=None):
        self.timeouts.append(timeout)
        return self.responses.pop(0) if self.responses else None

    def shutdown(self):
        self.closed = True


def response(arbitration_id=0x7E8, data=(0x67, 0x01, 0x12, 0x34)):
    return SimpleNamespace(arbitration_id=arbitration_id, data=bytes(data))


def make_tester(bus):
    return UDSSecurityTester(bus=bus, timeout=0.1)


def test_send_request_sends_standard_id_and_returns_matching_response():
    bus = FakeBus([response()])
    tester = make_tester(bus)

    result = tester.send_request([0x27, 0x01])

    assert result.data == bytes([0x67, 0x01, 0x12, 0x34])
    assert bus.sent[0].arbitration_id == 0x7E0
    assert list(bus.sent[0].data) == [0x27, 0x01]
    assert bus.sent[0].is_extended_id is False


def test_send_request_ignores_unrelated_can_identifier():
    bus = FakeBus([response(arbitration_id=0x123), response()])
    tester = make_tester(bus)

    result = tester.send_request([0x27, 0x01])

    assert result.arbitration_id == 0x7E8
    assert len(bus.timeouts) == 2


@pytest.mark.parametrize("payload", [[], [0x27, 256], [0x27, -1], [0x27] * 8])
def test_send_request_rejects_invalid_payload(payload):
    tester = make_tester(FakeBus())
    with pytest.raises(ValueError):
        tester.send_request(payload)


def test_send_request_rejects_wrong_input_type():
    tester = make_tester(FakeBus())
    with pytest.raises(TypeError):
        tester.send_request("2701")


def test_send_request_requires_bus():
    tester = make_tester(FakeBus())
    tester.bus = None
    with pytest.raises(RuntimeError, match="not connected"):
        tester.send_request([0x27, 0x01])


def test_evaluate_positive_response_checks_expected_service():
    assert UDSSecurityTester.evaluate_response(response(), [0x27, 0x01]) == "Positive Response"
    assert UDSSecurityTester.evaluate_response(response(data=(0x62, 0xF1, 0x90)), [0x27, 0x01]) == "Unexpected Response (SID 0x62)"


def test_evaluate_negative_response_extracts_nrc():
    negative = response(data=(0x7F, 0x27, 0x35))
    assert UDSSecurityTester.evaluate_response(negative, [0x27, 0x01]) == "Negative Response (NRC 0x35)"


def test_evaluate_response_handles_no_and_malformed_responses():
    assert UDSSecurityTester.evaluate_response(None, [0x27, 0x01]) == "No Response"
    assert UDSSecurityTester.evaluate_response(response(data=()), [0x27, 0x01]) == "Malformed Response (empty payload)"
    assert UDSSecurityTester.evaluate_response(response(data=(0x7F, 0x27)), [0x27, 0x01]) == "Malformed Negative Response"


def test_log_result_records_traceability_and_exports_json(tmp_path):
    bus = FakeBus([response()])
    tester = make_tester(bus)
    tester.security_access_test()
    target = tmp_path / "uds_report.json"

    tester.export_json(str(target))
    data = json.loads(target.read_text(encoding="utf-8"))

    assert data[0]["test_case_id"] == "UDS-SECACCESS-001"
    assert data[0]["request"] == "27 01"
    assert data[0]["response"] == "67 01 12 34"
    assert data[0]["status"] == "Positive Response"
    assert data[0]["request_id"] == 0x7E0
    assert data[0]["response_id"] == 0x7E8


def test_close_shuts_down_bus():
    bus = FakeBus()
    tester = make_tester(bus)
    tester.close()
    assert bus.closed is True
    assert tester.bus is None
