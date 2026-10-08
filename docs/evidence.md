# Evidence Framework — ECU-Cyber-Integrity-Lab

## 1. Purpose

This document defines the Phase-4 Evidence Framework for creation, validation, association, provenance, storage, lifecycle management and controlled use of assessment evidence.

The framework separates evidence from test definitions, observations, results, findings and verification conclusions.

```text
Test
  ↓
Execution
  ↓
Observation
  ↓
Evidence
  ↓
Result
  ↓
Assessment / Finding
  ↓
Verification
```

The framework does not create security findings and does not establish real ECU, vehicle, production or OEM validation.

## 2. Evidence Definition

Evidence is a technical artifact or set of artifacts that supports an identifiable execution observation, execution result, assessment statement or verification activity.

Evidence may include:

```text
Execution logs
Test output
Protocol captures
CAN captures
Network scan output
Firmware analysis output
JSON / CSV / TXT result files
Screenshots
Generated reports
Hashes and integrity metadata
Tool output
Configuration relevant to execution
```

Evidence is only interpreted within the provenance and context that can actually be established.

The following distinctions are mandatory:

```text
Expected Behaviour != Actual Observation
Test Definition != Execution
Execution != Observation
Observation != Evidence
Evidence != Finding
Evidence != Verification
```

### Implementation status

`a_framework/evidence.py` implements the canonical evidence record, validation, lifecycle transitions, artifact integrity metadata and JSON-backed evidence-record storage.

## 3. Canonical Evidence Record

The canonical record is represented by `EvidenceRecord` in `a_framework/evidence.py`.

Required fields are:

```text
Evidence Identifier
test_id
execution_id
Target
Environment
Preconditions
Input
Expected Behaviour
Actual Observation
Execution Status
Result
Timestamp
Artifacts
Tooling
Execution Method
Context Classification
Provenance
Evidence Status
Associations
```

Additional integrity and lifecycle-history fields are supported where applicable.

Unavailable information remains explicitly represented as `null`/empty data. The implementation does not infer missing target, environment, execution or provenance data from the artifact filename.

## 4. Evidence Identifier

Evidence identifiers are unique within the project evidence record set.

The identifier is the stable reference for an evidence record and must not be silently reused for unrelated evidence.

The repository implementation stores records as:

```text
c_evidence/records/<Evidence-ID>.json
```

## 5. Evidence Provenance Model

Provenance records, where available:

```text
Origin
Target
Environment
Execution Method
Tooling
Timestamp
Source Artifact
Generating Process
Relevant Test
Relevant Execution
```

Missing provenance remains missing. A stored artifact hash verifies the current stored artifact bytes; it does not prove the origin or original capture history of the artifact.

## 6. Evidence Validation Model

Evidence validation evaluates suitability for its intended assessment use.

The framework supports checks for:

```text
Identity
Integrity
Provenance
Structure
Context
Association
Completeness
Consistency
```

Evidence validation is not security verification.

```text
Evidence Validation
    !=
Security Verification
```

`EvidenceValidator` rejects a `PASS` or `FAIL` record without the minimum execution, observation and artifact information required by the result semantics.

## 7. Evidence Association Model

The association model is:

```text
Assessment Objective
        ↓
Security Property
        ↓
Test Objective
        ↓
Test
        ↓
Execution
        ↓
Observation
        ↓
Evidence
        ↓
Result
        ↓
Finding / Assessment
        ↓
Verification Activity
```

Phase 4 establishes the evidence-side representation. Finding and verification implementation remains outside Phase-4 scope.

The implementation represents associations as named identifier lists, allowing relationships to be recorded without inventing objects that do not exist.

## 8. Evidence Storage Model

The repository separates:

```text
c_evidence/
    Evidence artifacts and evidence records

d_examples/
    Methodological/example material

e_security_reports/
    Reporting outputs
```

Evidence records are stored under:

```text
c_evidence/records/
```

Verification execution evidence generated during Phase 4 is stored separately under:

```text
c_evidence/verification/
```

Evidence records reference the underlying artifact rather than replacing it.

## 9. Evidence Classification Model

Context classification describes origin/execution context:

```text
REAL
VIRTUAL
SIMULATED
LOCAL
STATIC
SYNTHETIC
```

These classifications are independent of the result state and lifecycle state.

`PASS`, `FAIL`, `NOT_RUN`, `INCONCLUSIVE` and `BLOCKED` are result states, not context classifications.

