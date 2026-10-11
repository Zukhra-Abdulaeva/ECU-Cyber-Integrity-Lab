# Intergration Notes

Create the corresponding Evidence Record, then validate and associate that record with the test execution, observation, and result.

The JSON field types and enum representations match the supplied `a_framework/evidence.py` model.

Artifact SHA-256: `be5c7c2a77651d7dbb2df36d92841b653019bc5a0572bffa08bd3c43016c9b08`
Artifact size: `2598` bytes
https://openfiletools.com/tools
https://openfiletools.com/guides/how-to-verify-a-file-checksum


Important:
- Record lifecycle remains `CREATED`.
- Associations are represented as references, but they have not yet been validated or transitioned through the repository lifecycle.
- `timestamp` remains null because the supplied terminal output does not contain an execution timestamp.
- The local EvidenceValidator has not been executed by this package. Run it from the repository checkout after copying the files into the paths shown.
- Confirm the repository's actual evidence root before copying; the supplied code's default is `c_evidence/records`.

Test Execution security-test architecture
Test 1 – Python-Syntax prüfen
python -m py_compile a_framework/execution.py
Erwartetes Ergebnis: keine Ausgabe und Exit-Code 0. Das bedeutet, dass die Datei syntaktisch kompiliert werden konnte.

Test 2 – Imports prüfen
python -c "from a_framework.execution import ExecutionInterface, AdapterExecutionInterface, ExecutionOutcome; from a_framework.domain_adapter import DomainAdapter; from a_framework.test_architecture import ExecutionStatus, Observation; print('Imports OK')"
Erwartete Ausgabe: Imports OK

Test 3.1 – Ausführung und Beobachtungsübergabe prüfen

python - <<'PY'
from a_framework.domain_adapter import DomainAdapter
from a_framework.execution import AdapterExecutionInterface
from a_framework.test_architecture import ExecutionStatus, Observation


class DemoAdapter(DomainAdapter):
    domain = "TEST"

    def execute(self, inputs):
        return {"echo": inputs["value"]}

    def get_observation(self, execution_output):
        return Observation(
            value=execution_output,
            source=self.domain,
        )


adapter = DemoAdapter()
interface = AdapterExecutionInterface()

outcome = interface.execute(adapter, {"value": "ok"})

assert outcome.status == ExecutionStatus.COMPLETED
assert len(outcome.observations) == 1
assert outcome.observations[0].value == {"echo": "ok"}
assert outcome.observations[0].source == "TEST"
assert outcome.duration_seconds >= 0

print("Execution smoke test: PASS")
print("Status:", outcome.status.value)
print("Observation:", outcome.observations[0].value)
PY

Erwartete Ausgabe, damit prüfen den erfolgreichen Ausführungspfad vom Adapter bis zum gemeinsamen Ergebnisobjekt:

Execution smoke test: PASS
Status: COMPLETED
Observation: {'echo': 'ok'}

Test 3.1: Fehlerpfad prüfen
python - <<'PY'
from a_framework.domain_adapter import DomainAdapter
from a_framework.execution import AdapterExecutionInterface
from a_framework.test_architecture import ExecutionStatus


class FailingObservationAdapter(DomainAdapter):
    domain = "TEST"

    def execute(self, inputs):
        return {"result": "ok"}

    def get_observation(self, execution_output):
        raise RuntimeError("Simulated observation failure")


adapter = FailingObservationAdapter()
outcome = AdapterExecutionInterface().execute(adapter, {})

assert outcome.status == ExecutionStatus.FAILED
assert outcome.error is not None
assert "Simulated observation failure" in outcome.error

print("Execution error-path test: PASS")
print("Outcome:", outcome.status.value)
print("Error:", outcome.error)
print("Adapter status:", adapter.status.value)
PY

Erwartete Ausgabe:
Execution error-path test: PASS
Outcome: FAILED
Error: RuntimeError: Simulated observation failure
Adapter status: FAILED

