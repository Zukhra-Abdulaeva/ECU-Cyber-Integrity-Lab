# Current State — ECU-Cyber-Integrity-Lab

## 1. Snapshot

| Item                       | Current state                                   |
| -------------------------- | ----------------------------------------------- |
| Project                    | ECU-Cyber-Integrity-Lab                         |
| Current document           | `docs/current_state.md`                         |
| Current phase              | Phase 4 — Evidence Framework                    |
| Phase status               | COMPLETED                                       |
| Overall implementation     | ESTABLISHED                                     |
| Execution state            | PARTIALLY OBSERVED / NOT VERIFIED AS COMPLETE   |
| Evidence state             | FRAMEWORK ESTABLISHED / LEGACY EVIDENCE PARTIAL |
| Verification state         | FRAMEWORK VERIFIED / PROJECT PARTIAL            |
| Documentation state        | ESTABLISHED                                     |
| Documentation completeness | PARTIAL                                         |
| Regression                 | NOT IMPLEMENTED                                 |
| CI/CD                      | NOT IMPLEMENTED / NOT VERIFIED                  |
| Traceability               | EVIDENCE TRACEABILITY ESTABLISHED               |
| Quality level              | Q2                                              |

This document describes the current technical state of the repository, including implementation, execution, evidence, verification, documentation, traceability and remaining work.

The state description distinguishes between functionality that exists in the repository, results that have been observed, evidence that is available, and functionality that remains planned. Planned work is not treated as implemented, and available artifacts are not treated as verified execution unless their provenance and execution context support that conclusion.

## 2. Quality Level

The project currently corresponds to quality level **Q2**.

| Level | Definition                                                                                  |
| ----- | ------------------------------------------------------------------------------------------- |
| Q0    | Initial or undefined project state                                                          |
| Q1    | Repository and project structure established                                                |
| Q2    | Core implementation exists; execution and evidence are partially established                |
| Q3    | Core functionality executed and technically verified                                        |
| Q4    | Integrated security assessment and evidence workflow established                            |
| Q5    | Reproducible, regression-capable and continuously validated security assessment environment |

The Q2 classification reflects the current engineering state: the repository structure and core implementation are established, the Evidence Framework is implemented and locally verified, while complete execution verification of the security-test domains, complete project-wide evidence coverage, regression capability and CI/CD remain incomplete.

## 3. Project Context

### 3.1 Identity

ECU-Cyber-Integrity-Lab is an automotive cybersecurity engineering laboratory for structured White-Box security assessment activities.

The repository contains security-test implementations, framework components, test files, evidence, examples, reports and project documentation.

The current implementation covers selected CAN, UDS, Ethernet and firmware-related security-test capabilities. The repository also contains the technical basis for subsequent expansion toward a structured ECU and security-domain model.

### 3.2 Engineering Chain

The intended security-engineering relationship is:

```text
Assessment Objective
Security Objective / Property
Test Objective
Security Test Case
Test Runner
Domain Adapter
Domain Module
Target / Model
Observation
Result
Evidence
Finding / Assessment
Mitigation
Retest / Verification
```

This chain defines the current common security-test architecture and its relationship between assessment objectives, test objectives, execution responsibilities, observations, results and subsequent evidence and assessment activities.

The common security-test architecture is established. The Evidence Framework now provides the defined evidence-record, provenance, validation, association, lifecycle and integrity boundaries required for subsequent execution-linked evidence. Complete implementation-to-test-to-evidence-to-finding lifecycle integration is not yet established.

### 3.3 Scope Classification

The current repository contains an implemented scope, a contextual automotive scope and planned future implementation areas.

#### Implemented scope

The existing security-test functionality covers selected areas of CAN, UDS, Ethernet and firmware assessment.

| Domain    | Current implementation                                                                                             |
| --------- | ------------------------------------------------------------------------------------------------------------------ |
| CAN       | Traffic capture, virtual CAN traffic generation, filtering, statistics, CSV export and fake CAN traffic generation |
| UDS       | Basic UDS request/response handling and SecurityAccess classification                                              |
| Ethernet  | IP/network scanning, host discovery, service inventory and JSON export                                             |
| Firmware  | SHA-256 hashing, firmware comparison and JSON reporting                                                            |
| Framework | Base framework components, report generation, Python/pytest infrastructure and Evidence Framework                  |