A virtual, simulated, local, static or synthetic artifact does not become real-world validation evidence through classification alone.

## 10. Lifecycle

The lifecycle is:

```text
CREATED
  ↓
VALIDATED
  ↓
ASSOCIATED
  ↓
ACTIVE
  ├──→ SUPERSEDED → ARCHIVED
  └──→ ARCHIVED
```

Allowed transitions are enforced by the implementation. Historical evidence is not silently overwritten. The repository rejects reuse of an existing evidence-record identifier; a new artifact requires a new evidence identifier and an explicit supersession relationship where applicable.

When evidence is superseded, the original identifier remains traceable and the replacement relationship is represented explicitly.

## 11. Integrity Handling

The implementation calculates SHA-256 and stored file size for referenced artifacts.

The integrity metadata establishes the identity of the currently stored artifact bytes at the time of the integrity check.

It does not establish:

```text
Original capture authenticity
Real ECU provenance
Original execution environment
Security verification
```

Those properties require their own evidence.

## 12. Result and Evidence Boundary

The framework uses:

```text
PASS
FAIL
NOT_RUN
INCONCLUSIVE
BLOCKED
```

`PASS` and `FAIL` require actual execution, a defined evaluation basis, an actual observation and supporting evidence.

The framework never converts:

```text
NOT_RUN → PASS
INCONCLUSIVE → PASS
EXPECTED → OBSERVED
SIMULATED → REAL
```

## 13. Reproducibility

An evidence record supports reproducibility when the relevant information is available:

```text
Test Identifier
Test Definition
Execution Identifier
Target
Environment
Preconditions
Input
Tooling
Execution Method
Timestamp
Observation
Artifact
Provenance
Result
```

The framework does not claim reproducibility when required target, interface or environment prerequisites are unavailable.

## 14. Real-World Boundary

Real ECU or vehicle validation requires, at minimum:

```text
REAL TARGET
HARDWARE
REAL ENVIRONMENT
EXECUTION
OBSERVATION
EVIDENCE
PROVENANCE
VALIDATION CONCLUSION
```

## 15. Finding Boundary

Evidence may support a later assessment or finding, but evidence existence alone does not establish a confirmed security finding.

```text
Evidence
  ↓
Supported Observation
  ↓
Supported Result
  ↓
Supported Assessment
```

# Existing Evidence Inventory

## 1. Review Basis

The inventory reflects the evidence artifacts present in the supplied repository snapshot under `c_evidence/`.

The artifact files were inspected for available content and metadata. The existence of an artifact is not treated as proof of execution or evidence validity.

Classification values used here are:

```text
PROJECT EVIDENCE
EXAMPLE / SAMPLE
GENERATED ARTIFACT
UNVERIFIED ARTIFACT
UNKNOWN PROVENANCE
DOCUMENTATION ARTIFACT
REPORT OUTPUT
NOT EVIDENCE
```

Context classification is kept separate from artifact classification.

## 2. Inventory

