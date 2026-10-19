# Integration Notes

## Zweck und Dokumentationsregeln

Diese Datei ist das technische Integrationsprotokoll des ECU-Cyber-Integrity-Lab. Sie hält konkrete Arbeitsschritte, Befehle, Test-Doubles, Terminalausgaben und dokumentierte Testergebnisse fest. So bleibt nachvollziehbar, wie gemeinsame Framework-Schnittstellen und domänenspezifische Security-Komponenten schrittweise aufgebaut und geprüft wurden.

Die Notizen unterscheiden zwischen dokumentiert ausgeführten Schritten, Smoke-Tests, synthetischen Tests bzw. Tests mit Test-Doubles und noch nicht nachgewiesenen Integrationsstufen. Historische Testzahlen gehören zu den jeweiligen Entwicklungsständen.

## Ausführungsumgebung

Dokumentierter Ausführungskontext: `LOCAL`, mit aktivierter virtueller Umgebung `.venv`.

```bash
source .venv/bin/activate
pip install --upgrade python-can
```

Python kann bei Bedarf plattformgerecht aktualisiert werden: Windows über den Installer von https://www.python.org/downloads/ (dabei „Add Python to PATH“ aktivieren), Linux über den Paketmanager oder `pyenv`, macOS über Homebrew. Eine System-Python-Aktualisierung ist von den Repository-Tests zu unterscheiden. Für reproduzierbare Läufe sollten Python-Version und Abhängigkeiten der `.venv` protokolliert werden.

---

## 1. Test Execution Framework

Dieser Abschnitt dokumentiert Syntax, Imports, erfolgreichen Ausführungspfad, Fehlerpfad und Regression der gemeinsamen Execution-Schnittstelle.

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

### 1.3 Erfolgreichen Ausführungspfad und Observation prüfen

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

Dokumentierter Ablauf:

1. Testfall bzw. Aufruf: Adapter und Eingaben sind bereits ausgewählt.
2. `TestRunner`: koordiniert die Ausführung.
3. `AdapterExecutionInterface`: führt den Adapter aus und vereinheitlicht das Ergebnis.
4. Domain-Adapter: stellt die domänenspezifische Ausführung bereit.
5. `ExecutionOutcome`: enthält Status, Beobachtungen, Laufzeit und gegebenenfalls Fehlerdetails.

### 2.2 End-to-End-Smoke-Test

Der dokumentierte Smoke-Test verwendete einen synthetischen `DemoAdapter` mit `domain = "TEST"`, der die Eingabe als Observation zurückgibt. Die Assertions prüften `COMPLETED`, genau eine Observation, den Wert `{"echo": "end-to-end"}` und den Adapterstatus `COMPLETED`.

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

Der Evidenzdatensatz wurde erstellt und validiert und mit der Testausführung und deren erfolgreichem Testergebnis verknüpft.

Die JSON-Feldtypen und die Darstellung der Aufzählungslisten entsprechen dem bereitgestellten Modell `a_framework/evidence.py`.

- Artefakt: `c_evidence/verification/EV-P4-VER-001_test_execution.txt`
- SHA-256: `be5c7c2a77651d7dbbdf36d92841b653019bc5a0572bffa08bd3c43016c9b08`
- Dateigröße: `2598` Bytes
- Kontext: `LOCAL`; historische Phase-4-Verifikation, nicht das aggregierte Ergebnis der späteren Phase-5-Arbeit
- Tools: https://openfiletools.com/tools
- Checksum guide: https://openfiletools.com/guides/how-to-verify-a-file-checksum

Dokumentierte Einschränkungen:

- Record-Lifecycle blieb `CREATED`.
- Associations waren als Referenzen repräsentiert, aber in diesem dokumentierten Schritt noch nicht durch den Repository-Lifecycle validiert.
- `timestamp` blieb `null`, weil die bereitgestellte Terminalausgabe keinen Ausführungszeitpunkt enthielt.
- Der lokale `EvidenceValidator` war in diesem Schritt noch nicht ausgeführt worden.
- Das tatsächliche Evidence-Root-Verzeichnis wurde bestätigt; `c_evidence/records` war im bereitgestellten Code als Standardpfad vorgesehen.

## 5.4. Dokumentierter Integrationsstand

