# Domain Architecture Matrix

## 1. Purpose

This document defines the technical architecture and current implementation mapping of the security-test domains used by the project.

It connects the common Security Test Architecture with the concrete domain implementations and their respective adapters.

The document provides a single technical view of:

* supported security-test domains
* domain-specific modules
* domain adapter boundaries
* target / model classification
* common test-architecture integration
* current implementation status
* execution status
* verification status
* architecture traceability
* remaining architecture gaps

The document describes the current technical state of the repository and the architecture established for structured security testing.

---

## 2. Domain Scope

The security-test architecture currently distinguishes the following domains:

```text
CAN
UDS
Firmware
Ethernet
Bootloader / OTA
```

The repository contains concrete implementation structures for:

```text
CAN
UDS
Firmware
Ethernet
```

Bootloader / OTA remains part of the defined security-testing architecture and project context. It is not represented as an implemented test domain unless corresponding repository implementation exists.

The architecture therefore distinguishes:

```text
ARCHITECTURALLY SUPPORTED DOMAIN

        !=

IMPLEMENTED DOMAIN

        !=

EXECUTED DOMAIN

        !=

VERIFIED DOMAIN
```

---

## 3. Domain Architecture Matrix

| Domain           | Domain Module                                      | Domain Adapter                                           | Target / Model                                        | Main Technical Responsibility                                                 | Implementation Status               | Execution Status | Verification Status |
| ---------------- | -------------------------------------------------- | -------------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------- | ---------------- | ------------------- |
| CAN              | `b_security_tests/can_tests/can_sniffer.py`             | `b_security_tests/can_tests/adapter.py::CANAdapter`           | CAN interface / virtual CAN                           | Capture, generation, filtering, statistics and CSV handling                   | IMPLEMENTED                         | LOCAL TESTS EXECUTED | LOCAL TESTS REPORTED PASS; REAL-TARGET VALIDATION NOT ESTABLISHED |
| UDS              | `b_security_tests/uds_tests/uds_security.py`            | `b_security_tests/uds_tests/adapter.py::UDSAdapter`           | Diagnostic target / simulated or local target context | UDS request / response interaction and SecurityAccess response classification | IMPLEMENTED                         | LOCAL TESTS EXECUTED | LOCAL TESTS REPORTED PASS; REAL-TARGET VALIDATION NOT ESTABLISHED |
| Firmware         | `b_security_tests/firmware_tests/firmware_validator.py` | `b_security_tests/firmware_tests/adapter.py::FirmwareAdapter` | Firmware artifact / local artifact                    | Firmware hashing, comparison and reporting                                    | IMPLEMENTED                         | LOCAL TESTS EXECUTED | LOCAL TESTS REPORTED PASS; REAL-TARGET VALIDATION NOT APPLICABLE / NOT ESTABLISHED |
| Ethernet         | `b_security_tests/ethernet_tests/test_ethernet_scan.py`      | `b_security_tests/ethernet_tests/adapter.py::EthernetAdapter` | Network / host / service environment                  | Host discovery, IP/network scanning and service inventory                     | IMPLEMENTED                         | SCANNER IMPLEMENTED; TEST SUITE NOT ESTABLISHED | NOT ESTABLISHED |
| Bootloader / OTA | No concrete implementation established             | No concrete adapter established                          | Project-defined target / model                        | Architecturally supported security-testing domain                             | PLANNED / ARCHITECTURALLY SUPPORTED | NOT RUN          | NOT ESTABLISHED     |

The matrix separates domain implementation, local module-test execution and target-level verification.

The Phase-5 test run is reported by the project owner as successful. This status applies to the covered local tests; it must not be generalized to real ECU/vehicle execution or to domains for which a pytest suite is not established. An implemented module or adapter alone does not establish successful test execution or security verification.

---

## 4. CAN Domain

### 4.1 Domain Role

The CAN domain provides security-testing capabilities for CAN communication and CAN traffic analysis.

The domain-specific implementation covers the technical processing of CAN traffic.

### 4.2 Domain Module

```text
b_security_tests/can_tests/can_sniffer.py
```

The CAN module provides the existing CAN-specific functionality, including:

```text
CAN traffic capture
Virtual CAN traffic generation
CAN message filtering
CAN message statistics
CAN CSV export
```

### 4.3 Domain Adapter

```text
b_security_tests/can_tests/adapter.py::CANAdapter
```

