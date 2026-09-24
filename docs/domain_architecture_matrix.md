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
| CAN              | `02_security_tests/can/can_sniffer.py`             | `02_security_tests/can/adapter.py::CANAdapter`           | CAN interface / virtual CAN                           | Capture, generation, filtering, statistics and CSV handling                   | IMPLEMENTED                         | NOT VERIFIED     | NOT ESTABLISHED     |
| UDS              | `02_security_tests/uds/uds_security.py`            | `02_security_tests/uds/adapter.py::UDSAdapter`           | Diagnostic target / simulated or local target context | UDS request / response interaction and SecurityAccess response classification | IMPLEMENTED                         | NOT VERIFIED     | NOT ESTABLISHED     |
| Firmware         | `02_security_tests/firmware/firmware_validator.py` | `02_security_tests/firmware/adapter.py::FirmwareAdapter` | Firmware artifact / local artifact                    | Firmware hashing, comparison and reporting                                    | IMPLEMENTED                         | NOT VERIFIED     | NOT ESTABLISHED     |
| Ethernet         | `02_security_tests/ethernet/ethernet_scan.py`      | `02_security_tests/ethernet/adapter.py::EthernetAdapter` | Network / host / service environment                  | Host discovery, IP/network scanning and service inventory                     | IMPLEMENTED                         | NOT VERIFIED     | NOT ESTABLISHED     |
| Bootloader / OTA | No concrete implementation established             | No concrete adapter established                          | Project-defined target / model                        | Architecturally supported security-testing domain                             | PLANNED / ARCHITECTURALLY SUPPORTED | NOT RUN          | NOT ESTABLISHED     |

The matrix separates the domain implementation from execution and verification status.

An implemented domain module or adapter establishes implementation of the corresponding architecture element. It does not by itself establish successful test execution or verification.

---

## 4. CAN Domain

### 4.1 Domain Role

The CAN domain provides security-testing capabilities for CAN communication and CAN traffic analysis.

The domain-specific implementation covers the technical processing of CAN traffic.

### 4.2 Domain Module

```text
02_security_tests/can/can_sniffer.py
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
02_security_tests/can/adapter.py::CANAdapter
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
Execution           = NOT VERIFIED
Verification        = NOT ESTABLISHED
```

---

## 5. UDS Domain

### 5.1 Domain Role

The UDS domain provides diagnostic communication and SecurityAccess-related security-testing capabilities.

### 5.2 Domain Module

```text
02_security_tests/uds/uds_security.py
```

The existing UDS implementation provides basic:

```text
UDS request / response interaction
SecurityAccess response classification
```

### 5.3 Domain Adapter

```text
02_security_tests/uds/adapter.py::UDSAdapter
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
Execution           = NOT VERIFIED
Verification        = NOT ESTABLISHED
```

---

## 6. Firmware Domain

### 6.1 Domain Role

The Firmware domain provides security-testing functionality for firmware artifacts.

### 6.2 Domain Module

```text
02_security_tests/firmware/firmware_validator.py
```

The firmware implementation provides:

```text
SHA-256 firmware hashing
Firmware comparison
Firmware JSON reporting
```

### 6.3 Domain Adapter

```text
02_security_tests/firmware/adapter.py::FirmwareAdapter
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
Execution           = NOT VERIFIED
Verification        = NOT ESTABLISHED
```

---

## 7. Ethernet Domain

### 7.1 Domain Role

The Ethernet domain provides network and service-discovery capabilities for security testing.

### 7.2 Domain Module

```text
02_security_tests/ethernet/ethernet_scan.py
```

The Ethernet implementation provides:

```text
Nmap-based IP / network scanning
Host discovery
Network service inventory
JSON export for Ethernet scan results
```

### 7.3 Domain Adapter

```text
02_security_tests/ethernet/adapter.py::EthernetAdapter
```

The `EthernetAdapter` provides the integration boundary between the common test architecture and Ethernet-specific network interaction.

Network-specific processing remains within the Ethernet domain.

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
Execution           = NOT VERIFIED
Verification        = NOT ESTABLISHED
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