| Bereich | Dokumentierter Arbeitsschritt bzw. Ergebnis |
|---|---|
| Execution Framework | Syntax-, Import-, Erfolgs- und Fehlerpfadprüfungen dokumentiert |
| TestRunner | End-to-End-Smoke-Test dokumentiert |
| CAN, UDS, Ethernet, Firmware | Alle vier Adapter mit Test-Doubles durch den Runner ausgeführt; `PASS` dokumentiert |
| Regression | Mehrere Läufe mit `14 passed` dokumentiert |
| Traceability und Logging | Beide Smoke-Tests mit `PASS` dokumentiert |
| Evidence Verification | Testausgabe- und Hash-Befehle dokumentiert; Evidence-Lifecycle noch nicht abgeschlossen |
| Reale Hardwareintegration | Separater Prüfschritt für CAN-Bus, ECU, UDS-Verbindung und tatsächliche Firmware-Dateien |

## 5.5. Nächste Integrationsschritte

1. Das tatsächliche Evidence-Root-Verzeichnis im Repository bestätigen.
2. Das Evidence-Testartefakt am vorgesehenen Pfad erzeugen.
3. SHA-256-Prüfsumme und Dateigröße der konkreten Datei prüfen.
4. Den Evidence Record mit dem im Repository vorhandenen `a_framework/evidence.py`-Modell erstellen und den lokalen `EvidenceValidator` ausführen.
5. Associations mit Test Execution, Observation und Result validieren und die vorgesehenen Lifecycle-Übergänge durchführen.
6. Die reale Hardwareintegration separat durchführen, sobald die erforderliche Testumgebung verfügbar ist.

Die Notizen halten damit die dokumentierten Integrationsschritte und ihre Ergebnisse fest. Die Adapterintegration mit Test-Doubles ist von der späteren Hardwareintegration getrennt.

## 6. Phase 5 – Security-Layer und domänenspezifische Validierung

### 6.1 Umfang

Phase 5 erweiterte die vorhandenen Security-Komponenten und prüfte sie mit konkreten Unit-Tests und kontrollierten lokalen Ausführungsläufen. Die dokumentierten Domänen sind CAN, UDS, Firmware und Ethernet/IP.

**CAN:** CAN Traffic Capture, CAN Message Analysis/Verkehrsstatistik, CSV-Mitschnitt und JSON-Bericht als Rohdaten- bzw. Ausführungsevidenz.

**UDS:** Diagnostic Session Control, Security Access Seed Request, ReadDataByIdentifier (einschließlich eines Read-VIN-Aufrufs im dokumentierten CLI-Lauf) und Klassifizierung positiver, negativer, fehlerhafter sowie unerwarteter Antworten.

**Firmware:** SHA-256 Integrity Validation, Firmware Comparison, Datei-Metadaten, JSON-Evidence-Reporting und Traceability-Metadaten.

**Ethernet/IP:** begrenzte Ziel- und Portvalidierung, TCP-Connect-Portinventar, strukturierte Scan-Ergebnisse und Metadaten sowie Servicehinweise als Daten.

Diese Aufzählung beschreibt den dokumentierten Funktionsbereich. Sie bedeutet nicht, dass sämtliche Automotive-Protokollschichten implementiert oder reale ECUs vollständig validiert wurden.

### 6.2 Bestehende TestCase-Aufrufer prüfen

```bash
grep -RIn --include="*.py" \
  -E 'TestCase\(|definition_issues|assert_definition_complete' \
  a_framework b_security_tests
```

Dokumentierter Fundstellen-Auszug:

```text
a_framework/test_architecture.py:63:    # with existing callers while definition_issues() identifies incomplete cases.
a_framework/test_architecture.py:120:    def definition_issues(self) -> tuple[str, ...]:
a_framework/test_architecture.py:137:    def assert_definition_complete(self) -> None:
a_framework/test_architecture.py:139:        issues = self.definition_issues()
b_security_tests/testcase_definition.py:8:    case = TestCase(
b_security_tests/testcase_definition.py:15:    assert case.definition_issues()
b_security_tests/testcase_definition.py:19:    case = TestCase(
b_security_tests/testcase_definition.py:41:    assert case.definition_issues() == ()
b_security_tests/testcase_definition.py:42:    case.assert_definition_complete()
b_security_tests/testcase_definition.py:45:def test_assert_definition_complete_lists_missing_fields():
b_security_tests/testcase_definition.py:46:    case = TestCase(
b_security_tests/testcase_definition.py:53:        case.assert_definition_complete()
b_security_tests/testcase_definition.py:58:        TestCase(
b_security_tests/testcase_definition.py:69:        TestCase(
```