The `CANAdapter` connects the common security-test execution architecture with the CAN-specific implementation.

Its responsibility is the domain integration boundary.

The adapter does not replace the CAN domain module and does not redefine common test semantics.

### 4.4 Target / Model

The CAN domain can operate against a CAN interface or virtual CAN environment.

The target classification remains dependent on the concrete execution context.

```text
CAN Interface
Virtual CAN
```

A virtual CAN environment does not constitute real ECU or vehicle validation.

### 4.5 Architecture Status

```text
Domain Module       = IMPLEMENTED
Domain Adapter      = IMPLEMENTED
Common Integration  = IMPLEMENTED
Local module tests  = REPORTED PASS where test coverage exists
Real target execution = NOT ESTABLISHED
Security verification = NOT ESTABLISHED
```

---

## 5. UDS Domain

### 5.1 Domain Role

The UDS domain provides diagnostic communication and SecurityAccess-related security-testing capabilities.

### 5.2 Domain Module

```text
b_security_tests/uds_tests/uds_security.py
```

The existing UDS implementation provides basic:

```text
UDS request / response interaction
SecurityAccess response classification
```

### 5.3 Domain Adapter

```text
b_security_tests/uds_tests/adapter.py::UDSAdapter
```

The `UDSAdapter` provides the integration boundary between the common test architecture and the UDS implementation.

UDS-specific protocol handling remains within the UDS domain implementation.

### 5.4 Target / Model

The UDS target context is represented through the common target/model boundary.

Possible contexts include:

```text
Diagnostic target
Simulated target
Local test environment
```

The target classification must reflect the actual execution environment.

### 5.5 Architecture Status

```text
Domain Module       = IMPLEMENTED
Domain Adapter      = IMPLEMENTED
Common Integration  = IMPLEMENTED
Local module tests  = REPORTED PASS where test coverage exists
Real target execution = NOT ESTABLISHED
Security verification = NOT ESTABLISHED
```

---

## 6. Firmware Domain

### 6.1 Domain Role

The Firmware domain provides security-testing functionality for firmware artifacts.

### 6.2 Domain Module

```text
b_security_tests/firmware_tests/firmware_validator.py
```

The firmware implementation provides:

```text
SHA-256 firmware hashing
Firmware comparison
Firmware JSON reporting
```

### 6.3 Domain Adapter

```text
b_security_tests/firmware_tests/adapter.py::FirmwareAdapter
```

The `FirmwareAdapter` connects the common test architecture with firmware-specific processing.

The adapter provides the domain boundary without moving firmware-specific algorithms into the common test framework.

### 6.4 Target / Model

The firmware domain normally operates on a local or static firmware artifact.

```text
Firmware Artifact
Local Artifact
Static Artifact
```

The artifact itself is not treated as evidence of runtime ECU behaviour.

### 6.5 Architecture Status

```text
Domain Module       = IMPLEMENTED
Domain Adapter      = IMPLEMENTED
Common Integration  = IMPLEMENTED
Local module tests  = REPORTED PASS where test coverage exists
Real target execution = NOT ESTABLISHED
Security verification = NOT ESTABLISHED
```

---

## 7. Ethernet Domain

### 7.1 Domain Role

The Ethernet domain provides network and service-discovery capabilities for security testing.

### 7.2 Domain Module

```text
b_security_tests/ethernet_tests/test_ethernet_scan.py
```

The current Ethernet scanner implementation provides bounded target/port validation, TCP connection scanning, inventory/service hints and JSON export. The repository snapshot places the scanner implementation in `b_security_tests/ethernet_tests/test_ethernet_scan.py`; despite the filename, that file does not contain `test_*` pytest functions. Therefore, the presence of this file must not be counted as proof of an Ethernet pytest suite or passing Ethernet test cases.

### 7.3 Domain Adapter

```text
b_security_tests/ethernet_tests/adapter.py::EthernetAdapter
```

The `EthernetAdapter` is the intended integration boundary between the common test architecture and Ethernet-specific network interaction. The snapshot contains an adapter file, but the scanner implementation and the adapter should not be treated as proof of a passing Ethernet pytest suite. Network-specific processing remains within the Ethernet domain.

### 7.4 Target / Model

The Ethernet domain operates against a network, host, or service environment.

```text
Network
Host
Service Environment
```

The target classification depends on the actual execution environment.

### 7.5 Architecture Status