#### Automotive context

The wider project context includes the following ECU, network and interface areas:

| Area                               | Scope                                                                    |
| ---------------------------------- | ------------------------------------------------------------------------ |
| ECU architectures                  | Gateway ECU, BCM, Powertrain ECU, Infotainment ECU, TCU, ADAS Controller |
| Vehicle networks                   | CAN, CAN FD, Automotive Ethernet, LIN, FlexRay                           |
| Diagnostic and external interfaces | OBD-II, Bluetooth, USB, Wi-Fi, Cellular                                  |
| Update and platform security       | OTA, Secure Boot                                                         |

These areas define project context and scope; their presence in this section does not indicate complete implementation.

#### Planned and future implementation

The planned scope includes extended test cases, evidence-backed findings and root-cause workflows, finding documentation, regression, CI/CD, packaging and final technical review.

The unified Evidence Framework is no longer classified as planned functionality. It has been implemented and locally verified in Phase 4. Legacy evidence remains subject to provenance and consistency limitations and is not retroactively treated as verified.

Additional future assessment areas include extended Automotive Ethernet, SOME/IP, extended OBD-II, Bluetooth, USB, Wi-Fi, Cellular, OTA, extended firmware security assessment, Secure Boot, additional test automation and integrated evidence/finding workflows.

These items remain planned until their corresponding implementation, execution and verification are established.

### 3.4 White-Box Approach

The project follows a White-Box assessment approach.

The assessment environment is intended to operate with knowledge of relevant implementation, architecture, interfaces and technical behavior. This supports detailed analysis of ECU functions, communication paths, diagnostic services, firmware and security mechanisms.

### 3.5 Simulation and Validation Boundary

The repository supports local, virtual and simulated assessment scenarios.

These scenarios provide a controlled environment for implementation development, functional testing and technical validation of individual components. They do not establish validation against a production ECU, production vehicle or production vehicle network.

### 3.6 Simulation Classification

The current simulation classifications are:

| Classification | Meaning                                              |
| -------------- | ---------------------------------------------------- |
| REAL           | Physical real-world system or ECU                    |
| VIRTUAL        | Software-defined or virtualized environment          |
| SIMULATED      | Software-generated representation of system behavior |
| LOCAL          | Execution on the local development environment       |
| STATIC         | Static artifact without live system interaction      |
| SYNTHETIC      | Artificially generated test data or traffic          |

Current examples:

| Example                 | Classification              |
| ----------------------- | --------------------------- |
| `vcan0`                 | VIRTUAL + LOCAL             |
| Fake CAN traffic        | SYNTHETIC + VIRTUAL + LOCAL |
| Local firmware artifact | LOCAL + STATIC              |

The Phase-4 Evidence Framework verification is classified as **LOCAL + SYNTHETIC**. These classifications describe the execution environment and artifact origin. They do not by themselves establish security validation against a real ECU or vehicle.

### 3.7 Real-World Validation Boundary

Validation against a physical ECU or vehicle requires an execution environment with a defined physical target, controlled test conditions, documented preconditions, reproducible execution information and evidence with sufficient provenance.

The current repository does not establish such a complete real-world validation chain.

## 4. Current Phase

| Item            | State                                |
| --------------- | ------------------------------------ |
| Phase           | Phase 4 — Evidence Framework         |
| Status          | COMPLETED                            |
| Completion gate | COMPLETED                            |
| Previous phase  | Phase 3 — Security Test Architecture |
| Next phase      | Phase 5 — Core Security Test Cases   |