Test 4: Syntaxprüfung
Diese Tests prüfen Syntax und vorhandene Testfälle. Für den eigentlichen Schnittstellenabgleich müssen die vier Adapter zusätzlich mit kontrollierten Test-Doubles ausgeführt werden, damit keine reale CAN-Kommunikation, Diagnoseverbindung oder Netzwerksuche gestartet wird.
python -m py_compile \
    b_security_tests/can_tests/adapter.py \
    b_security_tests/uds_tests/adapter.py \
    b_security_tests/ethernet_tests/adapter.py \
    b_security_tests/firmware_tests/adapter.py

Danach die vorhandene Testsuite:
python -m pytest -q
14 passed in 0.43s
Integration der realen CAN-, UDS-, Ethernet- und Firmware-Adapter

Test: Runner
Der Runner soll einen Testfall entgegennehmen, den bereits ausgewählten Domain-Adapter mit den Eingaben an die Execution-Schnittstelle übergeben und ein einheitliches Ergebnis zurückliefern. Er soll weder die domänenspezifische Logik duplizieren noch das Phase-4-Evidence-Framework ersetzen.
Ablauf:
1. Testfall / Aufruf: Adapter und Eingaben sind bereits ausgewählt
2. TestRunner: Startet und koordiniert eine einzelne Ausführung
3. AdapterExecutionInterface: Führt den Adapter aus und vereinheitlicht das Ergebnis
4. Domain-Adapter: CAN, UDS, Ethernet oder Firmware
5. ExecutionOutcome: Status, Beobachtungen, Laufzeit und Fehlerdetails

End-to-End-Smoke-Test

python -m py_compile a_framework/runner.py

python - <<'PY'
from a_framework.domain_adapter import DomainAdapter
from a_framework.runner import TestRunner
from a_framework.test_architecture import ExecutionStatus, Observation


class DemoAdapter(DomainAdapter):
    domain = "TEST"

    def execute(self, inputs):
        return {"echo": inputs["value"]}

    def get_observation(self, execution_output):
        return Observation(
            value=execution_output,
            source=self.domain,
        )


runner = TestRunner()
adapter = DemoAdapter()

outcome = runner.run(adapter, {"value": "end-to-end"})

assert outcome.status == ExecutionStatus.COMPLETED
assert len(outcome.observations) == 1
assert outcome.observations[0].value == {"echo": "end-to-end"}
assert adapter.status == ExecutionStatus.COMPLETED

print("Runner end-to-end smoke test: PASS")
print("Outcome:", outcome.status.value)
print("Observation:", outcome.observations[0].value)
print("Adapter status:", adapter.status.value)
PY

Erwartete Ausgabe:
Runner end-to-end smoke test: PASS
Outcome: COMPLETED
Observation: {'echo': 'end-to-end'}
Adapter status: COMPLETED

Danach die vorhandene Testsuite erneut ausführen:
python -m pytest -q
............. [100%]
14 passed in 1.38s

End-to-End mit realen Domain-Adaptern CAN-, UDS-, Ethernet- und Firmware-Adapter durch den Runner prüfen.
Dabei unterscheiden wir zwei Prüfebenen:
A. Adapterintegration: Die tatsächlichen CAN-, UDS-, Ethernet- und Firmware-Adapter werden instanziiert und durch den Runner ausgeführt. Nur die externen Scanner beziehungsweise Diagnose- und Firmware-Komponenten werden durch kontrollierte Test-Doubles ersetzt.
B. Reale Hardwareintegration: CAN-Bus, ECU, UDS-Verbindung und tatsächliche Firmware-Dateien. Diese Prüfung bleibt separat, bis die benötigte Testumgebung vorhanden ist.

1. Zuerst den Adapterstand prüfen, ob alle vier Adapter bereits auf a_framework verweisen und ob noch manuelle Statuszuweisungen vorhanden sind.
grep -nE 'DomainAdapter|Observation|ExecutionStatus|_status|def execute|def get_observation' \
    b_security_tests/can_tests/adapter.py \
    b_security_tests/uds_tests/adapter.py \
    b_security_tests/ethernet_tests/adapter.py \
    b_security_tests/firmware_tests/adapter.py

2. Integrationsvoraussetzungen prüfen
python - <<'PY'
from pathlib import Path

files = [
    "a_framework/domain_adapter.py",
    "a_framework/execution.py",
    "a_framework/runner.py",
    "a_framework/test_architecture.py",
    "b_security_tests/can_tests/adapter.py",
    "b_security_tests/uds_tests/adapter.py",
    "b_security_tests/ethernet_tests/adapter.py",
    "b_security_tests/firmware_tests/adapter.py",
]