Die Kompatibilitätsanforderung lautet: Bestehende Domain-Adapter und der Runner sollen nicht gezwungen werden, zusätzliche A1-Felder zu setzen, solange diese nicht Teil ihrer bisherigen Schnittstelle sind.

### 6.3 Inventory of security test-case definitions

`inventory.py` enthält die Inventory-Implementierung. `test_inventory.py` enthält sieben zugehörige pytest-Tests. Das bestehende `TestCase`-Modell aus `a_framework.test_architecture` bleibt die Grundlage.

```bash
python -m pytest -q b_security_tests/test_inventory.py
```

Dokumentierte Ausgabe:

```text
....... [100%]
7 passed in 0.07s
```

Anschließender Regressionstest:

```bash
python -m pytest -q
```

Dokumentierte Ausgabe:

```text
..................... [100%]
21 passed in 0.38s
```

---

## 7. CAN Core Test Implementation / Validation

### 7.1 Implementierungsänderungen

Die CAN-Unit-Tests verwenden synthetische CAN-Nachrichten und kontrollierte Fake-Busse. Sie führen keine reale Kommunikation mit einem Fahrzeug oder einer ECU aus.

Dokumentierte Änderungen an `b_security_tests/can_tests/can_sniffer.py`:

- Zeitmessung für die Aufnahmedauer auf `time.monotonic()` umgestellt.
- Negative Aufnahmedauer wird abgelehnt.
- Eine fehlende CAN-Verbindung führt zu einer verständlichen Fehlermeldung.
- CSV-Export verwendet explizit UTF-8.
- Die Capture-Schleife wertet `time.monotonic()` pro Schleifendurchlauf nur einmal aus, damit FakeClock-Tests stabil bleiben und die Erfassung nicht vorzeitig endet.

`b_security_tests/can_tests/test_can_sniffer.py` prüft Nachrichtenformat und CAN-ID, Filterung nach CAN-IDs, Aufnahme ohne Filter, fehlende Verbindung, ungültige Aufnahmedauer, CSV-Export und Verkehrszusammenfassung.

### 7.2 CAN-Report

Die Notizen beschreiben den CAN-Report als JSON-Rohdaten-Evidenz mit ergänzendem CSV-Mitschnitt. Das vorgesehene Reportmodell enthält:

| Feld | Bedeutung |
|---|---|
| `execution_id` | Eindeutige Kennung des konkreten Durchlaufs |
| `test_case_id` | Referenz auf die Testdefinition |
| `started_at`, `completed_at` | Beginn und Ende der Aufzeichnung |
| `channel`, `interface` | Beispielsweise `vcan0` und `socketcan` |
| `duration_seconds` | Konfigurierte und gemessene Laufzeit, sofern beide Werte erfasst werden |
| `filter_ids` | Verwendete CAN-ID-Filter oder `null` |
| `execution_status` | Beispielsweise `COMPLETED`, `ERROR` oder `INTERRUPTED` |
| `message_count`, `unique_ids` | Nachrichtenanzahl und Anzahl unterschiedlicher CAN-IDs |
| `observations` | CAN-Nachrichten mit Zeitstempeln und Payload |
| `evidence_files` | Referenzen auf JSON- und CSV-Dateien |
| `errors` | Aufgetretene technische Fehler |

Die Tabelle beschreibt das in den Notizen vorgesehene Reportmodell. Die tatsächliche Feldvollständigkeit ist am konkreten JSON-Artefakt zu prüfen.

Die dokumentierte Fehleranforderung lautet, möglichst auch bei gescheiterter Ausführung einen Report zu erzeugen: bei normalem Abschluss Beobachtungen und Status speichern; bei null Nachrichten `message_count = 0` dokumentieren; bei Verbindungsfehlern Fehler und Kontext festhalten, ohne Beobachtungen zu erfinden; bei Abbruch vorhandene Daten soweit möglich als unvollständige Evidenz sichern; Exportfehler sichtbar machen. Diese Anforderungen sind anhand der konkreten Implementierung und Tests zu verifizieren.

### 7.3 Vereinheitlichung auf SocketCAN (`vcan0`)

