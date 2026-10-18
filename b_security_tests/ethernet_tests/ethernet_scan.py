"""
==========================================================
Automotive Ethernet host/service inventory for authorized lab networks.

Description:
    Inventory and security validation tool for Automotive Ethernet environments.
    The scanner wraps ``python-nmap``. Unit tests should inject a fake PortScanner;
    they must never scan a real network. This module inventories observable hosts
    and ports only; it does not prove ECU security or protocol correctness.

Requirements:
    pip install python-nmap

System requirement:
    nmap must be installed on the host.

    sudo apt update
    sudo apt install nmap

source .venv/bin/activate
python b_security_tests/ethernet_tests/ethernet_scan.py
==========================================================
"""

from __future__ import annotations

import ipaddress
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import nmap
import uuid


DEFAULT_PORTS = "22,80,443,13400,30490-30509"
MAX_NETWORK_ADDRESSES = 256


class AutomotiveEthernetScanner:
    """Scan an explicitly supplied IP address/network and collect service data.

    ``target`` must be an IPv4/IPv6 address or CIDR network. To reduce accidental
    broad scans, networks larger than ``max_network_addresses`` are rejected.
    Run only against systems and networks for which you have authorization.
    """
    TEST_CASE_ID = "ETHERNET-SCANNER-001"

    def __init__(
        self,
        target: str,
        *,
        scanner: Any | None = None,
        max_network_addresses: int = MAX_NETWORK_ADDRESSES,
    ) -> None:
        if not isinstance(target, str) or not target.strip():
            raise ValueError("target must be a non-empty IP address or CIDR network")
        if not isinstance(max_network_addresses, int) or max_network_addresses < 1:
            raise ValueError("max_network_addresses must be a positive integer")
        self.target = target.strip()
        self.max_network_addresses = max_network_addresses
        self.scanner = scanner if scanner is not None else nmap.PortScanner()
        self.results: list[dict[str, Any]] = []
        self.last_scan: dict[str, Any] | None = None
        self.errors = []
        self.evidence_files = {}
        self.started_at = datetime.now(timezone.utc).isoformat()
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        self.execution_id = (
            f"EXEC-ETH-{timestamp}-"
            f"{uuid.uuid4().hex[:8].upper()}"
        )
        self.completed_at: str | None = None

        project_root = Path(__file__).resolve().parents[2]

        self.evidence_root = (
            project_root
            / "c_evidence"
            / "ethernet"
        )

        self.completed_at = None

    def validate_target(self) -> bool:
        """Return whether target is a valid, bounded IP address/network."""
        try:
            network = ipaddress.ip_network(self.target, strict=False)
        except ValueError:
            return False
        return network.num_addresses <= self.max_network_addresses

    @staticmethod
    def validate_ports(ports: str) -> str:
        """Validate a comma-separated list of ports/ranges and return it trimmed."""
        if not isinstance(ports, str) or not ports.strip():
            raise ValueError("ports must be a non-empty comma-separated string")
        normalized: list[str] = []
        for raw_item in ports.split(","):
            item = raw_item.strip()
            if not item:
                raise ValueError("ports contains an empty entry")
            pieces = item.split("-")
            if len(pieces) not in (1, 2) or any(not part.isdecimal() for part in pieces):
                raise ValueError(f"invalid port or port range: {item!r}")
            values = [int(part) for part in pieces]
            if any(value < 1 or value > 65535 for value in values):
                raise ValueError(f"port values must be between 1 and 65535: {item!r}")
            if len(values) == 2 and values[0] > values[1]:
                raise ValueError(f"port range start exceeds end: {item!r}")
            normalized.append(item)
        return ",".join(normalized)

    def scan(self, ports: str = DEFAULT_PORTS) -> list[dict[str, Any]]:
        """Run an authorized, bounded TCP connect scan and replace prior results."""
        if not self.validate_target():
            raise ValueError(
                f"invalid target or network exceeds {self.max_network_addresses} addresses: {self.target!r}"
            )
        ports = self.validate_ports(ports)
        # -sT performs a TCP connect scan; -Pn avoids relying on host discovery.
        self.scanner.scan(hosts=self.target, ports=ports, arguments="-Pn -sT")

        host_results: list[dict[str, Any]] = []
        for host in sorted(self.scanner.all_hosts()):
            host_data = self.scanner[host]
            host_result: dict[str, Any] = {
                "host": host,
                "state": str(host_data.state()),
                "services": [],
            }
            for protocol in sorted(host_data.all_protocols()):
                protocol_services = host_data[protocol]
                for port in sorted(protocol_services):
                    service = protocol_services[port]
                    host_result["services"].append(
                        {
                            "port": int(port),
                            "protocol": str(protocol),
                            "state": str(service.get("state", "unknown")),
                            "service": str(service.get("name", "unknown")),
                        }
                    )
            host_results.append(host_result)

        self.results = host_results
        self.last_scan = {
            "target": self.target,
            "ports": ports,
            "scan_type": "TCP_CONNECT",
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "host_count": len(host_results),
            "service_count": sum(len(host["services"]) for host in host_results),
        }
        return list(self.results)

    def analyze_services(self) -> list[dict[str, str]]:
        """Return cautious review hints for selected exposed services."""
        recommendations: list[dict[str, str]] = []
        hints = {
            22: "Review SSH exposure, authentication policy, and unused accounts.",
            80: "Determine whether clear-text HTTP is required; review HTTPS/TLS alternatives.",
            443: "Review TLS versions, cipher policy, and certificate validation.",
        }
        for host in self.results:
            for service in host["services"]:
                port = service["port"]
                if port in hints:
                    recommendations.append(
                        {"host": host["host"], "port": str(port), "recommendation": hints[port]}
                    )
                elif 30490 <= port <= 30509:
                    recommendations.append(
                        {
                            "host": host["host"],
                            "port": str(port),
                            "recommendation": "Potential SOME/IP-related port; verify service identity and configuration.",
                        }
                    )
                elif port == 13400:
                    recommendations.append(
                        {
                            "host": host["host"],
                            "port": str(port),
                            "recommendation":
                                "Diagnostic over IP detected. "
                                "Review diagnostic access control "
                                "and authentication mechanisms.",
                        }
                    )
                elif port == 443:
                    recommendations.append(
                        {
                            "host": host["host"],
                            "port": str(port),
                            "recommendation":
                                "Potential OTA or web service endpoint. "
                                "Review TLS configuration, certificates "
                                "and update trust model.",
                        }
                    )
                elif port in (1883, 8883):
                    recommendations.append(
                        {
                            "host": host["host"],
                            "port": str(port),
                            "recommendation":
                                "MQTT service detected. "
                                "Review authentication, encryption "
                                "and topic exposure.",
                        }
                    )


        return recommendations

    def summary(self) -> dict[str, int]:
        """Return host and service counts without printing or altering results."""
        return {
            "hosts_discovered": len(self.results),
            "services_detected": sum(len(host["services"]) for host in self.results),
        }

    def export_json(
        self,
        filename: str | Path | None = None,
    ) -> Path:

        if filename is None:

            run_dir = (
                self.evidence_root
                / self.execution_id
            )

            run_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            timestamp = datetime.now(
                timezone.utc
            ).strftime(
                "%Y%m%dT%H%M%SZ"
            )

            output_path = (
                run_dir
                / f"ethernet_report_{timestamp}.json"
            )

        else:

            output_path = Path(filename)

            output_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

        self.completed_at = datetime.now(
            timezone.utc
        ).isoformat()

        self.evidence_files["json"] = str(
            output_path
        )

        report = {
            "schema_version": "1.0",
            "execution_id": self.execution_id,
            "test_case_id": self.TEST_CASE_ID,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "generated_utc": self.completed_at,
            "execution_status": self.execution_status(),
            "assessment":
                "Automotive Ethernet Inventory Scan",
            "scope":
                "AUTHORIZED_NETWORK_SCAN",
            "scan": self.last_scan,
            "summary": self.summary(),
            "recommendations":
                self.analyze_services(),
            "results": self.results,
            "errors": self.errors,
            "evidence_files":
                dict(self.evidence_files),
            "evaluation": {
                "status": "NOT_EVALUATED",
                "rationale":
                    "Network inventory identifies "
                    "observable hosts and services. "
                    "Security criteria have not been "
                    "independently validated."
            },
            "limitations": [
                (
                    "Host and port discovery does not "
                    "prove ECU security."
                ),
                (
                    "Open services do not by "
                    "themselves imply vulnerabilities."
                ),
                (
                    "Protocol correctness of DoIP, "
                    "SOME/IP and other Automotive "
                    "Ethernet services is not verified."
                ),
                (
                    "Results support attack-surface "
                    "analysis and asset inventory only."
                ),
            ],
        }

        with output_path.open(
            "w",
            encoding="utf-8",
        ) as report_file:

            json.dump(
                report,
                report_file,
                indent=2,
                ensure_ascii=False,
            )

            report_file.write("\n")

        print(
            f"[+] Report exported -> "
            f"{output_path}"
        )

        return output_path

    def record_error(
        self,
        operation: str,
        error: Exception,
    ) -> None:

        self.errors.append(
            {
                "timestamp": datetime.now(
                    timezone.utc
                ).isoformat(),
                "operation": operation,
                "error_type": type(error).__name__,
                "message": str(error),
            }
        )

    def execution_status(self) -> str:

        if self.errors:
            return "ERROR"

        return "COMPLETED"

def main() -> None:
"""
    Example execution for local development.

    Default target:
        127.0.0.1

    This scans only the local host and normally completes quickly.

    For laboratory assessments, replace the target with an explicitly
    authorized Automotive Ethernet host or network, for example:

        192.168.10.0/24

    Larger network ranges can significantly increase scan duration.
    Run scans only against systems and networks for which authorization
    has been obtained.
    """
    scanner = AutomotiveEthernetScanner("127.0.0.1")
    if not scanner.validate_target():
        raise SystemExit("Invalid target or target network exceeds configured size limit.")
    scanner.scan()
    print(json.dumps({"summary": scanner.summary(), "recommendations": scanner.analyze_services()}, indent=2))
    scanner.export_json()


if __name__ == "__main__":
    main()