| Evidence ID | Artifact | Type | Origin / Context | Target | Environment | Timestamp | Tooling / Method | Provenance | Status | Association | Classification | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EV-CAN-001 | `c_evidence/can/can_capture.json` | CAN capture | UNKNOWN | UNKNOWN | UNKNOWN | `2026-07-23T14:23:11` and `2026-07-23T14:23:12` in artifact | UNKNOWN | INCOMPLETE | CREATED | None established | UNVERIFIED ARTIFACT | Target, environment, method and execution identity are missing |
| EV-CAN-002 | `c_evidence/can/new_can_capture.json` | CSV/header artifact | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | CREATED | None established | UNKNOWN PROVENANCE | Header-only artifact; no observation data |
| EV-CAN-003 | `c_evidence/can/example_output_can.txt` | Example output | STATIC / example material | N/A | N/A | UNKNOWN | UNKNOWN | Example source only | N/A | None | EXAMPLE / SAMPLE | Not execution evidence |
| EV-ETH-001 | `c_evidence/ethernet/example_output_ethernet_scan.txt` | Example scan output | STATIC / example material | N/A | N/A | UNKNOWN | UNKNOWN | Example source only | N/A | None | EXAMPLE / SAMPLE | Not execution evidence |
| EV-FW-001 | `c_evidence/firmware/firmware_report.json` | Firmware report | UNKNOWN | UNKNOWN | UNKNOWN | `2026-08-22T21:41:38.897410` | UNKNOWN | INCOMPLETE | CREATED | None established | UNVERIFIED ARTIFACT | Report contains PASS/FAIL-style data but no established execution provenance |
| EV-FW-002 | `c_evidence/firmware/new_firmware_report` | Firmware report | UNKNOWN | UNKNOWN | UNKNOWN | `2026-07-25T14:15:10` | UNKNOWN | UNKNOWN | CREATED | None established | UNKNOWN PROVENANCE | Contains PASS text without execution provenance |
| EV-FW-003 | `c_evidence/firmware/gateway_ecu.bin` | Firmware artifact | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | N/A | None established | UNKNOWN PROVENANCE | Artifact is listed in the repository tree; binary bytes were not present in the supplied text snapshot |
| EV-FW-004 | `c_evidence/firmware/gateway_ecu_v2.bin` | Firmware artifact | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | N/A | None established | UNKNOWN PROVENANCE | Artifact is listed in the repository tree; binary bytes were not present in the supplied text snapshot |
| EV-FW-005 | `c_evidence/firmware/example_output_firmware_validator.txt` | Example output | STATIC / example material | N/A | N/A | `2026-07-25T13:18:11` in example text | UNKNOWN | Example source only | N/A | None | EXAMPLE / SAMPLE | Not execution evidence |
| EV-UDS-001 | `c_evidence/uds/uds_report.json` | UDS report | UNKNOWN | UNKNOWN | UNKNOWN | `2026-08-22T21:53:20.042477` through `21:53:26.050405` | UNKNOWN | INCOMPLETE | CREATED | None established | UNVERIFIED ARTIFACT | Requests/responses are recorded as No Response; target and method are missing |
| EV-UDS-002 | `c_evidence/uds/new_uds_report` | UDS report | UNKNOWN | UNKNOWN | UNKNOWN | `2026-07-25T15:18:22` | UNKNOWN | UNKNOWN | CREATED | None established | UNKNOWN PROVENANCE | Positive SecurityAccess response is not independently traceable to an execution |
| EV-UDS-003 | `c_evidence/uds/example_output_uds_security.txt` | Example output | STATIC / example material | N/A | N/A | UNKNOWN | UNKNOWN | Example source only | N/A | None | EXAMPLE / SAMPLE | Explicitly contains planned governance separation; not execution evidence |
| EV-P4-VER-001 | `c_evidence/verification/pytest_evidence_framework.txt` | Framework verification log | LOCAL | Evidence Framework implementation | Local reconstructed repository snapshot | `2026-09-25T10:52:01Z` | pytest / command line | ESTABLISHED | ACTIVE | VC-01…VC-20 as listed in record | PROJECT EVIDENCE | Framework verification only; not ECU/vehicle security validation |
| EV-P4-VER-003 | `c_evidence/verification/pytest_evidence_framework_EXEC-P4-VER-003.txt` | Framework verification log | LOCAL | Evidence Framework implementation | Local reconstructed repository snapshot | `2026-09-25T10:56:28Z` | pytest / command line | ESTABLISHED | ACTIVE | VC-01…VC-20 as listed in record | PROJECT EVIDENCE | Latest framework verification execution; not ECU/vehicle security validation |

## 3. Stored Artifact Integrity

For the text artifacts available in the supplied snapshot, current stored SHA-256 values were calculated during the Phase-4 working review. These hashes identify the current stored bytes and do not establish original capture provenance.

```text
c_evidence/can/can_capture.json
4155c833eb8814a17e7020252880a811bebca0331ad50d3c41b5bdc40240abf8

c_evidence/can/example_output_can.txt
c936c66c926fd2aff56f76185243d7f014e11123a074fcfc8be6326098d29c32

c_evidence/can/new_can_capture.json
109e6d7b0ce073357fb55c2dd478d967f04f98fb8559efce88eab9a49738a5b5

c_evidence/ethernet/example_output_ethernet_scan.txt
94e1b2c0b5cefd7889a3ae116a37f5e136e1a7eaab68d163547f4ae6f99cb9de

c_evidence/firmware/firmware_report.json
9247200e8d3553d22c169ad44abec985cd98fee676da33f7b4f8182702897164

c_evidence/firmware/new_firmware_report
9f42d65d189ae1eb1e6c5a20895bef53aa0b010cad900e5f22806f8b540d65e5

c_evidence/firmware/example_output_firmware_validator.txt
8ad5c8f1757d84ac1159a23de65057fb026a3c3f56187ae3ec239a156b7add9d

c_evidence/uds/uds_report.json
9cf06bef5697e3a8cde3fe69fcd5632ab3b4aada39a3f4b7541f796e913f71dc

c_evidence/uds/new_uds_report
b7a73576c542e7b66fd3f103635eedb2e65672671f8f0ed1e1d777b1ff242225

c_evidence/uds/example_output_uds_security.txt
efab832a9de077fe10d92f56c9032141e7ab0d8581364018e8a1c2533a386d4c
```