```text
Domain Module       = IMPLEMENTED
Domain Adapter      = IMPLEMENTED
Common Integration  = IMPLEMENTED
Local module tests  = REPORTED PASS where test coverage exists
Real target execution = NOT ESTABLISHED
Security verification = NOT ESTABLISHED
```

---

## 8. Bootloader / OTA Domain

Bootloader / OTA is part of the supported security-testing model and architectural scope.

No concrete repository implementation is established for this domain in the current domain architecture mapping.

Accordingly:

```text
Domain              = ARCHITECTURALLY SUPPORTED
Domain Module       = NOT IMPLEMENTED
Domain Adapter      = NOT IMPLEMENTED
Execution           = NOT RUN
Verification        = NOT ESTABLISHED
```

The domain must remain distinguishable from CAN, UDS, Firmware and Ethernet, where concrete repository implementation exists.

---

## 9. Cross-Domain Adapter Model

The common architecture uses a domain adapter as the boundary between common test semantics and domain-specific technical interaction.

```text
Assessment Objective
        |
        v
Security Objective / Property
        |
        v
Test Objective
        |
        v
Security Test Case
        |
        v
Test Runner
        |
        v
Domain Adapter
        |
        v
Domain Module
        |
        v
Target / Model
        |
        v
Observation
        |
        v
Result
```

The concrete adapter mapping is:

```text
CAN
    |
    +-- CANAdapter
    |
    +-- CAN domain module

UDS
    |
    +-- UDSAdapter
    |
    +-- UDS domain module

Firmware
    |
    +-- FirmwareAdapter
    |
    +-- Firmware domain module

Ethernet
    |
    +-- EthernetAdapter
    |
    +-- Ethernet domain module
```

The adapter boundary keeps common test semantics separate from domain-specific implementation.

---

## 10. Domain Separation

The architecture separates common test responsibilities from domain-specific technical responsibilities.

### Common Architecture Responsibilities

```text
Test Case
Test Objective
Preconditions
Expected Behaviour
Oracle / Evaluation Criteria
Result Semantics
Execution Lifecycle
Target / Model Context
Execution Status
```

### Domain Responsibilities

```text
CAN
    CAN communication and traffic processing

UDS
    Diagnostic communication and SecurityAccess processing

Firmware
    Firmware artifact processing

Ethernet
    Network and service interaction
```

The common architecture controls the test lifecycle and result semantics.

The domain implementation controls domain-specific technical interaction.

A domain implementation must not silently redefine common result semantics.

---

## 11. Domain Target / Model Classification

The target / model boundary represents the technical object or environment against which a test operates.

The architecture supports the following classifications:

```text
REAL
VIRTUAL
SIMULATED
LOCAL
STATIC
SYNTHETIC
```

Examples within the current domain structure include:

| Domain   | Target / Model Example     | Classification         |
| -------- | -------------------------- | ---------------------- |
| CAN      | CAN interface              | Depends on environment |
| CAN      | Virtual CAN                | VIRTUAL                |
| UDS      | Diagnostic test target     | Depends on environment |
| UDS      | Simulated target           | SIMULATED              |
| Firmware | Firmware artifact          | STATIC / LOCAL         |
| Ethernet | Network / host environment | Depends on environment |

The target classification describes the technical execution context.

It does not by itself establish:

```text
Real ECU Validation
Vehicle Validation
Production Validation
OEM Validation
```

---

## 12. Architecture-DELTA Implementation

This established the common architecture integration required to connect the existing security domains with the Security Test Architecture.

The implementation is structured around the smallest common architectural elements required for domain integration.

### 12.1 Common Test-Case Model

The common Test Case structure is represented by:

```text
a_framework/test_architecture.py::TestCase
```

The common model contains the architectural test metadata required for structured security testing, including:

```text
Test Identifier
Test Name
Security Domain
Assessment Objective
Security Objective / Property
Test Objective
Preconditions
Inputs
Actions
Expected Behaviour
Oracle / Evaluation Criteria
Validity Scope
Applicable Target / Model
```

Status:

```text
IMPLEMENTED
```

---

### 12.2 Test Runner

The common execution controller is represented by:

```text
a_framework/runner.py::TestRunner
```

The current `TestRunner` coordinates a single operation on an already-selected domain adapter through the execution interface. Adapter execution and observation normalization are delegated to that interface.

The implemented responsibility is limited to:

```text
Accept an already-selected adapter
Pass operation inputs to the execution interface
Receive an ExecutionOutcome
Coordinate one adapter operation
Propagate execution errors
```