| Architecture state              | Current state                            |
| ------------------------------- | ---------------------------------------- |
| Common Test Case Model          | NOT PRESENT                              |
| Test Runner                     | NOT PRESENT                              |
| Domain Adapter                  | NOT PRESENT                              |
| Execution Interface             | NOT PRESENT                              |
| Target / Model Context          | NOT PRESENT                              |
| Observation / Result Model      | NOT PRESENT                              |
| Oracle / Evaluation Boundary    | NOT PRESENT                              |
| Traceability                    | NOT PRESENT                              |
| Logging Boundary                | NOT PRESENT                              |
| Reporting Integration           | PARTIAL / REPORT COMPONENT PRESENT       |
| CAN Adapter                     | PRESENT / DEPENDENCY UNRESOLVED          |
| UDS Adapter                     | PRESENT / DEPENDENCY UNRESOLVED          |
| Firmware Adapter                | PRESENT / DEPENDENCY UNRESOLVED          |
| Ethernet Adapter                | PRESENT / DEPENDENCY UNRESOLVED          |
| General Security Test Execution | BLOCKED / NOT VERIFIED                   |
| Evidence Framework              | IMPLEMENTED / TARGETED VERIFICATION PASS |

The Phase-4 Evidence Framework is implemented and locally verified. Targeted verification executed the Evidence Framework verification tests with **10 passed**.

The Phase-4 verification establishes the functional behavior of the local Evidence Framework, including evidence identity, structure, provenance, lifecycle, validation, association, persistence, integrity handling and overwrite protection.

Concrete ECU instances, ECU-to-ECU topology, concrete vehicle communication paths, concrete Ethernet targets, service ownership and a complete project-wide security-property or attacker-capability model remain unresolved.

The supplied repository snapshot also does not contain the Phase-3 common architecture modules referenced by the historical/documented Phase-3 mapping. The corresponding claims remain unverified against the supplied implementation snapshot and are not used as proof of Phase-4 integration.

## 5. Current Execution Position

The repository contains executable Python security-test code and a defined dependency baseline.

The technical environment is documented as follows:

| Component           | Version / source   |
| ------------------- | ------------------ |
| Python              | 3.12.3             |
| pytest              | 9.1.1              |
| Dependency baseline | `requirements.txt` |

The dependency baseline has been reviewed against `requirements.txt`.

The targeted Phase-4 Evidence Framework verification has been executed locally:

```text
10 passed in 0.30s
```

The currently available local repository test baseline was additionally executed with:

```text
14 passed in 0.57s
```

The **10 passed** result is the authoritative targeted Phase-4 verification result. The **14 passed** result represents the broader currently available local repository test baseline.

Complete project-wide execution of all security-test domains has not been established as a verified current execution state.

Available observations and artifacts provide partial execution information. They do not support a complete verification statement for the entire repository.

## 6. Actual Implementation State

### 6.1 Repository Structure

The current repository is organized into framework, security-test, evidence, example, report and documentation areas.

```text
a_framework/
b_security_tests/
c_evidence/
d_examples/
e_security_reports/
docs/
.gitignore
README.md
requirements.txt
```

The framework components are:

```text
a_framework/
├── __init__.py
├── base_test.py
├── config.py
├── logger.py
├── logging_boundary.py
├── report_generator.py
├── runner.p
├── test_architecture.py
├── test_evidence.py
└── traceability.py
```

The CAN security-test components are:

```text
b_security_tests/can_tests/
├── __init__.py
├── adapter.py
├── can_sniffer.py
├── send_fake_can.py
└── test_can_sniffer.py
```

The Ethernet security-test components are:

```text
b_security_tests/ethernet_tests/
├── __init__.py
├── adapter.py
├── ethernet_scan.py
└── test_ethernet_scan.py
```

The firmware security-test components are:

```text
b_security_tests/firmware_tests/
├── __init__.py
├── adapter.py
├── firmware_validator.py
└── test_firmware_validator.py
```

The UDS security-test components are:

```text
b_security_tests/uds_tests/
├── __init__.py
├── adapter.py
├── uds_security.py
└── test_uds_security.py
```

Example material is located in:

```text
d_examples/
├── firmware_review.md
├── risk_assessment.md
├── threat_model.md
└── uds_test.md
```

Security-report material is located in:

```text
e_security_reports/
├── example_output_security_assessment.txt
├── security_assessment.json
├── security_report.html
└── security_report.md
```

The current documentation structure is:

```text
docs/
├── White-Box-Ansatz.png
├── architecture_decisions.md
├── current_state.md
├── environment.md
├── evidence.md
├── project_definition_and_development_history.md
├── testing.md
```

The evidence structure additionally contains:

```text
c_evidence/
├── records/
├── reports/
└── verification/
```

Phase-4 verification artifacts include:

```text
c_evidence/verification/
├── EV-P4-VER-001_test_execution.txt
├── EV-P4-VER-002_test_intent.txt
├── EV-P4-VER-003_test_framework.txt
└── EV-P4-VER-004_framework_test_execution.txt
```

Corresponding evidence records are stored under:

```text
c_evidence/reports/
├── EV-P4-VER-001.json
├── EV-P4-VER-002.json
├── EV-P4-VER-003.json
└── EV-P4-VER-004.json
```

### 6.2 Framework Components

`a_framework/base_test.py` provides a base framework component. The common Phase-3 test architecture is established separately through `test_architecture.py` and `runner.py`.

`a_framework/evidence.py` provides the Phase-4 Evidence Framework core, including canonical evidence records, stable evidence identifiers, provenance, context classification, validation, association and lifecycle handling.

`a_framework/report_generator.py` expects the following report artifacts:

```text
can_capture.json
uds_report.json
ethernet_scan.json
firmware_report.json
```

The current CAN implementation exports CSV data rather than the expected `can_capture.json`. This represents an existing integration inconsistency between the CAN implementation and the report-generation component.

The common test architecture provides explicit boundaries for Test Case, Test Runner, Domain Adapter, Execution Interface, Target / Model Context, Observation, Result, Oracle / Evaluation, Traceability and logging.

The Evidence Framework provides a structured boundary for Evidence Record, Provenance, Context Classification, Validation, Association, Lifecycle, Storage and Integrity.

`config.py` and `logger.py` remain framework support components. The common logging boundary is established through `logging_boundary.py`.

## 7. Security Test Components

### 7.1 CAN

The CAN implementation provides traffic capture, filtering, statistics and CSV export. It uses `vcan0` as the default virtual CAN interface and includes functionality for generating fake CAN traffic.

A CAN test file is present, but its execution is not established as verified.

The current test implementation contains the following import:

```text
from can_sniffer.can_sniffer import CANSniffer
```

The implementation itself is located at:

```text
b_security_tests/can_tests/can_sniffer.py
```

This represents an existing import-path inconsistency.

The CAN implementation is connected to the common Phase-3 execution architecture through the CAN domain adapter.

| Aspect                        | Current state   |
| ----------------------------- | --------------- |
| Implementation                | IMPLEMENTED     |
| Domain Adapter                | IMPLEMENTED     |
| Test file                     | Present         |
| Test execution                | NOT VERIFIED    |
| Security validation           | NOT ESTABLISHED |
| Real ECU / vehicle validation | NOT ESTABLISHED |

### 7.2 UDS

The UDS implementation uses Python CAN and `vcan0` / SocketCAN for local diagnostic communication.

The current implementation defines:

| Element  | Value   |
| -------- | ------- |
| Request  | `0x7E0` |
| Response | `0x7E8` |

The implemented service-related handling includes:

| Service       | Function                   |
| ------------- | -------------------------- |
| `0x10 / 0x03` | Diagnostic Session Control |
| `0x27 / 0x01` | SecurityAccess             |
| `0x22 / F190` | Read Data By Identifier    |
| `0x11 / 0x01` | ECU Reset                  |

The implementation provides basic response classification and SecurityAccess classification.

A UDS test file exists, but no complete established test implementation is currently available.

The UDS implementation is connected to the common Phase-3 execution architecture through the UDS domain adapter.

| Aspect                         | Current state   |
| ------------------------------ | --------------- |
| Implementation                 | IMPLEMENTED     |
| Domain Adapter                 | IMPLEMENTED     |
| SecurityAccess classification  | Basic           |
| Test file                      | Present         |
| Test execution                 | NOT VERIFIED    |
| Security oracle                | Partial         |
| Security validation            | NOT ESTABLISHED |
| Real ECU diagnostic validation | NOT ESTABLISHED |