Während der Entwicklung wurden `interface="virtual"` (python-can VirtualBus) und `interface="socketcan"` mit Linux `vcan0` verwendet. Für lokale Linux-CAN-Simulationen wurde die gemeinsame Konfiguration festgelegt:

```python
bus = can.interface.Bus(
    channel="vcan0",
    interface="socketcan",
)
```

So können mehrere Werkzeuge dasselbe virtuelle Linux-CAN-Interface beobachten. Der python-can VirtualBus ist ein anderes Backend und nicht automatisch über `candump vcan0` sichtbar.

```bash
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
ip link show vcan0
```

Dokumentiert erwarteter Status:

```text
vcan0: <NOARP,UP,LOWER_UP>
```

Zur Fehlersuche:

```bash
candump vcan0
```

Für lokale Komponenten, die mit SocketCAN-Werkzeugen zusammenarbeiten müssen, gilt `channel="vcan0"` und `interface="socketcan"`. Das ist kein Nachweis einer Verbindung zu einem realen Fahrzeugbus.

### 7.4 Dokumentierter Sender-/Sniffer-Lauf

Terminal 1:

```bash
python b_security_tests/can_tests/send_fake_can.py
```

Dokumentierte Ausgabeauszüge:

```text
[+] Sending synthetic CAN messages on vcan0 for 15 seconds...
Sent ID: 0x100
Sent ID: 0x321
Sent ID: 0x200
```

Terminal 2:

```bash
python b_security_tests/can_tests/can_sniffer.py
```

Dokumentierte Ausgabeauszüge:

```text
[+] Connected to vcan0 (socketcan)
[+] Capturing CAN traffic (10s)...
ID: 0x200 DATA: ff ff ff ff ff ff ff ff
ID: 0x100 DATA: 01 00 ff a2 12 44 55 66
ID: 0x321 DATA: 11 22 33 44 55 66 77 88
```

Der protokollierte Lauf meldete:

```text
[+] CSV exported -> /home/zukhra/GitHub_Automotive-Security/ECU-Cyber-Integrity-Lab/c_evidence/can/EXEC-CAN-20261018T044421-49eab15f/can_capture.csv

========== CAN Statistics ==========
Messages: 20
Unique IDs: 3
====================================

[+] JSON report exported -> /home/zukhra/GitHub_Automotive-Security/ECU-Cyber-Integrity-Lab/c_evidence/can/EXEC-CAN-20261018T044421-49eab15f/can_report.json

========== CAN Statistics ==========
Messages: 20
Unique IDs: 3
====================================
```

Damit ist ein konkreter lokaler Lauf auf `vcan0` mit synthetisch gesendeten Nachrichten und JSON-/CSV-Ausgabe dokumentiert. Er ist keine Messung an einem realen Fahrzeug oder einer realen ECU.

### 7.5 CAN-Tests und Regression

```bash
python -m pytest -q b_security_tests/can_tests/test_can_sniffer.py
```

Dokumentiertes Ergebnis: `7 passed in 0.17s`.

```bash
python -m pytest -q
```

Dokumentiertes Ergebnis: `27 passed in 0.47s`.

---

## 8. UDS Security Test Implementation / Validation

### 8.1 Dokumentierte Änderungen

Ziel ist die nachvollziehbare Prüfung von Anfrage- und Antwortverhalten rund um Security Access (UDS Service `0x27`). Negative Response Codes (NRCs), unerwartete Antworten und fehlende Antworten werden erfasst, ohne sie pauschal als Sicherheitslücke zu bewerten.

Dokumentierte Änderungen an `b_security_tests/uds_tests/uds_security.py`:

- Validierung von UDS-Anfragen und Nutzdaten
- Zuordnung von Antworten anhand der CAN-Response-ID
- Erkennung positiver, negativer, fehlerhafter und unerwarteter Antworten
- Protokollierung mit Testfall-ID sowie Request-/Response-IDs
- UTF-8-JSON-Export
- kontrolliertes Schließen des CAN-Busses
- automatischer ECU-Reset aus `main()` entfernt, weil ein Reset den Zielzustand verändert

`b_security_tests/uds_tests/test_uds_security.py` ersetzte den Platzhalter durch konkrete Unit-Tests bzw. parametrische Testausführungen für ungültige Requests, NRC-Auswertung, unerwartete Antworten, JSON-Reporting und Bus-Lifecycle.

### 8.2 Lokaler Aufbau und CLI-Lauf

Die ursprünglichen Notizen nennen folgende Befehle:

```bash
pip install python-can isotp
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
ip link show vcan0
source .venv/bin/activate
python b_security_tests/uds_tests/uds_security.py
```

Dokumentierte Interface-Ausgabe:

```text
3: vcan0: <NOARP,UP,LOWER_UP> mtu 2060 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/can
```

Der dokumentierte CLI-Lauf gab keine Antworten zurück:

```text
[Diagnostic Session] No Response
[Security Access Seed Request] No Response
[Read VIN] No Response

========== UDS TEST SUMMARY ==========
Diagnostic Session           No Response
Security Access Seed Request No Response
Read VIN                     No Response
======================================
[DEBUG] Writing report to /home/zukhra/GitHub_Automotive-Security/ECU-Cyber-Integrity-Lab/c_evidence/uds/uds_report_20261018_045023.json
[+] Report exported -> /home/zukhra/GitHub_Automotive-Security/ECU-Cyber-Integrity-Lab/c_evidence/uds/uds_report_20261018_045023.json
```

Ein laufendes `vcan0` stellt allein noch keine ECU oder UDS-Gegenstelle bereit. `No Response` ist daher nicht als Nachweis einer ECU-Sicherheitslücke zu interpretieren.

### 8.3 Gezielte Tests und Grenzen

```bash
python -m pytest -q b_security_tests/uds_tests/test_uds_security.py
```

Dokumentiertes Ergebnis: `13 passed in 0.34s`.

```bash
python -m pytest -q
```

Dokumentiertes Ergebnis: `39 passed in 0.48s`.

Die dokumentierte Implementierung verarbeitet nur einzelne UDS-Nutzdatenframes auf CAN. Sie implementiert keine ISO-TP-Segmentierung und weist weder ECU-Verhalten noch Zugriffskontrolle oder Fahrzeugsicherheit nach. Security Access fordert einen Seed mit `0x27 0x01` an; es wird kein Schlüssel berechnet oder gesendet und keine Security-Level-Sperre aufgehoben. Tests mit Test-Doubles ersetzen keine Kommunikation mit einem autorisierten, kontrollierten ECU-Ziel.

---

## 9. Firmware Integrity Test Implementation

### 9.1 Testartefakte vorbereiten

Die ursprünglichen Notizen verwenden:

```text
c_evidence/firmware/
├── gateway_ecu.bin
└── gateway_ecu_v2.bin
```

Dateien prüfen:

```bash
ls -lh c_evidence/firmware/*.bin
file c_evidence/firmware/gateway_ecu.bin
file c_evidence/firmware/gateway_ecu_v2.bin
```

Der zuerst dokumentierte Zustand zeigte zwei leere Dateien:

```text
-rw-r--r-- 1 zukhra zukhra 0 Sep  9 11:05 c_evidence/firmware/gateway_ecu.bin
-rw-r--r-- 1 zukhra zukhra 0 Sep  9 11:05 c_evidence/firmware/gateway_ecu_v2.bin
c_evidence/firmware/gateway_ecu.bin: empty
c_evidence/firmware/gateway_ecu_v2.bin: empty
```

Anschließend wurden synthetische Testinhalte geschrieben:

```bash
echo "Firmware Version 1" > c_evidence/firmware/gateway_ecu.bin
echo "Firmware Version 2" > c_evidence/firmware/gateway_ecu_v2.bin
sha256sum c_evidence/firmware/gateway_ecu.bin
sha256sum c_evidence/firmware/gateway_ecu_v2.bin
```

Diese Dateien sind Testartefakte und keine nachgewiesenen Firmware-Dumps realer Steuergeräte.

### 9.2 Implementierungsumfang

Dokumentierte Änderungen an `b_security_tests/firmware_tests/firmware_validator.py`:

- SHA-256-Berechnung für Firmware- und Binärdateien in begrenzten Datenblöcken
- Datei-Metadaten: Name, Größe, Änderungszeitpunkt in UTC und SHA-256-Hash
- Integritätsprüfung durch Vergleich mit einem erwarteten Referenz-Hash einschließlich Formatvalidierung
- Vergleich zweier Firmware-Artefakte anhand ihrer SHA-256-Hashes
- strukturierte Fehlererfassung
- JSON-Bericht mit Audit-Metadaten wie Execution-ID, Zeitstempel, Testfall-ID, Status, Ergebnissen und Fehlern
- Export unter `c_evidence/firmware/<execution_id>/`
- zeitgestempelte Report-Dateien
- CLI-basierter Workflow für Integritätsprüfungen und Firmware-Vergleiche
- fehlende oder nicht lesbare Dateien werden als Fehler behandelt

