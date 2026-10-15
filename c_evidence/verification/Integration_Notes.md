# Integration Notes

## 1. Test Execution Framework

Dieser Abschnitt dokumentiert die Arbeitsschritte zur Prüfung der gemeinsamen Execution-Schnittstelle: Syntax, Imports, erfolgreicher Ausführungspfad, Fehlerpfad und Regression.
Die dokumentierten Befehle, Test-Doubles, Ausgaben und Testergebnisse beschreiben konkreten Integrationsprozess. Sie zeigen, wie das Framework schrittweise aufgebaut, die Schnittstellen verbunden und das Zusammenspiel der Komponenten überprüft wurden sind.

Diese Datei dient als technisches Integrationsprotokoll des Projektaufbaus und deren historischen technischen Integrationsverlauf.

Ausführungsumgebung und Befehle

Python wird über das System aktualisiert, z. B.:
Windows: Installer von python.org (https://www.python.org/downloads/, Installer starten, „Add Python to PATH“ anhaken und „Upgrade Now“ wählen)
Linux: sudo apt install python3.x (sudo apt update, sudo apt install python3 oder sudo apt install python3.x) oder pyenv (curl https://pyenv.run | bash, pyenv install 3.12.3, pyenv global 3.12.3)
macOS: Homebrew (brew update, brew install python, brew upgrade python)

Dokumentierter Ausführungskontext: LOCAL, venv aktivieren und python-can aktualisieren 
```bash
source .venv/bin/activate
pip install --upgrade python-can
```

Python wird über das System aktualisiert, z. B.:

Windows: Installer von python.org
Linux: sudo apt install python3.x oder pyenv
macOS: Homebrew (brew install python)

### 1.1 Python-Syntax prüfen

```bash
python -m py_compile a_framework/execution.py
```

Erwartetes Ergebnis: keine Ausgabe und Exit-Code `0`. Die Datei konnte syntaktisch kompiliert werden.

### 1.2 Imports prüfen

```bash
python -c "from a_framework.execution import ExecutionInterface, AdapterExecutionInterface, ExecutionOutcome; from a_framework.domain_adapter import DomainAdapter; from a_framework.test_architecture import ExecutionStatus, Observation; print('Imports OK')"
```

Erwartete Ausgabe:

```text
Imports OK
```

### 1.3 Ausführung und Observation prüfen

```bash
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
```

Dokumentierte erwartete Ausgabe:

```text
Execution smoke test: PASS
Status: COMPLETED
Observation: {'echo': 'ok'}
```

Damit wird der erfolgreiche Ausführungspfad vom Adapter bis zum gemeinsamen Ergebnisobjekt geprüft.

### 1.4 Fehlerpfad prüfen

```bash
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
```

Dokumentierte erwartete Ausgabe:

```text
Execution error-path test: PASS
Outcome: FAILED
Error: RuntimeError: Simulated observation failure
Adapter status: FAILED
```

### 1.5 Syntaxprüfung der vier Adapter

```bash
python -m py_compile \
    b_security_tests/can_tests/adapter.py \
    b_security_tests/uds_tests/adapter.py \
    b_security_tests/ethernet_tests/adapter.py \
    b_security_tests/firmware_tests/adapter.py
```

Die Syntaxprüfung wird durch die anschließende Adapterintegration ergänzt.

### 1.6 Regressionstest

```bash
python -m pytest -q
```

Dokumentiertes Ergebnis:

```text
14 passed in 0.43s
```

## 2. Integration des TestRunners

### 2.1 Ziel und Ablauf

Der Runner nimmt einen Testfall entgegen, übergibt den bereits ausgewählten Domain-Adapter mit den Eingaben an die Execution-Schnittstelle und liefert ein einheitliches Ergebnis zurück. Er dupliziert weder domänenspezifische Logik noch ersetzt er das Phase-4-Evidence-Framework.

Ablauf:

1. **Testfall / Aufruf:** Adapter und Eingaben sind bereits ausgewählt.
2. **TestRunner:** startet und koordiniert eine einzelne Ausführung.
3. **AdapterExecutionInterface:** führt den Adapter aus und vereinheitlicht das Ergebnis.
4. **Domain-Adapter:** CAN, UDS, Ethernet oder Firmware.
5. **ExecutionOutcome:** Status, Beobachtungen, Laufzeit und Fehlerdetails.

### 2.2 End-to-End-Smoke-Test

Syntaxprüfung:

```bash
python -m py_compile a_framework/runner.py
```

Smoke-Test:

```bash
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
```

Dokumentierte erwartete Ausgabe:

```text
Runner end-to-end smoke test: PASS
Outcome: COMPLETED
Observation: {'echo': 'end-to-end'}
Adapter status: COMPLETED
```

Danach wurde die vorhandene Testsuite erneut ausgeführt:

```bash
python -m pytest -q
```

Dokumentiertes Ergebnis:

```text
14 passed in 1.38s
```

## 3. Integration der CAN-, UDS-, Ethernet- und Firmware-Adapter

### 3.1 Prüfebenen

**A. Adapterintegration:** Die tatsächlichen CAN-, UDS-, Ethernet- und Firmware-Adapter werden instanziiert und durch den Runner ausgeführt. Nur die externen Scanner-, Diagnose- und Firmware-Komponenten werden durch kontrollierte Test-Doubles ersetzt.

**B. Reale Hardwareintegration:** CAN-Bus, ECU, UDS-Verbindung und tatsächliche Firmware-Dateien. Diese Prüfung bleibt separat, bis die benötigte Testumgebung vorhanden ist.

### 3.2 Adapterstand prüfen

```bash
grep -nE 'DomainAdapter|Observation|ExecutionStatus|_status|def execute|def get_observation' \
    b_security_tests/can_tests/adapter.py \
    b_security_tests/uds_tests/adapter.py \
    b_security_tests/ethernet_tests/adapter.py \
    b_security_tests/firmware_tests/adapter.py
```

Damit wird geprüft, ob alle vier Adapter auf die gemeinsame Framework-Schnittstelle verweisen und ob manuelle Statuszuweisungen vorhanden sind.

### 3.3 Integrationsvoraussetzungen prüfen

```bash
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
```

Dokumentiertes Ergebnis:

```text
OK: a_framework/domain_adapter.py
OK: a_framework/execution.py
OK: a_framework/runner.py
OK: a_framework/test_architecture.py
OK: b_security_tests/can_tests/adapter.py
OK: b_security_tests/uds_tests/adapter.py
OK: b_security_tests/ethernet_tests/adapter.py
OK: b_security_tests/firmware_tests/adapter.py
```

### 3.4 Test-Doubles vorbereiten

Für die Integration werden kontrollierte Test-Doubles für die vier domänenspezifischen Abhängigkeiten verwendet:

| Adapter | Simulierte Abhängigkeit |
|---|---|
| CAN | Sniffer mit `receive_messages()` und `messages` |
| UDS | Tester mit `send_request()` |
| Ethernet | Scanner mit `scan()` und `results` |
| Firmware | Validator mit den drei verwendeten Prüfmethoden |

Jeder Adapter wird über `TestRunner.run()` ausgeführt. Geprüft werden:

- Status `COMPLETED`
- genau eine zurückgegebene Observation
- erwarteter Beobachtungsinhalt und korrekte Domänenquelle
- Adapterstatus `COMPLETED`

Es wird keine reale CAN-Kommunikation, UDS-Anfrage oder Netzwerkprüfung ausgelöst.

### 3.5 Alle vier Adapter durch den Runner ausführen

```bash
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
```

Dokumentiertes Ergebnis:

```text
CAN: PASS | outcome=COMPLETED | source=CAN.CANSniffer
UDS: PASS | outcome=COMPLETED | source=UDS.UDSSecurityTester
Ethernet: PASS | outcome=COMPLETED | source=Ethernet.AutomotiveEthernetScanner
Firmware: PASS | outcome=COMPLETED | source=Firmware.FirmwareValidator
All four adapter integration checks: PASS
```

### 3.6 Regression und abschließende Syntaxprüfung

Regressionstest:

```bash
python -m pytest -q
```

Dokumentiertes Ergebnis:

```text
14 passed in 0.47s
```

Syntaxprüfung aller vier Adapter:

```bash
python -m py_compile \
    b_security_tests/can_tests/adapter.py \
    b_security_tests/uds_tests/adapter.py \
    b_security_tests/ethernet_tests/adapter.py \
    b_security_tests/firmware_tests/adapter.py
```

Anschließender Regressionstest:

```bash
python -m pytest -q
```

Dokumentiertes Ergebnis:

```text
14 passed in 0.19s
```

**Abnahmekriterium:** Alle vier Adapter laufen erfolgreich durch `TestRunner` und liefern jeweils eine korrekt zugeordnete Observation.

Die dokumentierte Prüfung deckt die tatsächlichen Adapterklassen mit simulierten externen Abhängigkeiten ab. Sie prüft nicht die Funktion an realer Fahrzeughardware.

## 4. Traceability und Logging

### 4.1 Zuständigkeiten

**Traceability:** Verknüpft bestehende Identifikatoren und Evidence-Referenzen, ohne Testergebnisse selbst zu bewerten.

**Logging:** Einheitliche Logging-Schnittstelle. `logging_boundary.py` kapselt die Logger-Bereitstellung. Es verwaltet weder Teststatus noch Evidence-Lifecycle.

### 4.2 Smoke-Test für beide Schnittstellen

```bash
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
```

Dokumentiertes Ergebnis:

```text
Traceability smoke test: PASS
Logging boundary smoke test: PASS
```

### 4.3 Syntax- und Regressionstest

```bash
python -m py_compile a_framework/base_test.py a_framework/logging_boundary.py
python -m pytest -q
```

Dokumentiertes Ergebnis:

```text
14 passed in 0.79s
```

## 5. Evidence Framework und Evidence Verification

### 5.1 Ausführungsumgebung

Dokumentierter Ausführungskontext: `LOCAL`

```bash
source .venv/bin/activate
pip install --upgrade python-can
python -m pytest -q a_framework/test_evidence.py
python -m pytest -q
```

Die Befehle sind Teil der dokumentierten Integrationsschritte. Für jeden einzelnen Befehl ist in den vorliegenden Notizen kein separates Ergebnis angegeben.

### 5.2 Testausgabe als Artefakt speichern

```bash
mkdir -p c_evidence/verification
python -m pytest -q a_framework/test_evidence.py 2>&1 | tee c_evidence/verification/EV-P4-VER-001_test_execution.txt
sha256sum c_evidence/verification/EV-P4-VER-001_test_execution.txt
```

Damit wird die Terminalausgabe des Evidence-Testlaufs unter `c_evidence/verification/EV-P4-VER-001_test_execution.txt` gespeichert und anschließend deren SHA-256-Prüfsumme berechnet.

### 5.3 Evidence Record und Artefaktinformationen

Create the corresponding Evidence Record, then validate and associate that record with the test execution, observation, and result.

The JSON field types and enum representations match the supplied `a_framework/evidence.py` model.

- **Artifact SHA-256:** `be5c7c2a77651d7dbb2df36d92841b653019bc5a0572bffa08bd3c43016c9b08`
- **Artifact size:** `2598` bytes
- **Tools:** https://openfiletools.com/tools
- **Checksum guide:** https://openfiletools.com/guides/how-to-verify-a-file-checksum

Dokumentierte Einschränkungen:

- Record-Lifecycle bleibt `CREATED`.
- Associations sind als Referenzen repräsentiert, wurden jedoch noch nicht validiert oder durch den Repository-Lifecycle geführt.
- `timestamp` bleibt `null`, weil die bereitgestellte Terminalausgabe keinen Ausführungszeitpunkt enthält.
- Der lokale `EvidenceValidator` wurde durch dieses Paket nicht ausgeführt. Er muss nach dem Kopieren der Dateien in die angegebenen Pfade aus dem Repository-Checkout gestartet werden.
- Vor dem Kopieren ist das tatsächliche Evidence-Root-Verzeichnis des Repositorys zu bestätigen. Der Standardpfad im bereitgestellten Code ist `c_evidence/records`.

Die SHA-256-Prüfsumme und Dateigröße sind die in den ursprünglichen Notizen angegebenen Werte.

## 6. Dokumentierter Integrationsstand

| Bereich | Dokumentierter Arbeitsschritt bzw. Ergebnis |
|---|---|
| Execution Framework | Syntax-, Import-, Erfolgs- und Fehlerpfadprüfungen dokumentiert |
| TestRunner | End-to-End-Smoke-Test dokumentiert |
| CAN, UDS, Ethernet, Firmware | Alle vier Adapter mit Test-Doubles durch den Runner ausgeführt; `PASS` dokumentiert |
| Regression | Mehrere Läufe mit `14 passed` dokumentiert |
| Traceability und Logging | Beide Smoke-Tests mit `PASS` dokumentiert |
| Evidence Verification | Testausgabe- und Hash-Befehle dokumentiert; Evidence-Lifecycle noch nicht abgeschlossen |
| Reale Hardwareintegration | Separater Prüfschritt für CAN-Bus, ECU, UDS-Verbindung und tatsächliche Firmware-Dateien |

## 7. Nächste Integrationsschritte

1. Das tatsächliche Evidence-Root-Verzeichnis im Repository bestätigen.
2. Das Evidence-Testartefakt am vorgesehenen Pfad erzeugen.
3. SHA-256-Prüfsumme und Dateigröße der konkreten Datei prüfen.
4. Den Evidence Record mit dem im Repository vorhandenen `a_framework/evidence.py`-Modell erstellen und den lokalen `EvidenceValidator` ausführen.
5. Associations mit Test Execution, Observation und Result validieren und die vorgesehenen Lifecycle-Übergänge durchführen.
6. Die reale Hardwareintegration separat durchführen, sobald die erforderliche Testumgebung verfügbar ist.

Die Notizen halten damit die dokumentierten Integrationsschritte und ihre Ergebnisse fest. Die Adapterintegration mit Test-Doubles ist von der späteren Hardwareintegration getrennt.