for name in files:
    path = Path(name)
    print(f"{'OK' if path.is_file() else 'MISSING'}: {name}")
PY

Ergebnis:
OK: a_framework/domain_adapter.py
OK: a_framework/execution.py
OK: a_framework/runner.py
OK: a_framework/test_architecture.py
OK: b_security_tests/can_tests/adapter.py
OK: b_security_tests/uds_tests/adapter.py
OK: b_security_tests/ethernet_tests/adapter.py
OK: b_security_tests/firmware_tests/adapter.py

3. End-to-End-Prüfung vorbereiten
Für die eigentliche Integration verwenden wir kontrollierte Test-Doubles für die vier domänenspezifischen Abhängigkeiten:
Adapter / Test-Double
CAN: Simulierter Sniffer mit receive_messages() und messages
UDS: Simulierter Tester mit send_request()
Ethernet: Simulierter Scanner mit scan() und results
Firmware: Simulierter Validator mit den drei vorhandenen Prüfmethoden

Jeder Adapter wird über TestRunner.run() ausgeführt. Geprüft werden:
Status COMPLETED
genau eine zurückgegebene Observation
passender Beobachtungsinhalt und korrekte Domänenquelle
Adapterstatus COMPLETED
Das löst keine reale CAN-Kommunikation, UDS-Anfrage oder Netzwerkprüfung aus.

Dadurch führen alle vier Adapterklassen durch TestRunner aus und ersetzen nur ihre externen Abhängigkeiten durch Test-Doubles. 
Damit prüfen die echte Adapterimplementierung, ohne Fahrzeugbus, ECU oder Netzwerk anzusprechen.

python - <<'PY'
from a_framework.runner import TestRunner
from a_framework.test_architecture import ExecutionStatus

from b_security_tests.can_tests.adapter import CANAdapter
from b_security_tests.uds_tests.adapter import UDSAdapter
from b_security_tests.ethernet_tests.adapter import EthernetAdapter
from b_security_tests.firmware_tests.adapter import FirmwareAdapter


# Controlled test doubles: no real vehicle or network communication.

class FakeSniffer:
    def __init__(self):
        self.messages = []

    def receive_messages(self, duration=10, filter_ids=None):
        self.messages = [
            {"can_id": "0x123", "data": "010203"}
        ]


class FakeUDSTester:
    def send_request(self, request):
        return {"request": request, "response": "simulated-response"}


class FakeEthernetScanner:
    def __init__(self):
        self.results = []

    def scan(self, ports):
        self.results = [{"port": 13400, "state": "simulated-open"}]


class FakeFirmwareValidator:
    def firmware_information(self, filename):
        return {"filename": filename, "status": "simulated"}

    def verify_integrity(self, filename, expected_hash):
        return {
            "filename": filename,
            "integrity": "simulated",
            "expected_hash": expected_hash,
        }

    def compare_firmware(self, firmware_a, firmware_b):
        return {
            "firmware_a": firmware_a,
            "firmware_b": firmware_b,
            "comparison": "simulated",
        }


runner = TestRunner()

cases = [
    (
        "CAN",
        CANAdapter(FakeSniffer()),
        {"duration": 1},
        "CAN.CANSniffer",
    ),
    (
        "UDS",
        UDSAdapter(FakeUDSTester()),
        {"request": "22F190"},
        "UDS.UDSSecurityTester",
    ),
    (
        "Ethernet",
        EthernetAdapter(FakeEthernetScanner()),
        {"ports": "13400"},
        "Ethernet.AutomotiveEthernetScanner",
    ),
    (
        "Firmware",
        FirmwareAdapter(FakeFirmwareValidator()),
        {"operation": "information", "filename": "demo.bin"},
        "Firmware.FirmwareValidator",
    ),
]