### 9.3 Dokumentierter CLI-Lauf

```bash
python b_security_tests/firmware_tests/firmware_validator.py
```

Dokumentierte Ausgabeauszüge:

```text
[+] No CLI arguments supplied.
[+] Running default firmware comparison.

========== Firmware ==========
File      : gateway_ecu.bin
Size      : 19 Bytes
Modified  : 2026-10-18T14:53:45.935874+00:00
SHA256    : 90baf0886afbef4419916675504955dca5b3bc2993a1eec60557c1ee41570d1e
==============================
[+] Report exported -> ECU-Cyber-Integrity-Lab/c_evidence/firmware/EXEC-FW-20261018T150813-42B72D6B/firmware_report_20261018T150813Z.json
```

Der Lauf dokumentiert Datei-Metadaten und einen Report-Export. Er belegt nicht, dass alle möglichen Vergleichs- und Integritätsfälle im CLI-Lauf durchlaufen wurden.

### 9.4 Automatisierte Tests

`b_security_tests/firmware_tests/test_firmware_validator.py` enthält dokumentierte Tests für:

- SHA-256-Berechnung kleiner und größerer Binärdateien
- Datei-Metadaten
- erfolgreiche Integritätsprüfung bei übereinstimmenden Hashwerten
- fehlgeschlagene Integritätsprüfung bei abweichenden Hashwerten
- ungültige SHA-256-Eingaben
- Vergleich identischer und unterschiedlicher Firmware-Dateien
- fehlende Dateien
- JSON-Report-Erzeugung und Report-Inhalt
- Standardexport und zeitgestempelte Report-Dateien
- Nachvollziehbarkeit gespeicherter Evidence-Dateien

```bash
python -m pytest -q b_security_tests/firmware_tests/test_firmware_validator.py
```

Dokumentiertes Ergebnis: `16 passed in 1.24s`.

```bash
python -m pytest -q
```

Dokumentiertes Ergebnis: `53 passed in 0.61s`.

Diese 53 Tests sind der dokumentierte Gesamtstand nach der Firmware-Implementierung und vor dem nicht zahlenmäßig festgehaltenen Ethernet-Testlauf.

### 9.5 Sicherheitsgrenzen

Ein übereinstimmender SHA-256-Hash bestätigt, dass der untersuchte Dateiinhalt mit dem angegebenen Referenz-Hash übereinstimmt. Daraus folgt weder Authentizität noch Vertrauenswürdigkeit der Firmware.

Die Implementierung führt statische Artefaktanalyse durch. Nicht nachgewiesen werden Secure Boot, Signaturprüfungen, Bootloader-Verhalten, Flashing-Prozesse, Hardware Root of Trust, Laufzeitintegrität, ECU-Kommunikation, ECU-Ausführungsverhalten oder tatsächliche Firmware-Akzeptanz durch ein Steuergerät. Authentizität erfordert zusätzliche Vertrauensanker, beispielsweise eine korrekt geprüfte Signaturkette; Secure Boot und ECU-Akzeptanz erfordern separate Prüfungen.

---

## 10. Ethernet/IP Scanner: Validierung und Testabdeckung

### 10.1 Dokumentierte Änderungen

Für `b_security_tests/ethernet_tests/ethernet_scan.py` wurden folgende Änderungen dokumentiert:

- begrenzte Zielvalidierung: nur IP-Adresse bzw. CIDR; Netze mit mehr als 256 Adressen werden standardmäßig abgelehnt
- Portlistenvalidierung vor dem Scan, einschließlich einzelner Ports und Portbereiche; Werte 1–65535
- Ergebnisse werden pro Aufruf neu aufgebaut und deterministisch nach Host, Protokoll und Port sortiert
- strukturierte Metadaten, darunter Ziel, Ports, Scan-Art, UTC-Zeitstempel sowie Host- und Serviceanzahl
- UTF-8-JSON-Bericht
- Servicehinweise werden als Daten zurückgegeben und nicht ausschließlich auf der Konsole ausgegeben

Die Tests verwenden einen Fake-PortScanner. Dadurch wird durch diese Unit-Tests kein echter Netzwerk-Scan ausgelöst.