## 4. Inventory Conclusion

The supplied repository snapshot contains evidence-like artifacts, examples and generated reports, but most existing assessment artifacts lack the provenance and execution association required for validated project evidence.

# Evidence Traceability Matrix

## 1. Traceability Model

```text
Assessment Objective
        ↓
Security Property
        ↓
Test Objective
        ↓
Test
        ↓
Execution
        ↓
Observation
        ↓
Evidence
        ↓
Result
        ↓
Finding / Assessment
        ↓
Verification Activity
```

Phase 4 establishes the evidence-side relationships without creating findings or later-phase verification workflows.

## 2. Framework Verification Traceability

| Requirement / Objective | Implementation                                          | Test                                                                                            | Execution         | Observation                                                                                             | Evidence        | Result | Documentation      |
| ----------------------- | ------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ----------------- | ------------------------------------------------------------------------------------------------------- | --------------- | ------ | ------------------ |
| Evidence record model   | `a_framework/evidence.py::EvidenceRecord`               | `a_framework/test_evidence.py::test_framework_accepts_well_formed_synthetic_record`             | `EXEC-P4-VER-001` | Well-formed synthetic evidence record accepted by the framework validation path                         | `EV-P4-VER-001` | PASS   | `docs/evidence.md` |
| Lifecycle control       | `a_framework/evidence.py::EvidenceRecord.transition_to` | `a_framework/test_evidence.py::test_lifecycle_allows_valid_path_and_rejects_reverse_transition` | `EXEC-P4-VER-001` | Valid lifecycle transition accepted; invalid reverse transition rejected                                | `EV-P4-VER-001` | PASS   | `docs/evidence.md` |
| Evidence storage        | `a_framework/evidence.py::EvidenceRepository`           | `a_framework/test_evidence.py::test_repository_round_trip_and_no_overwrite`                     | `EXEC-P4-VER-001` | Evidence record persisted and reloaded successfully; repository refused overwrite of an existing record | `EV-P4-VER-001` | PASS   | `docs/evidence.md` |
| PASS guard              | `a_framework/evidence.py::EvidenceValidator`            | `a_framework/test_evidence.py::test_pass_without_execution_metadata_is_rejected`                | `EXEC-P4-VER-001` | PASS record without required execution metadata was rejected                                            | `EV-P4-VER-001` | PASS   | `docs/evidence.md` |

## 3. Existing Security-Test Evidence Traceability

| Domain | Test / Artifact | Execution | Observation | Evidence | Result | Traceability State |
| --- | --- | --- | --- | --- | --- | --- |
| CAN | `b_security_tests/can_tests/test_can_sniffer.py` / `EV-CAN-001` | NOT ESTABLISHED | Artifact contains two timestamped CAN rows | `EV-CAN-001` | NOT ESTABLISHED | PARTIAL / UNVERIFIED |
| UDS | `b_security_tests/uds_tests/test_uds_security.py` / `EV-UDS-001` | NOT RUN / test file is placeholder in supplied snapshot | Report contains No Response records | `EV-UDS-001` | NOT ESTABLISHED | PARTIAL / UNVERIFIED |
| Firmware | `b_security_tests/firmware_tests/test_firmware_validator.py` / `EV-FW-001` | BLOCKED in supplied snapshot because test file is syntactically invalid placeholder | Report contains FAIL/identical values | `EV-FW-001` | NOT ESTABLISHED | UNVERIFIED |
| Ethernet | `b_security_tests/ethernet_tests/test_ethernet_scan.py` / `EV-ETH-001` | BLOCKED / no executable test established | Example text contains scan output | `EV-ETH-001` | NOT ESTABLISHED | EXAMPLE / SAMPLE |

The existing domain rows do not support confirmed security findings. Their evidence associations remain incomplete until execution provenance is established.

## 4. Missing Relationships

The following relationships remain unestablished for the existing domain artifacts:

```text
Test → Execution
Execution → Observation
Observation → Evidence
Evidence → Result
```