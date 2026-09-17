# Current State — ECU-Cyber-Integrity-Lab

## 1. Snapshot

| Item | Current state |
|---|---|
| Project | ECU-Cyber-Integrity-Lab |
| Current document | `docs/current_state.md` |
| Current phase | Phase 2 — ECU / Security Domain Model |
| Phase status | COMPLETED |
| Overall implementation | ESTABLISHED |
| Execution state | PARTIALLY OBSERVED / NOT VERIFIED AS COMPLETE |
| Evidence state |AVAILABLE / PARTIALLY CONSISTENT |
| Verification state | PARTIALLY ESTABLISHED |
| Documentation state | ESTABLISHED |
| Documentation completeness | PARTIAL |
| Regression | NOT IMPLEMENTED |
| CI/CD | NOT IMPLEMENTED / NOT VERIFIED |
| Traceability | PARTIAL |
| Quality level | Q2 |

This document describes the current technical state of the repository, including implementation, execution, evidence, verification, documentation, traceability and remaining work.

The state description distinguishes between functionality that exists in the repository, results that have been observed, evidence that is available, and functionality that remains planned. Planned work is not treated as implemented, and available artifacts are not treated as verified execution unless their provenance and execution context support that conclusion.

## 2. Quality Level

The project currently corresponds to quality level **Q2**.

| Level | Definition |
|---|---|
| Q0 | Initial or undefined project state |
| Q1 | Repository and project structure established |
| Q2 | Core implementation exists; execution and evidence are partially established |
| Q3 | Core functionality executed and technically verified |
| Q4 | Integrated security assessment and evidence workflow established |
| Q5 | Reproducible, regression-capable and continuously validated security assessment environment |

The Q2 classification reflects the current engineering state: the repository structure and core implementation are established, while complete execution verification, consistent evidence handling, integrated traceability, regression capability and CI/CD remain incomplete.

## 3. Project Context

### 3.1 Identity

ECU-Cyber-Integrity-Lab is an automotive cybersecurity engineering laboratory for structured White-Box security assessment activities.

The repository contains security-test implementations, framework components, test files, evidence, examples, reports and project documentation.

The current implementation covers selected CAN, UDS, Ethernet and firmware-related security-test capabilities. The repository also contains the technical basis for subsequent expansion toward a structured ECU and security-domain model.

### 3.2 Engineering Chain

The intended security-engineering relationship is:

```text
Asset
Security Property
Threat
Attack Surface
Attack Vector
Attacker Capability
Preconditions
Attack Path
Test Objective
Test Design
Execution
Observation
Evidence
Finding / Assessment
Impact
Risk
Mitigation
Retest / Verification
```

This chain defines the intended relationship between security requirements, assessment activities, execution results and subsequent verification.

Only parts of this chain are currently implemented. A complete implementation-to-test-to-evidence-to-finding lifecycle is not yet established.

### 3.3 Scope Classification

The current repository contains an implemented scope, a contextual automotive scope and planned future implementation areas.

#### Implemented scope

The existing security-test functionality covers selected areas of CAN, UDS, Ethernet and firmware assessment.

| Domain | Current implementation |
|---|---|
| CAN | Traffic capture, virtual CAN traffic generation, filtering, statistics, CSV export and fake CAN traffic generation |
| UDS | Basic UDS request/response handling and SecurityAccess classification |
| Ethernet | IP/network scanning, host discovery, service inventory and JSON export |
| Firmware | SHA-256 hashing, firmware comparison and JSON reporting |
| Framework | Base framework components, report generation and Python/pytest infrastructure |

#### Automotive context

The wider project context includes the following ECU, network and interface areas:

| Area | Scope |
|---|---|
| ECU architectures | Gateway ECU, BCM, Powertrain ECU, Infotainment ECU, TCU, ADAS Controller |
| Vehicle networks | CAN, CAN FD, Automotive Ethernet, LIN, FlexRay |
| Diagnostic and external interfaces | OBD-II, Bluetooth, USB, Wi-Fi, Cellular |
| Update and platform security | OTA, Secure Boot |

