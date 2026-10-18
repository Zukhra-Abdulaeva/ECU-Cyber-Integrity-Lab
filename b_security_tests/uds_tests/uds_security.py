"""
==========================================================
UDS Security Validation Tool

Description:
Demonstration tool for validating selected UDS services during an White-Box Security Test.
UDS diagnostic security assessment helpers:
This module performs bounded UDS-over-CAN request/response checks. It does not
implement ISO-TP segmentation; requests and responses must fit in one CAN frame.

Requirements:
pip install python-can isotp

Setting up a virtual CAN interface
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
Check:: ip link show vcan0    output:vcan0: <NOARP,UP,LOWER_UP>
source .venv/bin/activate
python b_security_tests/uds_tests/uds_security.py
==========================================================
"""

import json
from datetime import datetime
from pathlib import Path

import can


class UDSSecurityTester:
    """Send selected UDS requests and record their observed responses."""

    def __init__(
        self,
        channel="vcan0",
        interface="socketcan",
        request_id=0x7E0,
        response_id=0x7E8,
        timeout=2.0,
        bus=None,
    ):
        if not isinstance(request_id, int) or not 0 <= request_id <= 0x7FF:
            raise ValueError("request_id must be a standard 11-bit CAN identifier")
        if not isinstance(response_id, int) or not 0 <= response_id <= 0x7FF:
            raise ValueError("response_id must be a standard 11-bit CAN identifier")
        if timeout < 0:
            raise ValueError("timeout must be >= 0")

        self.bus = bus if bus is not None else can.interface.Bus(
            channel=channel,
            interface=interface,
        )
        self.request_id = request_id
        self.response_id = response_id
        self.timeout = timeout
        self.results = []

    @staticmethod
    def _validate_request(data):
        if isinstance(data, (bytes, bytearray)):
            request = list(data)
        elif isinstance(data, (list, tuple)):
            request = list(data)
        else:
            raise TypeError("UDS request must be bytes, bytearray, list, or tuple")
        if not request:
            raise ValueError("UDS request must not be empty")
        if any(not isinstance(value, int) or not 0 <= value <= 0xFF for value in request):
            raise ValueError("UDS request values must be integers in range 0..255")
        if len(request) > 7:
            raise ValueError("single-frame UDS request payload must not exceed 7 bytes")
        return request

    def send_request(self, data):
        """Send one single-frame UDS request and return the matching CAN response.

        Frames from unrelated arbitration IDs are ignored until the configured
        timeout expires. ISO-TP multi-frame transport is intentionally out of scope.
        """
        if self.bus is None:
            raise RuntimeError("CAN bus is not connected")
        request = self._validate_request(data)
        message = can.Message(
            arbitration_id=self.request_id,
            data=request,
            is_extended_id=False,
        )
        self.bus.send(message)

        # Use the CAN library's bounded receive timeout. If unrelated frames are received, continue waiting while the overall deadline is respected.
        import time
        deadline = time.monotonic() + self.timeout
        while True:
            remaining = max(0.0, deadline - time.monotonic())
            response = self.bus.recv(timeout=remaining)
            if response is None:
                return None
            if getattr(response, "arbitration_id", None) == self.response_id:
                return response
            if time.monotonic() >= deadline:
                return None

    @staticmethod
    def evaluate_response(response, request=None):
        """Classify the raw response; classification is not itself a security verdict."""
        if response is None:
            return "No Response"
        payload = getattr(response, "data", None)
        if payload is None or len(payload) == 0:
            return "Malformed Response (empty payload)"

        service = payload[0]
        request_bytes = UDSSecurityTester._validate_request(request) if request is not None else None
        if service == 0x7F:
            if len(payload) < 3:
                return "Malformed Negative Response"
            if request_bytes is not None and payload[1] != request_bytes[0]:
                return f"Unexpected Negative Response (SID 0x{payload[1]:02X})"
            return f"Negative Response (NRC 0x{payload[2]:02X})"

        if request_bytes is not None:
            expected_sid = (request_bytes[0] + 0x40) & 0xFF
            if service != expected_sid:
                return f"Unexpected Response (SID 0x{service:02X})"
        return "Positive Response"

    def log_result(self, test_name, request, response, status, test_case_id=None):
        request_bytes = self._validate_request(request)
        response_data = None
        response_id = None
        if response is not None:
            response_data = bytes(getattr(response, "data", b"")).hex(" ")
            response_id = getattr(response, "arbitration_id", None)

        record = {
            "timestamp": datetime.now().astimezone().isoformat(),
            "test_case_id": test_case_id,
            "test": test_name,
            "request_id": self.request_id,
            "response_id": response_id,
            "request": " ".join(f"{value:02X}" for value in request_bytes),
            "response": response_data,
            "status": status,
        }
        self.results.append(record)
        return record

    def _run_test(self, test_name, request, test_case_id):
        response = self.send_request(request)
        status = self.evaluate_response(response, request=request)
        self.log_result(test_name, request, response, status, test_case_id=test_case_id)
        print(f"[{test_name}] {status}")
        return status

    def diagnostic_session_test(self):
        return self._run_test("Diagnostic Session", [0x10, 0x03], "UDS-SESSION-001")

    def security_access_test(self):
        # Request seed only. No key calculation or unlock attempt is performed.
        return self._run_test("Security Access Seed Request", [0x27, 0x01], "UDS-SECACCESS-001")

    def read_data_identifier_test(self):
        return self._run_test("Read VIN", [0x22, 0xF1, 0x90], "UDS-RDID-001")

    def ecu_reset_test(self):
        # Reset is state-changing; call only against an explicitly authorized target.
        return self._run_test("ECU Reset", [0x11, 0x01], "UDS-RESET-001")

    def export_json(self, filename=None):
        if filename is None:
            project_root = Path(__file__).resolve().parents[2]
            report_dir = project_root / "c_evidence" / "uds"
            report_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = report_dir / f"uds_report_{timestamp}.json"
            print(f"[DEBUG] Writing report to {filename}")
        with open(filename, "w", encoding="utf-8") as report_file:
            json.dump(self.results, report_file, indent=4, ensure_ascii=False)
        print(f"[+] Report exported -> {filename}")

    def print_summary(self):
        print("\n========== UDS TEST SUMMARY ==========")
        for result in self.results:
            print(f"{result['test']:<28}{result['status']}")
        print("======================================\n")

    def close(self):
        if self.bus is not None and hasattr(self.bus, "shutdown"):
            self.bus.shutdown()
        self.bus = None


def main():
    tester = UDSSecurityTester()
    try:
        tester.diagnostic_session_test()
        tester.security_access_test()
        tester.read_data_identifier_test()
        # ECU reset is intentionally not run automatically because it changes target state.
        tester.print_summary()
        tester.export_json()
    finally:
        tester.close()


if __name__ == "__main__":
    main()