The runner does not itself implement general test selection, test-suite orchestration, oracle evaluation, PASS/FAIL assignment, or automatic Evidence Framework creation. Those responsibilities must not be inferred from the presence of the runner.

Status:

```text
SINGLE-OPERATION COORDINATION = IMPLEMENTED
FULL TEST-CASE ORCHESTRATION = NOT ESTABLISHED
```

---

### 12.3 Domain Adapter

The common architecture defines a Domain Adapter boundary between the Test Runner and the domain-specific implementation.

Concrete adapters are established for the implemented domains:

```text
CANAdapter
UDSAdapter
FirmwareAdapter
EthernetAdapter
```

The adapters preserve the existing domain responsibilities while providing the common integration boundary.

Status:

```text
IMPLEMENTED
```

---

### 12.4 Execution Interface

The common execution contract is represented by:

```text
ExecutionInterface
```

The execution interface provides the architectural contract for:

```text
Initialization
Precondition handling
Target / Model access
Input handling
Execution request
Observation retrieval
Execution status
Error handling
Result handoff
```

Domain adapters implement the execution boundary required by the common architecture.

Status:

```text
IMPLEMENTED
```

---

### 12.5 Target / Model Context

The common target context is represented by:

```text
TargetContext
```

The target context is passed through the common execution path so that target/model information remains separate from domain-specific implementation details.

The target context preserves the distinction between the technical target and the execution mechanism.

Status:

```text
IMPLEMENTED
```

---

### 12.6 Observation and Result

The common architecture provides explicit structures for observation and result handling:

```text
Observation
ResultStatus
ExecutionStatus
TestResult
```

The result states are:

```text
PASS
FAIL
NOT_RUN
INCONCLUSIVE
BLOCKED
```

Observation represents actual execution output.

Result represents the evaluated outcome of execution against the defined oracle or evaluation criteria.

The architecture therefore preserves:

```text
Expected Behaviour
        !=
Actual Observation
        !=
Result
```

Status:

```text
IMPLEMENTED
```

---

### 12.7 Oracle / Evaluation

The common architecture defines an explicit oracle/evaluation boundary in its model. The conceptual evaluation flow is:

```text
Test Objective
        |
        v
Expected Behaviour
        |
        v
Oracle / Evaluation Criteria
        |
        v
Actual Observation
        |
        v
Result
```

The evaluation responsibility is located at the common test-architecture level rather than being redefined independently by each domain.

A missing or insufficient oracle may result in:

```text
INCONCLUSIVE
```

where the defined evaluation criteria do not establish a valid PASS or FAIL decision.

Status:

```text
ARCHITECTURAL BOUNDARY = DEFINED
END-TO-END RUNNER EVALUATION = NOT ESTABLISHED
```

---

### 12.8 Architecture Traceability

The common Test Case structure includes the objective relationship required for architecture-level traceability.

The traceability structure is represented by:

```text
a_framework/traceability.py::Traceability
```

The minimum relationship is:

```text
Assessment Objective
        |
        v
Security Objective / Property
        |
        v
Test Objective
        |
        v
Test Case
        |
        v
Execution
        |
        v
Observation
        |
        v
Result
```

The architecture does not extend this boundary into the later Evidence Framework or Finding Lifecycle.

Status:

```text
IMPLEMENTED
```

---

### 12.9 Logging Boundary

The logging boundary is represented by:

```text
a_framework/logging_boundary.py
```

The logging boundary exposes logging functionality without treating log output itself as a test result.

The architecture preserves the distinction:

```text
Logging
    !=
Observation
    !=
Result
```

Status:

```text
IMPLEMENTED
```

---

### 12.10 Reporting Boundary

The repository contains a legacy `a_framework/report_generator.py` that consolidates domain JSON files into JSON, Markdown and HTML reports. The available snapshot does not establish an end-to-end connection from `TestRunner`/`ExecutionOutcome` to a common test-result reporting API.

The architecture must therefore distinguish:

```text
Legacy module/finding report generation = PRESENT
Common test-result reporting integration = NOT ESTABLISHED
```

Reporting consumes information; it does not create a test result merely because a report is generated.

Status:

```text
LEGACY REPORT GENERATION = IMPLEMENTED
END-TO-END TEST-RESULT REPORTING = NOT ESTABLISHED
```

---

### 12.11 Domain Architecture Mapping