### 10.2 Grenzen und sichere Voreinstellungen

Der Scanner führt ein Host-/Portinventar mittels TCP-Connect-Scan durch. Er ist keine vollständige Ethernet-, SOME/IP-, DoIP-, TLS- oder ECU-Protokollprüfung.

- Ein offener Port oder ein erkannter Dienst ist kein Beweis für eine Schwachstelle.
- Ein fehlender Treffer beweist nicht, dass ein Host oder Dienst sicher ist.
- Zielbegrenzung reduziert versehentlich großflächige Scans, ersetzt aber keine Autorisierung.
- Es dürfen nur ausdrücklich freigegebene Labornetze gescannt werden.
- Fake-Scanner-Tests prüfen Datenverarbeitung und Validierung, nicht die tatsächliche `nmap`-Integration oder ein ECU im Netzwerk.

### 10.3 Ausführung und Testbefehle

Im Repository-Root:

```bash
python b_security_tests/ethernet_tests/ethernet_scan.py
python -m pytest -q b_security_tests/ethernet_tests/test_ethernet_scan.py
python -m pytest -q
```

Die übermittelten Notizen enthalten für diese Befehle keine konkrete Terminalausgabe und keine genaue Testanzahl. Deshalb wird kein Ergebnis ergänzt. Die Tests setzen `pytest` voraus. Ein in der Testdatei verwendeter Import-Fallback für fehlendes `python-nmap` ersetzt weder `python-nmap` noch die native `nmap`-Installation für einen tatsächlichen Scan.

### 10.4 Sicherheitsgrenze

Der Scanner inventarisiert beobachtbare Hosts, offene Ports und identifizierbare Netzwerkdienste in autorisierten Testumgebungen. Das unterstützt die Angriffsflächenanalyse, beweist aber weder die Sicherheit eines Steuergeräts noch die korrekte Implementierung von SOME/IP, DoIP oder anderen Automotive-Ethernet-Protokollen.

---

## 11. Chronologie der dokumentierten Regressionsergebnisse

Die Zahlen sind historische, aufeinanderfolgende Entwicklungsstände und dürfen nicht addiert werden. Gesamt-Testläufe enthalten jeweils die Tests, die zum betreffenden Zeitpunkt von pytest entdeckt wurden.

| Entwicklungsstand | Befehl bzw. Anlass | Dokumentiertes Ergebnis |
|---|---|---|
| Früher Execution-Framework-Stand | `python -m pytest -q` | `14 passed in 0.43s` |
| Runner-Smoke-Test danach | `python -m pytest -q` | `14 passed in 1.38s` |
| Adapterintegration | `python -m pytest -q` | `14 passed in 0.47s` |
| Adapter-Syntaxprüfung, danach Regression | `python -m pytest -q` | `14 passed in 0.19s` |
| Traceability/Logging | `python -m pytest -q` | `14 passed in 0.79s` |
| TestCase-/Inventory-Entwicklung | `python -m pytest -q` | `14 passed in 0.46s` |
| Inventory gezielt | `python -m pytest -q b_security_tests/test_inventory.py` | `7 passed in 0.07s` |
| Inventory integriert | `python -m pytest -q` | `21 passed in 0.38s` |
| CAN gezielt | `python -m pytest -q b_security_tests/can_tests/test_can_sniffer.py` | `7 passed in 0.17s` |
| CAN integriert | `python -m pytest -q` | `27 passed in 0.47s` |
| UDS gezielt | `python -m pytest -q b_security_tests/uds_tests/test_uds_security.py` | `13 passed in 0.34s` |
| UDS integriert | `python -m pytest -q` | `39 passed in 0.48s` |
| Firmware gezielt | `python -m pytest -q b_security_tests/firmware_tests/test_firmware_validator.py` | `16 passed in 1.24s` |
| Firmware integriert | `python -m pytest -q` | `53 passed in 0.61s` |

Für Ethernet sind die Testbefehle dokumentiert, aber keine konkrete Ausgabe. Ein späterer Abschlusslauf sollte separat mit Befehl, Datum, Umgebung und vollständiger Ausgabe festgehalten werden.


### 11.1. Dokumentierter Integrationsstand