### 7.3 Ethernet

The Ethernet implementation uses `python-nmap` for IP and network scanning.

Implemented functionality includes host discovery, service discovery, port scanning and JSON export.

The current implementation references the following ports:

```text
22
80
443
13400
30490
```

The Ethernet test file is currently a structural placeholder without an established pytest implementation.

Existing example output is treated as an artifact and not as independently verified current execution.

The Ethernet implementation is connected to the common Phase-3 execution architecture through the Ethernet domain adapter.

| Aspect                        | Current state        |
| ----------------------------- | -------------------- |
| Implementation                | IMPLEMENTED          |
| Domain Adapter                | IMPLEMENTED          |
| Test file                     | Present / structural |
| Test execution                | NOT VERIFIED         |
| Security assessment           | NOT ESTABLISHED      |
| Production network validation | NOT ESTABLISHED      |

### 7.4 Firmware

The firmware implementation provides SHA-256 hashing, expected-hash comparison, firmware A/B comparison and JSON reporting.

Referenced firmware artifacts include:

```text
gateway_ecu.bin
gateway_ecu_v2.bin
```

The firmware test file does not currently establish a complete pytest implementation.

The firmware implementation is connected to the common Phase-3 execution architecture through the firmware domain adapter.

| Aspect               | Current state                                     |
| -------------------- | ------------------------------------------------- |
| Implementation       | IMPLEMENTED                                       |
| Domain Adapter       | IMPLEMENTED                                       |
| Test file            | Present                                           |
| Test execution       | NOT VERIFIED                                      |
| Integrity validation | NOT ESTABLISHED BEYOND AVAILABLE ARTIFACT RESULTS |

## 8. Test Execution State

### 8.1 Pytest

Pytest test files exist for CAN, UDS, Ethernet and firmware.

The complete project test suite has not been established as a verified security-test execution result.

The Phase-3 architecture verification establishes the common test-architecture boundaries and their domain integration, while the Phase-4 verification establishes the functional behavior of the Evidence Framework.

Known structural conditions are:

| Area     | Current condition                     |
| -------- | ------------------------------------- |
| CAN      | Import-path mismatch present          |
| UDS      | Test implementation not established   |
| Ethernet | Pytest implementation not established |
| Firmware | Test implementation not established   |

The currently available local repository execution produced 14 passed tests, including the targeted Phase-4 framework verification. This does not establish complete project-wide security-test execution or security validation.

### 8.2 CAN Execution

The CAN implementation uses `vcan0` as its default virtual interface and supports fake traffic generation and capture.

Existing evidence includes differing interface conditions, including references to `can0`.

The available artifacts therefore represent observations under different execution conditions and do not provide a consistent verified basis for the current CAN environment.

### 8.3 UDS Execution

Existing UDS artifacts contain conflicting observations.

One current report documents no response, while another historical artifact documents a positive SecurityAccess-related result. Example output also contains a positive result.

The available provenance does not establish a single reproducible execution state for these observations.

Current UDS verification is therefore not established.

### 8.4 Ethernet Execution

Existing example reports document two discovered hosts and three services.

The execution environment, target and current reproducibility of these results are not independently established.

The reports therefore remain available execution artifacts rather than verified current security-assessment results.

### 8.5 Firmware Execution

Available firmware reports contain different execution states.

A report dated 2026-08-22 documents:

| Field              | Result                                                             |
| ------------------ | ------------------------------------------------------------------ |
| Result             | FAIL                                                               |
| Expected SHA-256   | `0123456789abcdef`                                                 |
| Calculated SHA-256 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| A/B identical      | `TRUE`                                                             |

A report dated 2026-07-25 documents:

| Field         | Result  |
| ------------- | ------- |
| Result        | PASS    |
| A/B identical | `FALSE` |

The calculated hash in the 2026-08-22 report is consistent with an empty input. No root-cause conclusion is derived from this observation.

The differing reports represent different execution states or conditions and are not consolidated into one current verified firmware conclusion.

## 9. Observed Results

The currently available observations cover the following areas:

| Domain   | Available observation                          |
| -------- | ---------------------------------------------- |
| CAN      | Existing capture / example artifacts           |
| UDS      | Conflicting historical and current artifacts   |
| Ethernet | Example reports                                |
| Firmware | Conflicting execution reports                  |
| Evidence | Phase-4 local framework verification artifacts |

These observations are not consolidated into a single verified project-wide security result.

The Phase-4 Evidence Framework verification establishes a verified result for the local Evidence Framework itself. It does not establish a verified security result for CAN, UDS, Ethernet, firmware, an ECU or a vehicle.

No conclusion is drawn beyond the technical content and provenance supported by the respective artifacts.

## 10. Evidence State

### 10.1 Available Evidence

Evidence-related material is present in:

```text
c_evidence/
d_examples/
e_security_reports/
```

The repository therefore contains existing artifacts representing test outputs, examples and security-report material.

Phase 4 additionally established structured evidence records and execution-verification artifacts under:

```text
c_evidence/records/
c_evidence/reports/
c_evidence/verification/
```

The current Phase-4 verification records include:

```text
EV-P4-VER-001.json
EV-P4-VER-002.json
EV-P4-VER-003.json
EV-P4-VER-004.json
```

with corresponding verification artifacts:

```text
EV-P4-VER-001_test_execution.txt
EV-P4-VER-002_test_intent.txt
EV-P4-VER-003_test_framework.txt
EV-P4-VER-004_framework_test_execution.txt
```

### 10.2 Evidence Classification

The Evidence Framework establishes the following canonical evidence classification:

| Field                      | Purpose                             |
| -------------------------- | ----------------------------------- |
| Evidence ID                | Evidence identification             |
| Test ID                    | Association with a test             |
| Domain                     | Technical assessment domain         |
| Target                     | Assessed target                     |
| Environment                | Execution environment               |
| Preconditions              | Conditions required for execution   |
| Input                      | Test input                          |
| Expected Result            | Expected behavior                   |
| Actual Result              | Observed result                     |
| Observation                | Recorded observation                |
| Result                     | Result classification               |
| Execution Status           | Execution state                     |
| Timestamp                  | Execution timing                    |
| Artifacts                  | Associated artifacts                |
| Tooling                    | Tools used                          |
| Command / Execution Method | Execution information               |
| Notes                      | Additional information              |
| Provenance                 | Origin and traceability information |

The Phase-4 implementation provides validation rules for these evidence properties and prevents invalid records from being persisted.

The classification is established for the Evidence Framework and its newly generated records. Legacy artifacts are not retroactively converted into verified evidence merely by the existence of the framework.

### 10.3 Evidence Position

| Evidence aspect                            | Current state                         |
| ------------------------------------------ | ------------------------------------- |
| Evidence available                         | YES                                   |
| Evidence consistency                       | FRAMEWORK CONSISTENT / LEGACY PARTIAL |
| Evidence provenance                        | FRAMEWORK DEFINED / LEGACY PARTIAL    |
| Unified evidence lifecycle                 | ESTABLISHED FOR FRAMEWORK             |
| Evidence sufficient for confirmed findings | NO                                    |

The Phase-4 Evidence Framework establishes canonical evidence records, stable identifiers, provenance, context classification, validation, association, lifecycle management, storage and integrity handling.

The framework was locally verified with:

```text
10 passed in 0.30s
```

The persisted Phase-4 execution artifact is:

```text
c_evidence/verification/EV-P4-VER-001_test_execution.txt
```

Its recorded SHA-256 integrity value is:

```text
be5c7c2a77651d7dbb2df36d92841b653019bc5a0572bffa08bd3c43016c9b08
```

The corresponding evidence record identifies the execution as:

```text
execution_status: EXECUTED
result: PASS
evidence_status: VERIFIED
```

The Phase-4 verification context is classified as:

```text
LOCAL
SYNTHETIC
```

An artifact documents an observation only to the extent that its origin, execution context and technical content support that observation.

## 11. Security State

### 11.1 Assets

The project context includes ECU and vehicle-related assets such as:

* Gateway ECU
* BCM
* Powertrain ECU
* Infotainment ECU
* TCU
* ADAS Controller
* Communication interfaces
* Diagnostic interfaces
* Firmware