These areas define project context and scope; their presence in this section does not indicate complete implementation.

#### Planned and future implementation

The planned scope includes the ECU/security-domain model, a common security-test architecture, a unified evidence framework, extended test cases, evidence-backed findings and root-cause workflows, finding documentation, regression, CI/CD, packaging and final technical review.

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

| Classification | Meaning |
|---|---|
| REAL | Physical real-world system or ECU |
| VIRTUAL | Software-defined or virtualized environment |
| SIMULATED | Software-generated representation of system behavior |
| LOCAL | Execution on the local development environment |
| STATIC | Static artifact without live system interaction |
| SYNTHETIC | Artificially generated test data or traffic |

Current examples:

| Example | Classification |
|---|---|
| `vcan0` | VIRTUAL + LOCAL |
| Fake CAN traffic | SYNTHETIC + VIRTUAL + LOCAL |
| Local firmware artifact | LOCAL + STATIC |

These classifications describe the execution environment and artifact origin. They do not by themselves establish security validation against a real ECU or vehicle.

### 3.7 Real-World Validation Boundary

Validation against a physical ECU or vehicle requires an execution environment with a defined physical target, controlled test conditions, documented preconditions, reproducible execution information and evidence with sufficient provenance.

The current repository does not establish such a complete real-world validation chain.

## 4. Current Phase

| Item | State |
|---|---|
| Phase | Phase 2 — ECU / Security Domain Model |
| Status | COMPLETED |
| Completion gate | COMPLETED |
| Previous phase | Phase 1 — Repository Foundation |
| Next phase | Phase 3 — Security Test Architecture |

| Model state | Current state |
|---|---|
| ECU / component model | ESTABLISHED |
| Communication domain inventory | ESTABLISHED |
| Interface inventory | ESTABLISHED |
| Asset model | ESTABLISHED |
| Security property mapping | ESTABLISHED |
| Security-domain relationships | ESTABLISHED |
| Security-domain boundaries | DOCUMENTED WHERE ESTABLISHED |
| Assessment-surface mapping | DOCUMENTED WHERE ESTABLISHED |
| Model traceability | ESTABLISHED |
| Unresolved model elements | EXPLICITLY CLASSIFIED |

Concrete ECU instances, ECU-to-ECU topology, concrete vehicle communication paths, concrete Ethernet targets, service ownership and a complete project-wide security-property or attacker-capability model remain unresolved

## 5. Current Execution Position

The repository contains executable Python security-test code and a defined dependency baseline.

The technical environment is documented as follows:

| Component | Version / source |
|---|---|
| Python | 3.12.3 |
| pytest | 9.1.1 |
| Dependency baseline | `requirements.txt` |

The dependency baseline has been reviewed against `requirements.txt`.

Executable test files are present, but complete project-wide execution has not been established as a verified current execution state.

Available observations and artifacts provide partial execution information. They do not support a complete verification statement for the entire repository.

## 6. Actual Implementation State

### 6.1 Repository Structure

The current repository is organized into framework, security-test, evidence, example, report and documentation areas.

```text
01_framework/
02_security_tests/
03_evidence/
04_examples/
05_security_reports/
docs/
.gitignore
README.md
requirements.txt
```

The framework components are:

```text
01_framework/
├── __init__.py
├── base_test.py
├── config.py
├── logger.py
└── report_generator.py
```

The CAN security-test components are:

```text
02_security_tests/can/
├── __init__.py
├── can_sniffer.py
├── send_fake_can.py
└── test_can_sniffer.py
```

The Ethernet security-test components are:

```text
02_security_tests/ethernet/
├── __init__.py
├── ethernet_scan.py
└── test_ethernet_scan.py
```

The firmware security-test components are:

```text
02_security_tests/firmware/
├── __init__.py
├── firmware_validator.py
└── test_firmware_validator.py
```