| Bereich | Dokumentierter Stand | Abgrenzung |
|---|---|---|
| Execution Framework | Syntax-, Import-, Erfolgs- und Fehlerpfad-Smoke-Tests dokumentiert | Nicht alle Fehler- oder Parallelitätsszenarien belegt |
| TestRunner | Smoke-Test mit synthetischem Adapter dokumentiert | Keine automatische Testfallauswahl oder Security-Bewertung belegt |
| Vier Domain-Adapter | Runner-Integration mit Test-Doubles dokumentiert | Keine reale ECU- oder Fahrzeugvalidierung |
| TestCase / Inventory | Kompatibilitätsprüfung und Inventory-Tests dokumentiert | Bestehende Aufrufer dürfen nicht unbeabsichtigt brechen |
| CAN | Unit-Tests, lokaler `vcan0`-Lauf sowie JSON-/CSV-Ausgabe dokumentiert | Synthetischer Verkehr; kein realer Fahrzeugbus |
| UDS | 13 gezielte Tests und lokaler CLI-Lauf dokumentiert | CLI erhielt `No Response`; keine echte ECU-Sicherheitsbewertung |
| Firmware | 16 gezielte Tests, SHA-256-Prüfung und JSON-Report-Lauf dokumentiert | Synthetische Datei-Inhalte; keine Signatur-, Secure-Boot- oder Laufzeitprüfung |
| Ethernet/IP | Implementierungsumfang und Testbefehle dokumentiert | Keine konkrete Testausgabe in den übermittelten Notizen |
| Traceability | In-Memory-Registrierung und Abfragen dokumentiert | Persistenz über Prozesse hinweg nicht belegt |
| Logging | Logging-Boundary-Smoke-Test dokumentiert | Kein zentrales Log-Aggregationssystem belegt |
| Evidence Framework | Phase-4-Testartefakt, Hash und damalige Lifecycle-Einschränkungen dokumentiert | Automatische zentrale Verknüpfung nicht allein durch diese Notizen belegt |
| Reale Hardwareintegration | Als separate Prüfebene beschrieben | Nicht als abgeschlossen dokumentiert |


### 11.2. Nächste Integrationsschritte

Die folgenden Punkte sind offene bzw. erneut zu verifizierende Schritte, keine Behauptung bereits erledigter Arbeit:

1. **Aktuellen Repository-Zustand erfassen.** Änderungen an Framework, Adaptern, Domänenmodulen und Tests mit dem letzten dokumentierten Stand vergleichen.
2. **Ethernet-Testlauf protokollieren.** `test_ethernet_scan.py` und die vollständige Regression ausführen und Ausgabe, Python-/pytest-Version sowie Ausführungskontext sichern.
3. **Evidence-Root bestätigen.** Zentrale Evidence Records und domänenspezifische Reports als unterschiedliche Artefaktarten erfassen.
4. **Evidence-Lifecycle verifizieren.** Den aktuellen `EvidenceValidator`, Repository-Lifecycle und Association-Prüfungen anhand der implementierten Schnittstellen ausführen und Ergebnisse dokumentieren.
5. **Report-Verknüpfungen prüfen.** Verifizieren, ob domänenspezifische JSON-Berichte tatsächlich mit Execution, Testfall, Observation und zentralen Evidence Records verbunden sind oder getrennte Artefakte bleiben.
6. **Integritätsnachweise prüfen.** Hashes gegen konkrete Dateien neu berechnen und Zeitstempel, Pfade sowie Dateigrößen aus den tatsächlichen Artefakten übernehmen.
7. **Hardwaretests separat planen.** Reale CAN-/UDS-/Ethernet-/Firmware-Validierung nur mit autorisiertem Ziel, dokumentierter Konfiguration und geeigneter Laborumgebung durchführen.
8. **Status nicht überinterpretieren.** `COMPLETED` beschreibt einen Ausführungsstatus; es bedeutet nicht automatisch einen fachlichen Security-`PASS`.

### Abschlussnotiz

Die dokumentierten erfolgreichen Unit-Tests und Smoke-Tests belegen die jeweils geprüften Softwarepfade. 

Diese Integrationsnotizen dokumentieren die schrittweise Entwicklung und Prüfung gemeinsamer Framework-Schnittstellen sowie der CAN-, UDS-, Firmware- und Ethernet/IP-Komponenten. Sie halten konkrete Befehle und historische Testergebnisse fest und trennen synthetische Tests, lokale Simulationen und statische Artefaktprüfungen von realer Fahrzeugvalidierung.