A complete ECU/security-domain model is planned for a subsequent phase.

### 11.2 Security Properties

Relevant security properties include the protection and integrity of:

* Diagnostic functions
* Communication interfaces
* Firmware
* ECU functions
* Security-relevant services
* Network-accessible services

The current repository contains individual assessment implementations and now provides an Evidence Framework for structured evidence association, but does not yet provide a complete security-property model linked to all test activities.

### 11.3 Threats

A threat model exists in:

```text
d_examples/threat_model.md
```

The document is currently treated as example/project context until its elements are linked to defined security objectives, test objectives, execution and evidence.

### 11.4 Attack Surfaces

Current assessment-related attack surfaces include:

* CAN
* UDS diagnostics
* Automotive Ethernet / IP network interfaces
* Firmware artifacts

Additional automotive interfaces are part of the contextual and planned project scope.

### 11.5 Attacker Capabilities

The project uses a White-Box assessment context in which technical knowledge of relevant system behavior and implementation may be available.

Specific attacker capabilities are not yet represented by a complete unified attacker-capability model.

## 12. Findings State

No confirmed security finding is currently established from the available repository state.

Example material exists, but example material is not automatically treated as a confirmed project finding.

The Evidence Framework now provides the technical evidence foundation for a finding workflow, but a finding still requires a traceable chain:

```text
Security Property
Expected Behavior
Test Objective
Test Design
Execution
Observation
Evidence
Assessment
```

The current repository does not establish this complete chain for a confirmed finding.

## 13. Root Cause and Remediation State

No complete root-cause analysis is currently established for a confirmed security finding.

The repository does not yet provide a verified mitigation, retest and residual-risk workflow for a confirmed finding.

The intended lifecycle is:

```text
Finding
Root Cause
Mitigation
Retest
Verification
Residual Risk
```

## 14. Documentation State

The current documentation structure includes:

| Document                                             | Role                                                      |
| ---------------------------------------------------- | --------------------------------------------------------- |
| `README.md`                                          | Project entry point / finalized project documentation     |
| `docs/project_definition_and_development_history.md` | Project definition and historical development information |
| `docs/current_state.md`                              | Active current technical state                            |
| `docs/architecture_decisions.md`                     | Architecture decisions                                    |
| `docs/testing.md`                                    | Testing documentation                                     |
| `docs/environment.md`                                | Environment documentation                                 |
| `docs/White-Box-Ansatz.png`                          | White-Box approach illustration                           |

The documentation structure is established.

`docs/current_state.md` is an active and evolving document representing the current technical state.

Phase 4 additionally established or updated:

```text
docs/evidence.md
```

The document covers the Evidence Framework definition, evidence inventory, evidence gaps and traceability.

Project history is maintained separately in:

```text
docs/project_definition_and_development_history.md
```

`PROJECT_STATUS.md` is not part of the defined project architecture.

## 15. Regression State

Regression capability is not currently implemented as a complete project function.

The intended regression architecture requires repeatable execution, defined test cases, comparable results, persistent evidence and verification of changes.

| Regression aspect | Current state   |
| ----------------- | --------------- |
| Architecture      | Planned         |
| Execution         | NOT ESTABLISHED |
| Evidence          | NOT ESTABLISHED |
| Verification      | NOT ESTABLISHED |

The Evidence Framework provides a technical foundation for persistent evidence within a future regression workflow, but regression itself remains part of the planned project scope.

## 16. CI/CD State

The repository currently contains no `.github` directory.

| CI/CD aspect                  | Current state   |
| ----------------------------- | --------------- |
| CI/CD implementation          | NOT IMPLEMENTED |
| Pipeline execution            | NOT VERIFIED    |
| Automated test pipeline       | NOT ESTABLISHED |
| Automated evidence generation | NOT ESTABLISHED |

CI/CD remains part of the planned project scope.

## 17. Traceability State

The current common test-architecture traceability chain is:

```text
Security Requirement
Security Objective / Property
Security Design
Implementation
Test Objective
Test Design
Test Execution
Evidence
Result
Finding / Assessment
Mitigation
Retest
Verification
```