for name, adapter, inputs, expected_source in cases:
    outcome = runner.run(adapter, inputs)

    assert outcome.status == ExecutionStatus.COMPLETED, (
        f"{name}: unexpected outcome status {outcome.status}"
    )
    assert len(outcome.observations) == 1, (
        f"{name}: expected exactly one observation"
    )
    assert outcome.observations[0].source == expected_source, (
        f"{name}: unexpected observation source "
        f"{outcome.observations[0].source!r}"
    )
    assert adapter.status == ExecutionStatus.COMPLETED, (
        f"{name}: adapter status is {adapter.status}"
    )

    print(
        f"{name}: PASS | "
        f"outcome={outcome.status.value} | "
        f"source={outcome.observations[0].source}"
    )

print("All four adapter integration checks: PASS")
PY

Ergebnis:CAN: PASS | outcome=COMPLETED | source=CAN.CANSniffer
UDS: PASS | outcome=COMPLETED | source=UDS.UDSSecurityTester
Ethernet: PASS | outcome=COMPLETED | source=Ethernet.AutomotiveEthernetScanner
Firmware: PASS | outcome=COMPLETED | source=Firmware.FirmwareValidator
All four adapter integration checks: PASS

Anschleissend die Regressionstests ausführen
python -m pytest -q
..............[100%]
14 passed in 0.47s
Abnahmekriterium: Alle vier Adapter müssen erfolgreich durch TestRunner laufen und jeweils eine korrekt zugeordnete Observation liefern.
Diese Prüfung belegt die Integration mit den echten Adapterklassen und simulierten Abhängigkeiten – nicht die Funktion an realer Fahrzeughardware.

Zu letzt die Syntaxprüfung aller Adapter:
python -m py_compile \
  b_security_tests/can_tests/adapter.py \
  b_security_tests/uds_tests/adapter.py \
  b_security_tests/ethernet_tests/adapter.py \
  b_security_tests/firmware_tests/adapter.py

python -m pytest -q
..............[100%]
14 passed in 0.19s

Integration: Die Adapter funktionieren mit dem TestRunner und den simulierten Abhängigkeiten.
Syntax: Alle vier Adapterdateien lassen sich separat kompilieren.
Regression: Die vorhandenen Tests prüfen, ob die Änderungen bestehende Funktionalität beeinträchtigt haben.

Traceability: Nachverfolgbarkeit von Testziel bis Evidence. Verknüpft bestehende Identifikatoren und Evidence-Referenzen, ohne Testergebnisse selbst zu bewerten.
Logging: Einheitliche Logging-Schnittstelle. logging_boundary.py kapselt die Logger-Bereitstellung. Es verwaltet weder Teststatus noch Evidence-Lifecycle.

Smoke-Test für die beiden Schnittstellen:
python - <<'PY'
from a_framework.logging_boundary import get_logger
from a_framework.traceability import (
    TraceabilityRecord,
    TraceabilityRegistry,
)

logger = get_logger("ECU-Cyber-Integrity-Lab.smoke")
assert logger.name == "ECU-Cyber-Integrity-Lab.smoke"

record = TraceabilityRecord(
    objective_id="OBJ-001",
    test_case_id="TC-CAN-001",
    execution_id="EXEC-001",
    evidence_ids=("EV-001",),
)

registry = TraceabilityRegistry()
registry.add(record)

assert registry.get(record.traceability_id) == record
assert len(registry.for_objective("OBJ-001")) == 1
assert len(registry.for_test_case("TC-CAN-001")) == 1
assert len(registry.for_execution("EXEC-001")) == 1
assert len(registry.for_evidence("EV-001")) == 1

print("Traceability smoke test: PASS")
print("Logging boundary smoke test: PASS")
PY

Ergebnis: 
Traceability smoke test: PASS
Logging boundary smoke test: PASS

Validierung:
python -m py_compile a_framework/base_test.py a_framework/logging_boundary.py
python -m pytest -q
.............. [100%]
14 passed in 0.79s

Test Execution Framework:
Command: source .venv/bin/activate
Command: pip install --upgrade python-can
Command: python -m pytest -q a_framework/test_evidence.py
Command: python -m pytest -q
Execution context: LOCAL

Test Verification: 
mkdir -p c_evidence/verification
python -m pytest -q a_framework/test_evidence.py \ 2>&1 | tee c_evidence/verification/EV-P4-VER-001_test_execution.txt
sha256sum c_evidence/verification/EV-P4-VER-001_test_execution.txt