The concrete domain adapter mapping established for the architecture is:

| Domain           | Domain Module                                           | Adapter                | Target / Model Context         | Status                    |
| ---------------- | ------------------------------------------------------- | ---------------------- | ------------------------------ | ------------------------- |
| CAN              | `b_security_tests/can_tests/can_sniffer.py`             | `CANAdapter`           | CAN interface / virtual CAN    | IMPLEMENTED               |
| UDS              | `b_security_tests/uds_tests/uds_security.py`            | `UDSAdapter`           | Diagnostic / simulated target  | IMPLEMENTED               |
| Firmware         | `b_security_tests/firmware_tests/firmware_validator.py` | `FirmwareAdapter`      | Firmware artifact              | IMPLEMENTED               |
| Ethernet         | `b_security_tests/ethernet_tests/test_ethernet_scan.py`      | `EthernetAdapter`      | Network / host environment     | IMPLEMENTED               |
| Bootloader / OTA | No concrete module established                          | No adapter established | Project-defined target / model | ARCHITECTURALLY SUPPORTED |

The adapter mapping establishes the intended and implemented integration boundary for the concrete repository domains.

Status:

```text
IMPLEMENTED
```

for CAN, UDS, Firmware and Ethernet.

Bootloader / OTA remains architecturally supported without a corresponding implemented adapter.

---

## 13. Domain Integration Status

Following the common architecture implementation, the current integration state is:

```text
Common Test Case Model
        = IMPLEMENTED

Test Runner
        = IMPLEMENTED

Domain Adapter Boundary
        = IMPLEMENTED

Execution Interface
        = IMPLEMENTED

Target / Model Context
        = IMPLEMENTED

Observation / Result Structures
        = IMPLEMENTED

Oracle / Evaluation Boundary
        = IMPLEMENTED

Architecture Traceability
        = IMPLEMENTED

Logging Boundary
        = IMPLEMENTED

Legacy Reporting Component
        = IMPLEMENTED

End-to-End Test-Result Reporting
        = NOT ESTABLISHED
```

Concrete domain integration:

```text
CAN
    = IMPLEMENTED

UDS
    = IMPLEMENTED

Firmware
    = IMPLEMENTED

Ethernet
    = IMPLEMENTED

Bootloader / OTA
    = ARCHITECTURALLY SUPPORTED
```

Implementation status does not establish execution or verification status.

---

## 14. Execution Status

The current architecture provides the structures required for execution.

The project owner reports that the Phase-5 test run completed successfully and evidence was created. The available source snapshot supports the existence of focused pytest modules for CAN, UDS and Firmware, with test doubles/local artifacts used by those tests. No consolidated Phase-5 test log or aggregate test count is established by this document, and the Ethernet scanner file is implementation rather than a pytest suite.

Current execution status:

```text
CAN        = LOCAL MODULE TESTS REPORTED PASS
UDS        = LOCAL MODULE TESTS REPORTED PASS
Firmware   = LOCAL MODULE TESTS REPORTED PASS
Ethernet   = SCANNER IMPLEMENTED; PYTEST COVERAGE NOT ESTABLISHED
Bootloader / OTA = NOT RUN
```

The architecture therefore distinguishes implementation from execution:

```text
DESIGNED
    |
    v
IMPLEMENTED
    |
    v
EXECUTED
    |
    v
OBSERVED
    |
    v
VERIFIED
```

An implementation status must not be interpreted as execution evidence.

---

## 15. Verification Status

The reported successful Phase-5 run supports local verification of the tested module behavior within the available test context. It does not establish that security tests were run against a real ECU, vehicle, production network or OEM environment. Test-double and local-artifact results must remain scoped to those environments.

Current verification status:

```text
CAN        = LOCAL MODULE TESTS REPORTED PASS; REAL TARGET NOT VERIFIED
UDS        = LOCAL MODULE TESTS REPORTED PASS; REAL TARGET NOT VERIFIED
Firmware   = LOCAL ARTIFACT TESTS REPORTED PASS; RUNTIME ECU BEHAVIOUR NOT VERIFIED
Ethernet   = SCANNER IMPLEMENTED; PYTEST VERIFICATION NOT ESTABLISHED
Bootloader / OTA = NOT ESTABLISHED
```

The project owner reports successful execution and generated evidence for Phase 5. No aggregate Phase-5 test report, total test count, or new run identifier is asserted here. Architecture implementation, local module tests and target-level security verification remain separate claims.

