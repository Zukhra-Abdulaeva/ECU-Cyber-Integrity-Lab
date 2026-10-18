from __future__ import annotations

import ipaddress
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import nmap


DEFAULT_PORTS = "22,80,443,13400,30490"
MAX_NETWORK_ADDRESSES = 256


class AutomotiveEthernetScanner:
    """Scan an explicitly supplied IP address/network and collect service data.

    ``target`` must be an IPv4/IPv6 address or CIDR network. To reduce accidental
    broad scans, networks larger than ``max_network_addresses`` are rejected.
    Run only against systems and networks for which you have authorization.
    """

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
        return recommendations

    def summary(self) -> dict[str, int]:
        """Return host and service counts without printing or altering results."""
        return {
            "hosts_discovered": len(self.results),
            "services_detected": sum(len(host["services"]) for host in self.results),
        }

    def export_json(self, filename: str | Path = "ethernet_scan.json") -> Path:
        """Write a UTF-8 JSON inventory report and return its path."""
        output_path = Path(filename)
        report = {
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "assessment": "Automotive Ethernet host and service inventory",
            "scope": "AUTHORIZED_NETWORK_SCAN",
            "scan": self.last_scan,
            "summary": self.summary(),
            "recommendations": self.analyze_services(),
            "results": self.results,
        }
        with output_path.open("w", encoding="utf-8") as report_file:
            json.dump(report, report_file, indent=2, ensure_ascii=False)
            report_file.write("\n")
        return output_path


def main() -> None:
    # Explicit lab target; change only to a network you are authorized to scan.
    scanner = AutomotiveEthernetScanner("192.168.10.0/24")
    if not scanner.validate_target():
        raise SystemExit("Invalid target or target network exceeds configured size limit.")
    scanner.scan()
    print(json.dumps({"summary": scanner.summary(), "recommendations": scanner.analyze_services()}, indent=2))
    scanner.export_json()


if __name__ == "__main__":
    main()