The UDS security-test components are:

```text
02_security_tests/uds/
├── __init__.py
├── uds_security.py
└── test_uds_security.py
```

Example material is located in:

```text
04_examples/
├── firmware_review.md
├── risk_assessment.md
├── threat_model.md
└── uds_test.md
```

Security-report material is located in:

```text
05_security_reports/
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
├── project_definition_and_development_history.md
├── testing.md
```

### 6.2 Framework Components

`01_framework/base_test.py` provides a base framework component. The existing domain-specific test implementations do not currently establish a consistent inheritance relationship to this base class.

`01_framework/report_generator.py` expects the following report artifacts:

```text
can_capture.json
uds_report.json
ethernet_scan.json
firmware_report.json
```

The current CAN implementation exports CSV data rather than the expected `can_capture.json`. This represents an existing integration inconsistency between the CAN implementation and the report-generation component.

`config.py` and `logger.py` are present as framework components. A complete established implementation and integration of their intended functionality is not currently documented as verified.

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
02_security_tests/can/can_sniffer.py
```

This represents an existing import-path inconsistency.

| Aspect | Current state |
|---|---|
| Implementation | IMPLEMENTED |
| Test file | Present |
| Test execution | NOT VERIFIED |
| Security validation | NOT ESTABLISHED |
| Real ECU / vehicle validation | NOT ESTABLISHED |

### 7.2 UDS

The UDS implementation uses Python CAN and `vcan0` / SocketCAN for local diagnostic communication.

The current implementation defines:

| Element | Value |
|---|---|
| Request | `0x7E0` |
| Response | `0x7E8` |

The implemented service-related handling includes:

| Service | Function |
|---|---|
| `0x10 / 0x03` | Diagnostic Session Control |
| `0x27 / 0x01` | SecurityAccess |
| `0x22 / F190` | Read Data By Identifier |
| `0x11 / 0x01` | ECU Reset |

The implementation provides basic response classification and SecurityAccess classification.

A UDS test file exists, but no complete established test implementation is currently available.

| Aspect | Current state |
|---|---|
| Implementation | IMPLEMENTED |
| SecurityAccess classification | Basic |
| Test file | Present |
| Test execution | NOT VERIFIED |
| Security oracle | Partial |
| Security validation | NOT ESTABLISHED |
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

| Aspect | Current state |
|---|---|
| Implementation | IMPLEMENTED |
| Test file | Present / structural |
| Test execution | NOT VERIFIED |
| Security assessment | NOT ESTABLISHED |
| Production network validation | NOT ESTABLISHED |

### 7.4 Firmware

The firmware implementation provides SHA-256 hashing, expected-hash comparison, firmware A/B comparison and JSON reporting.

Referenced firmware artifacts include:

```text
gateway_ecu.bin
gateway_ecu_v2.bin
```

The firmware test file does not currently establish a complete pytest implementation.

| Aspect | Current state |
|---|---|
| Implementation | IMPLEMENTED|
| Test file | Present |
| Test execution | NOT VERIFIED |
| Integrity validation | NOT ESTABLISHED BEYOND AVAILABLE ARTIFACT RESULTS |

## 8. Test Execution State

### 8.1 Pytest

Pytest test files exist for CAN, UDS, Ethernet and firmware.

The complete project test suite has not been established as a verified execution result.

Known structural conditions are:

| Area | Current condition |
|---|---|
| CAN | Import-path mismatch present |
| UDS | Test implementation not established |
| Ethernet | Pytest implementation not established |
| Firmware | Test implementation not established |

Repository-wide pytest execution is therefore not a verified baseline.

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

| Field | Result |
|---|---|
| Result | FAIL |
| Expected SHA-256 | `0123456789abcdef` |
| Calculated SHA-256 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| A/B identical | `TRUE` |

A report dated 2026-07-25 documents:

| Field | Result |
|---|---|
| Result | PASS |
| A/B identical | `FALSE` |

The calculated hash in the 2026-08-22 report is consistent with an empty input. No root-cause conclusion is derived from this observation.

The differing reports represent different execution states or conditions and are not consolidated into one current verified firmware conclusion.

## 9. Observed Results

The currently available observations cover the following areas:

| Domain | Available observation |
|---|---|
| CAN | Existing capture / example artifacts |
| UDS | Conflicting historical and current artifacts |
| Ethernet | Example reports |
| Firmware | Conflicting execution reports |

These observations are not consolidated into a single verified project-wide security result.

No conclusion is drawn beyond the technical content and provenance supported by the respective artifacts.

## 10. Evidence State

### 10.1 Available Evidence

Evidence-related material is present in:

```text
03_evidence/
04_examples/
05_security_reports/
```

The repository therefore contains existing artifacts representing test outputs, examples and security-report material.

### 10.2 Evidence Classification

The intended evidence classification contains:

| Field | Purpose |
|---|---|
| Evidence ID | Evidence identification |
| Test ID | Association with a test |
| Domain | Technical assessment domain |
| Target | Assessed target |
| Environment | Execution environment |
| Preconditions | Conditions required for execution |
| Input | Test input |
| Expected Result | Expected behavior |
| Actual Result | Observed result |
| Observation | Recorded observation |
| Result | Result classification |
| Execution Status | Execution state |
| Timestamp | Execution timing |
| Artifacts | Associated artifacts |
| Tooling | Tools used |
| Command / Execution Method | Execution information |
| Notes | Additional information |
| Provenance | Origin and traceability information |

The current repository does not yet apply this classification consistently across all available artifacts.

### 10.3 Evidence Position

| Evidence aspect | Current state |
|---|---|
| Evidence available | YES |
| Evidence consistency | PARTIAL |
| Evidence provenance | PARTIAL / INSUFFICIENT FOR STRONG CLAIMS |
| Unified evidence lifecycle | NOT ESTABLISHED |
| Evidence sufficient for confirmed findings | NO |

An artifact documents an observation only to the extent that its origin, execution context and technical content support that observation.

## 11. Security State

### 11.1 Assets

The project context includes ECU and vehicle-related assets such as:

- Gateway ECU
- BCM
- Powertrain ECU
- Infotainment ECU
- TCU
- ADAS Controller
- Communication interfaces
- Diagnostic interfaces
- Firmware

A complete ECU/security-domain model is planned for a subsequent phase.

### 11.2 Security Properties

Relevant security properties include the protection and integrity of:

- Diagnostic functions
- Communication interfaces
- Firmware
- ECU functions
- Security-relevant services
- Network-accessible services

The current repository contains individual assessment implementations but does not yet provide a complete security-property model linked to all test activities.

### 11.3 Threats

A threat model exists in:

```text
04_examples/threat_model.md
```

The document is currently treated as example/project context until its elements are linked to defined security objectives, test objectives, execution and evidence.

### 11.4 Attack Surfaces

Current assessment-related attack surfaces include:

- CAN
- UDS diagnostics
- Automotive Ethernet / IP network interfaces
- Firmware artifacts

Additional automotive interfaces are part of the contextual and planned project scope.

### 11.5 Attacker Capabilities

The project uses a White-Box assessment context in which technical knowledge of relevant system behavior and implementation may be available.

Specific attacker capabilities are not yet represented by a complete unified attacker-capability model.

## 12. Findings State

No confirmed security finding is currently established from the available repository state.

Example material exists, but example material is not automatically treated as a confirmed project finding.

A finding requires a traceable chain:

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

| Document | Role |
|---|---|
| `README.md` | Project entry point / finalized project documentation |
| `docs/project_definition_and_development_history.md` | Project definition and historical development information |
| `docs/current_state.md` | Active current technical state |
| `docs/architecture_decisions.md` | Architecture decisions |
| `docs/testing.md` | Testing documentation |
| `docs/environment.md` | Environment documentation |
| `docs/White-Box-Ansatz.png` | White-Box approach illustration |

The documentation structure is established.

`docs/current_state.md` is an active and evolving document representing the current technical state.

Project history is maintained separately in:

```text
docs/project_definition_and_development_history.md
```

`PROJECT_STATUS.md` is not part of the defined project architecture.

## 15. Regression State

Regression capability is not currently implemented as a complete project function.

The intended regression architecture requires repeatable execution, defined test cases, comparable results, persistent evidence and verification of changes.

| Regression aspect | Current state |
|---|---|
| Architecture | Planned |
| Execution | NOT ESTABLISHED |
| Evidence | NOT ESTABLISHED |
| Verification | NOT ESTABLISHED |

Regression remains part of the planned project scope.

## 16. CI/CD State

The repository currently contains no `.github` directory.

| CI/CD aspect | Current state |
|---|---|
| CI/CD implementation | NOT IMPLEMENTED |
| Pipeline execution | NOT VERIFIED |
| Automated test pipeline | NOT ESTABLISHED |
| Automated evidence generation | NOT ESTABLISHED |

CI/CD remains part of the planned project scope.

## 17. Traceability State

The intended traceability chain is:

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

It does not represent complete implementation-to-test-to-evidence traceability.

| Traceability area | Current state |
|---|---|
| Requirements | PARTIAL |
| Security objectives | PARTIAL |
| Implementation mapping | PARTIAL |
| Test objectives | PARTIAL |
| Test execution | NOT VERIFIED |
| Evidence association | PARTIAL |
| Finding traceability | NOT ESTABLISHED FOR CONFIRMED FINDINGS |
| Mitigation / retest | NOT ESTABLISHED |
| Overall traceability | PARTIAL |

## 18. Quality Assessment

The current project quality level is **Q2**.

The assessment is based on the following state:

| Area | Assessment |
|---|---|
| Repository structure | ESTABLISHED |
| Core security-test implementations | PARTIALLY ESTABLISHED |
| Test infrastructure | PARTIALLY ESTABLISHED |
| Complete test execution | NOT VERIFIED |
| Evidence | AVAILABLE / PARTIALLY CONSISTENT |
| Confirmed security finding | NOT ESTABLISHED |
| Root-cause analysis | NOT ESTABLISHED FOR CONFIRMED FINDINGS |
| Regression | NOT IMPLEMENTED |
| CI/CD | NOT IMPLEMENTED |
| Documentation | ESTABLISHED / PARTIAL COMPLETENESS |
| Traceability | PARTIAL |

The Q2 classification reflects the current engineering state and does not represent a security maturity rating of an ECU, vehicle or production system.

## 19. Remaining Work

The remaining project work includes:

- Establish the ECU/security-domain model.
- Establish the common security-test architecture.
- Resolve existing implementation and integration inconsistencies.
- Establish executable pytest coverage.
- Establish reproducible test execution.
- Establish unified evidence handling.
- Establish complete execution-to-evidence traceability.
- Extend security-test coverage.
- Establish an evidence-backed finding workflow.
- Establish the root-cause analysis workflow.
- Establish mitigation and retest workflow.
- Establish regression capability.
- Establish CI/CD.
- Establish packaging.
- Perform the final technical review.

Additional planned security-test areas remain defined in the project scope and are not considered implemented until corresponding implementation, execution and verification are established.

## 20. Project History Reference

Historical project development, including the relationship between previous project phases and their completed activities, is maintained separately in:

```text
docs/project_definition_and_development_history.md
```

This document remains focused on the current technical truth state rather than duplicating the project history.

## Final Principle

The repository state is represented according to the distinction between implementation, execution, observation, evidence, verification and planned work.

An implemented component is not automatically a verified security result. An execution artifact is not automatically reproducible evidence. An example is not automatically a finding. Planned functionality is not treated as implemented functionality.

The current state therefore reflects the technically supported repository condition at the time of documentation.