WP-10 established the common architecture integration required to connect the existing security domains with the Security Test Architecture.

The implementation is structured around the smallest common architectural elements required for domain integration.

### 12.1 Common Test-Case Model

The common Test Case structure is represented by:

```text
01_framework/test_architecture.py::TestCase
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
01_framework/runner.py::TestRunner
```

The Test Runner provides the common execution lifecycle and separates execution orchestration from domain-specific protocol or target interaction.

Its responsibility includes:

```text
Test selection
Initialization
Precondition handling
Execution control
Lifecycle handling
Result collection
Execution status
Error / exception handling
Completion handling
```

Status:

```text
IMPLEMENTED
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

The common architecture provides an explicit oracle boundary.

The conceptual evaluation flow is:

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
IMPLEMENTED
```

---

### 12.8 Architecture Traceability

The common Test Case structure includes the objective relationship required for architecture-level traceability.

The traceability structure is represented by:

```text
01_framework/traceability.py::Traceability
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
01_framework/logging_boundary.py
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

The reporting layer supports test-result reporting through:

```text
ReportGenerator.add_test_result()
```

Test results are represented separately from existing finding/module reporting.

The existing reporting responsibilities remain preserved.

The reporting boundary therefore distinguishes:

```text
Test Result
Finding
Module Reporting
```

Reporting consumes results; it does not create a result merely because a report is generated.

Status:

```text
IMPLEMENTED
```

---

### 12.11 Domain Architecture Mapping

The concrete domain adapter mapping established for the architecture is:

| Domain           | Domain Module                                      | Adapter                | Target / Model Context         | Status                    |
| ---------------- | -------------------------------------------------- | ---------------------- | ------------------------------ | ------------------------- |
| CAN              | `02_security_tests/can/can_sniffer.py`             | `CANAdapter`           | CAN interface / virtual CAN    | IMPLEMENTED               |
| UDS              | `02_security_tests/uds/uds_security.py`            | `UDSAdapter`           | Diagnostic / simulated target  | IMPLEMENTED               |
| Firmware         | `02_security_tests/firmware/firmware_validator.py` | `FirmwareAdapter`      | Firmware artifact              | IMPLEMENTED               |
| Ethernet         | `02_security_tests/ethernet/ethernet_scan.py`      | `EthernetAdapter`      | Network / host environment     | IMPLEMENTED               |
| Bootloader / OTA | No concrete module established                     | No adapter established | Project-defined target / model | ARCHITECTURALLY SUPPORTED |

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

Reporting Boundary
        = IMPLEMENTED
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

The domain architecture matrix does not establish successful execution of the domain tests.

Current execution status:

```text
CAN        = NOT VERIFIED
UDS        = NOT VERIFIED
Firmware   = NOT VERIFIED
Ethernet   = NOT VERIFIED
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

The current domain architecture does not establish verified security-test execution.

Current verification status:

```text
CAN        = NOT ESTABLISHED
UDS        = NOT ESTABLISHED
Firmware   = NOT ESTABLISHED
Ethernet   = NOT ESTABLISHED
Bootloader / OTA = NOT ESTABLISHED
```

Verification requires actual execution and the corresponding observation/result information according to the project testing model.

The architecture definition and implementation mapping are separate from verification evidence.

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

Domain execution verification
    = NOT ESTABLISHED

Security finding workflow
    = OUTSIDE THIS ARCHITECTURE DOCUMENT
```

---

## 18. Status Classification

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

## 19. Result Semantics

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

## 20. Evidence Boundary

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

## 21. Reporting Boundary

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

## 22. Scope Integrity

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

## 23. Final Classification

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
    = IMPLEMENTED

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

DOMAIN EXECUTION
    = NOT VERIFIED

DOMAIN VERIFICATION
    = NOT ESTABLISHED
```

The resulting architecture provides a common execution and integration structure for the concrete CAN, UDS, Firmware and Ethernet domains while preserving their domain-specific technical responsibilities.

The implementation status of the architecture is distinct from execution, observation and verification status. The domain architecture therefore establishes the technical integration structure without representing unverified domain execution as completed verification.