---

## 16. Domain-to-Architecture Traceability

The domain integration follows the common architecture:

```text
Assessment Objective
        |
        v
Security Objective / Property
        |
        v
Test Objective
        |
        v
Security Test Case
        |
        v
Test Runner
        |
        v
Domain Adapter
        |
        v
Domain Module
        |
        v
Target / Model
        |
        v
Execution
        |
        v
Observation
        |
        v
Result
```

Domain-specific mapping:

```text
CAN
    Test Case
        |
        v
    Test Runner
        |
        v
    CANAdapter
        |
        v
    CAN Module
        |
        v
    CAN Target / Virtual CAN

UDS
    Test Case
        |
        v
    Test Runner
        |
        v
    UDSAdapter
        |
        v
    UDS Module
        |
        v
    Diagnostic Target / Model

Firmware
    Test Case
        |
        v
    Test Runner
        |
        v
    FirmwareAdapter
        |
        v
    Firmware Module
        |
        v
    Firmware Artifact

Ethernet
    Test Case
        |
        v
    Test Runner
        |
        v
    EthernetAdapter
        |
        v
    Ethernet Module
        |
        v
    Network / Host Environment
```

This mapping keeps the common execution structure stable while allowing the technical implementation to remain domain-specific.

---

## 17. Current Domain Architecture Gap

The principal architectural gap before the common architecture integration was the missing common execution and adapter layer between the generic test structure and the existing domain implementations.

The architecture now provides:

```text
Test Case
    |
    v
Test Runner
    |
    v
Domain Adapter
    |
    v
Domain Module
    |
    v
Target / Model
```

The remaining gap is therefore primarily related to execution and verification status rather than the existence of the common domain-integration architecture.

The current state is:

```text
Common architecture integration
    = IMPLEMENTED

Concrete domain adapters
    = IMPLEMENTED for CAN / UDS / Firmware / Ethernet

Local Phase-5 module test execution
    = REPORTED PASS for covered CAN / UDS / Firmware tests

Real-target security verification
    = NOT ESTABLISHED

Ethernet pytest coverage
    = NOT ESTABLISHED

Security finding workflow
    = OUTSIDE THIS ARCHITECTURE DOCUMENT
```

---

## 18. Phase-5 Domain Test Status

Phase 5 covers the core security-test modules and their focused local tests. The project owner reports that the Phase-5 test run completed successfully and that evidence was created. The matrix therefore records local module-test completion separately from target-level security validation.

The repository snapshot supports the following distinctions:

| Domain | Test/implementation evidence in the snapshot | Status interpretation |
| --- | --- | --- |
| CAN | `b_security_tests/can_tests/test_can_sniffer.py` contains tests for normalization, filtered/unfiltered capture with test doubles, disconnected bus handling, duration validation, CSV export and statistics. | Local module tests reported passed; does not establish real CAN-bus or ECU validation. |
| UDS | `b_security_tests/uds_tests/test_uds_security.py` contains tests for request/response handling, response-ID matching, response classification, JSON export and bus closure, using a fake bus. | Local module tests reported passed; does not establish diagnostic validation against a real ECU. |
| Firmware | `b_security_tests/firmware_tests/test_firmware_validator.py` contains tests for SHA-256, binary data, metadata, digest comparisons, invalid digests, missing files and JSON export. | Local artifact tests reported passed; does not establish runtime firmware behavior on an ECU. |
| Ethernet | The snapshot contains scanner implementation in `b_security_tests/ethernet_tests/test_ethernet_scan.py`, but that file has no `test_*` pytest functions. | Scanner implementation exists; a passing Ethernet pytest suite is not established by this snapshot. |
| Bootloader / OTA | No concrete domain module or adapter established. | Not implemented / not run. |

The exact aggregate Phase-5 test count and a consolidated execution log are not specified here. Do not infer them from the individual test files. Any evidence files must be interpreted according to their recorded execution context and provenance.

Local test success is not equivalent to confirmed security findings, real-ECU validation, vehicle-level validation, production validation, regression validation or CI/CD validation.

---

## 19. Status Classification

The domain architecture uses the following status distinctions:

```text
DESIGNED
IMPLEMENTED
EXECUTED
OBSERVED
VERIFIED
```

These states describe different levels of technical maturity.

### DESIGNED

The architecture element is defined but no implementation is established.

### IMPLEMENTED