The Phase-0 project-definition work established the project-level traceability foundation:

```text
Project Definition
Security Engineering Goals / Security Domains
Scope and Assessment Boundaries
Assessment Methodology / Security Lifecycle
Truth-State and Test Result Model
Evidence Principle / Evidence Lifecycle
Subsequent Test and Assessment Activities
```

This foundation defines the intended relationship between project definition, assessment methodology, evidence and subsequent engineering activities.

Phase 4 establishes the technical Evidence Framework required to associate execution evidence with defined evidence records and to maintain provenance, validation, lifecycle and integrity information.

It does not represent complete implementation-to-test-to-evidence-to-finding traceability for the entire project.

| Traceability area      | Current state                                          |
| ---------------------- | ------------------------------------------------------ |
| Requirements           | PARTIAL                                                |
| Security objectives    | PARTIAL                                                |
| Implementation mapping | ESTABLISHED FOR COMMON TEST ARCHITECTURE               |
| Test objectives        | PARTIALLY ESTABLISHED                                  |
| Test execution         | NOT VERIFIED FOR COMPLETE PROJECT                      |
| Evidence association   | ESTABLISHED FOR EVIDENCE FRAMEWORK                     |
| Finding traceability   | NOT ESTABLISHED FOR CONFIRMED FINDINGS                 |
| Mitigation / retest    | NOT ESTABLISHED                                        |
| Overall traceability   | PARTIALLY ESTABLISHED / EVIDENCE FRAMEWORK ESTABLISHED |

## 18. Quality Assessment

The current project quality level is **Q2**.

The assessment is based on the following state:

| Area                               | Assessment                               |
| ---------------------------------- | ---------------------------------------- |
| Repository structure               | ESTABLISHED                              |
| Core security-test implementations | PARTIALLY ESTABLISHED                    |
| Test infrastructure                | ESTABLISHED FOR PHASE-3 ARCHITECTURE     |
| Complete test execution            | NOT VERIFIED                             |
| Evidence                           | FRAMEWORK VERIFIED / LEGACY PARTIAL      |
| Confirmed security finding         | NOT ESTABLISHED                          |
| Root-cause analysis                | NOT ESTABLISHED FOR CONFIRMED FINDINGS   |
| Regression                         | NOT IMPLEMENTED                          |
| CI/CD                              | NOT IMPLEMENTED                          |
| Documentation                      | ESTABLISHED / PARTIAL COMPLETENESS       |
| Traceability                       | PARTIAL / EVIDENCE FRAMEWORK ESTABLISHED |

The Q2 classification reflects the current engineering state and does not represent a security maturity rating of an ECU, vehicle or production system.

## 19. Remaining Work

The remaining project work includes:

* Resolve existing implementation and integration inconsistencies.
* Establish executable pytest coverage.
* Establish reproducible test execution.
* Extend security-test coverage.
* Establish an evidence-backed finding workflow.
* Establish the root-cause analysis workflow.
* Establish mitigation and retest workflow.
* Establish regression capability.
* Establish CI/CD.
* Establish packaging.
* Perform the final technical review.

Additional planned security-test areas remain defined in the project scope and are not considered implemented until corresponding implementation, execution and verification are established.

The Evidence Framework itself is no longer a remaining implementation task. Its Phase-4 implementation and targeted verification are completed.

## 20. Project History Reference

Historical project development, including the relationship between previous project phases and their completed activities, is maintained separately in:

```text
docs/project_definition_and_development_history.md
```

This document remains focused on the current technical truth state rather than duplicating the project history.

## Final Principle

The repository state is represented according to the distinction between implementation, execution, observation, evidence, verification and planned work.

An implemented component is not automatically a verified security result. An execution artifact is not automatically reproducible evidence. An example is not automatically a finding. Planned functionality is not treated as implemented functionality.

The Phase-4 Evidence Framework is implemented and locally verified, but its verification does not retroactively validate legacy evidence artifacts or establish security validation of an ECU, vehicle or production system.

The current state therefore reflects the technically supported repository condition at the time of documentation.