The corresponding technical implementation exists in the repository or is established by the documented implementation mapping.

### EXECUTED

The corresponding test or execution path has actually been run.

### OBSERVED

Execution produced an actual observation that can be evaluated.

### VERIFIED

The implementation or execution result has been verified according to the applicable verification criteria.

These states must not be collapsed into a single implementation status.

---

## 20. Result Semantics

The common result states are:

```text
PASS
FAIL
NOT_RUN
INCONCLUSIVE
BLOCKED
```

The result is derived from execution, observation and the defined evaluation criteria.

```text
Execution
    +
Observation
    +
Oracle / Evaluation Criteria
    =
Result
```

A test definition, expected behaviour or planned execution path does not itself establish a PASS or FAIL result.

A failed test result remains distinct from a confirmed security finding.

---

## 21. Evidence Boundary

The domain architecture establishes the boundary at which execution produces observations and results.

The subsequent evidence relationship is:

```text
Observation
        |
        v
Evidence
        |
        v
Result
```

The detailed Evidence Framework is maintained separately.

This document therefore does not define the complete evidence lifecycle.

---

## 22. Reporting Boundary

Reporting consumes information generated by the test architecture.

The relationship is:

```text
Test Execution
        |
        v
Observation
        |
        v
Result
        |
        v
Reporting
```

Reporting does not establish execution and does not create a result without an underlying execution state.

Existing finding-oriented reporting remains separate from test-result reporting.

---

## 23. Scope Integrity

The domain architecture remains limited to the security-test architecture and its current repository integration.

The following areas are not established by this document:

```text
Evidence Framework implementation
Security Finding Lifecycle
Root Cause Analysis
Regression Framework
CI/CD Automation
Professional Packaging
Production / OEM Validation
Real ECU Validation
Vehicle Validation
```

These areas remain separate engineering concerns.

The domain matrix therefore describes the technical architecture and implementation state without extending the current domain architecture into later workflow stages.

---

## 24. Final Classification

The current domain architecture can be classified as follows:

```text
COMMON SECURITY-TEST ARCHITECTURE
    = IMPLEMENTED

COMMON TEST CASE MODEL
    = IMPLEMENTED

TEST RUNNER
    = IMPLEMENTED

DOMAIN ADAPTER ARCHITECTURE
    = IMPLEMENTED

EXECUTION INTERFACE
    = IMPLEMENTED

TARGET / MODEL CONTEXT
    = IMPLEMENTED

OBSERVATION / RESULT STRUCTURES
    = IMPLEMENTED

ORACLE / EVALUATION BOUNDARY
    = DEFINED; END-TO-END RUNNER EVALUATION NOT ESTABLISHED

TRACEABILITY STRUCTURE
    = IMPLEMENTED

CAN DOMAIN
    = IMPLEMENTED

UDS DOMAIN
    = IMPLEMENTED

FIRMWARE DOMAIN
    = IMPLEMENTED

ETHERNET DOMAIN
    = IMPLEMENTED

BOOTLOADER / OTA
    = ARCHITECTURALLY SUPPORTED

LOCAL PHASE-5 MODULE TESTS
    = REPORTED PASS FOR COVERED CAN / UDS / FIRMWARE TESTS

ETHERNET PYTEST COVERAGE
    = NOT ESTABLISHED

REAL-TARGET DOMAIN EXECUTION
    = NOT ESTABLISHED

TARGET-LEVEL SECURITY VERIFICATION
    = NOT ESTABLISHED
```

The resulting architecture provides a common execution and integration structure for the concrete CAN, UDS, Firmware and Ethernet domains while preserving their domain-specific technical responsibilities.

The implementation status of the architecture is distinct from execution, observation and verification status. The domain architecture therefore establishes the technical integration structure without representing unverified domain execution as completed verification.

## Implementation Reference

Use this matrix for domain-level mapping and status. The concrete file-by-file framework mapping and the exact scope of the runner/adapter path are maintained in [`system_implementation_reference.md`](system_implementation_reference.md). A domain module or adapter being present does not establish a fully integrated test case, oracle/evaluation, evidence association, or end-to-end verification. In the available snapshot, the CAN, UDS and Firmware test files contain focused local tests; the Ethernet file named `test_ethernet_scan.py` contains scanner implementation but no `test_*` pytest functions. The project owner reports a successful Phase-5 test run, but no aggregate test count or consolidated Phase-5 execution log is asserted in this matrix.
