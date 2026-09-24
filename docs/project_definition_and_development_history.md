# ECU-Cyber-Integrity-Lab

# Project Definition and Phase History

## 1. Project Identity

ECU-Cyber-Integrity-Lab is an automotive cybersecurity engineering laboratory for the structured investigation and assessment of ECU- and vehicle-related security aspects.

The project combines technical security testing, white-box analysis, security assessment, and technical documentation. The focus is on traceable investigation of selected security areas within a controlled laboratory environment.

The technical character of the project can be summarized as follows:

```text
Automotive Cybersecurity Engineering Laboratory
        |
        +-- White-Box Security Assessment
        |
        +-- ECU / Vehicle Security Concepts
        |
        +-- Technical Security Testing
        |
        +-- Evidence-Oriented Assessment
        |
        +-- Security Engineering Documentation
```

The laboratory evolves from individual technical security components and assessment artifacts toward a more integrated environment for Automotive Security Assessments.

The project identity describes the technical purpose and intended character of the laboratory. It is distinct from the current implementation or verification status of individual components.

---

## 2. Project Purpose

The purpose of ECU-Cyber-Integrity-Lab is to provide a structured engineering environment for the investigation and documentation of automotive cybersecurity aspects in ECU-oriented systems and connected vehicle architectures.

The laboratory supports the following security engineering activities in particular:

- System and architecture analysis
- Threat modeling
- White-box review of implementations
- CAN Security Assessment
- UDS Diagnostic Security Assessment
- Firmware Integrity and Security Review
- Automotive Ethernet Assessment
- Risk Assessment
- Security Reporting
- Technical security recommendations

The environment is intended to support selected security assessment activities in a traceable and reproducible manner within a controlled laboratory environment. Depending on the available target and execution environment, this includes the definition of Security Objectives, development of technical tests, execution of available test components, recording of observations, and structured storage of assessment artifacts.

The project purpose extends beyond the identification of individual vulnerabilities. Technical security tests are related to the underlying system, affected Security Properties, potential impacts, risk, and possible technical improvements.

The project therefore provides a technical basis for investigating how automotive security weaknesses can arise at architectural, implementation, and interface levels and how corresponding observations can be structured, documented, and assessed.

The project definition describes the engineering scope of the laboratory. It does not define the implementation, execution, or verification status of every listed activity.

---

## 3. Automotive Context

### 3.1 System Context

The project considers automotive systems containing multiple electronic control units, internal vehicle networks, diagnostic functions, and external communication interfaces.

Typical ECU categories considered in the technical context are:

- Gateway ECU
- Body Control Module (BCM)
- Powertrain ECU
- Infotainment ECU
- Telematics Control Unit (TCU)
- ADAS Controller

These categories provide technical context for security analyses and test cases. They do not imply the availability of a physical ECU for every category within the laboratory.

### 3.2 Automotive Network Technologies

The technical context includes in particular:

- CAN
- CAN FD
- Automotive Ethernet
- LIN
- FlexRay

The available technical implementation focuses on the security components actually present in the repository. Additional network technologies form part of the technical or planned scope where corresponding implementation and execution evidence is not yet established.

### 3.3 Diagnostic and External Interfaces

The automotive context includes, among others:

- UDS
- OBD-II
- Bluetooth
- USB
- Wi-Fi
- Cellular Connectivity
- OTA functions

These interfaces are considered security-relevant communication and attack-surface areas. Inclusion in the Automotive Context describes their technical relevance and does not establish that a corresponding security test has already been implemented or executed for each interface.

### 3.4 Automotive Security Areas

The technical security context includes in particular:

- Gateway and Trust Boundary concepts
- Diagnostic services
- Firmware Integrity and Firmware Security
- Secure Boot
- Network communication
- Remote Connectivity
- Threat Modeling
- Security Requirements
- Risk Assessment

These areas form the technical framework for the development and future extension of the security assessment.

---

## 4. Security Engineering Scope

The Security Engineering Scope combines system understanding, technical investigation, and structured assessment.

The investigation follows the following engineering relationship:

```text
SYSTEM / SECURITY CONTEXT

        |
        +--> Asset
        |
        +--> Security Property
        |
        +--> Threat
        |
        v

ATTACK MODEL

        |
        +--> Attack Surface
        |
        +--> Attack Vector
        |
        +--> Attacker Capability
        |
        +--> Preconditions
        |
        +--> Attack Path
        |
        v

SECURITY TEST DEFINITION

        |
        +--> Test Objective
        |
        +--> Test Preconditions
        |
        +--> Test Design
        |
        +--> Expected Result / Oracle
        |
        v

TEST EXECUTION

        |
        +--> Target / Environment
        |
        +--> Input / Action
        |
        +--> Execution
        |
        +--> Observation
        |
        v

EVIDENCE

        |
        +--> Logs / Captures
        +--> Reports
        +--> Output Artifacts
        +--> Execution Metadata
        |
        v

ASSESSMENT

        |
        +--> Result
        |
        +--> Finding
        |
        +--> Impact
        |
        +--> Risk
        |
        v

REMEDIATION & VERIFICATION

        |
        +--> Mitigation
        |
        +--> Retest
        |
        +--> Verification
        |
        +--> Residual Risk
```

The complete sequence is not required for every individual test case. It defines the technical relationship between the assessment objective, test, observation, evidence, and security assessment.

### 4.1 Security Properties

Security investigations address, depending on the respective objective, among others:

- Integrity
- Authenticity
- Confidentiality
- Availability
- Access Control
- Diagnostic Security
- Firmware Integrity
- Communication Security

The affected Security Property is determined from the specific test objective and available evidence.

### 4.2 White-Box Approach

The White-Box approach considers available technical information about implementation, configuration, interfaces, test logic, and assessment artifacts.

Compared with an exclusively external Black-Box test, this approach enables investigation of aspects such as:

- implementation of test functions,
- communication parameters used,
- intended security-relevant checks,
- data stored in assessment artifacts,
- processing of technical results.

The White-Box approach is based on technical information available within the project. It does not require access to proprietary OEM development environments or production systems.

---

## 5. Current Implementation Scope

The current implementation scope contains selected Python-based security and assessment components together with associated test structures, common security-test architecture components, examples, evidence artifacts, and documentation.

The described implementation scope includes:

- Python-based assessment components
- CAN Message Capture
- Virtual CAN Message Generation
- CAN Security Test Structure
- UDS Request/Response Handling
- UDS Security Test Structure
- Firmware SHA-256 Integrity Calculation
- Firmware Comparison
- Automotive Ethernet/IP Network Scanning with Nmap
- JSON-based Assessment Outputs
- Basic Report Generation
- Pytest Infrastructure
- Security Assessment Examples
- Existing Evidence Artifacts
- Technical Project Documentation

The current implementation scope is assessed separately from its execution and verification status. Source code, test structures, and common security-test architecture components provide implementation artifacts; execution and verification require corresponding technical evidence.

The detailed current Repository, Test, Execution, Evidence, and Verification situation is maintained separately in `docs/current_state.md`.

### 5.1 Component Implementation Matrix

<table style="width:100%; border-collapse:collapse;">
  <thead style="background-color:#f6f8fa;">
    <tr>
      <th>Existing Component</th>
      <th>Architecture Role</th>
      <th>Domain</th>
      <th>Current Implementation Status</th>
      <th>Relevant Limitation</th>
      <th>Required Architectural Relationship</th>
    </tr>
  </thead>
  <tbody>

<!-- 01_framework -->
<tr style="background-color:#ffffff;">
      <td><code>01_framework/base_test.py</code></td>
      <td>Common Test Framework Support</td>
      <td>Common</td>
      <td><b style="color:#22863a;">IMPLEMENTED</b></td>
      <td>Existing common test framework support<br>is retained within the common security-test architecture.</td>
      <td>Security Test Case → Test Runner</td>
    </tr>

<tr style="background-color:#f9f9f9;">
      <td><code>01_framework/logger.py</code></td>
      <td>Logging Support</td>
      <td>Common</td>
      <td><b style="color:#22863a;">IMPLEMENTED</b></td>
      <td>Common logging boundary is established<br>through the Phase‑3 architecture.</td>
      <td>Test Execution → Logging Boundary</td>
    </tr>

<tr style="background-color:#ffffff;">
      <td><code>01_framework/config.py</code></td>
      <td>Configuration Support</td>
      <td>Common</td>
      <td><b style="color:#d73a49;">NOT IMPLEMENTED AS COMMON ARCHITECTURE</b></td>
      <td>Configuration support exists as a repository component,<br>but no common execution configuration architecture is established.</td>
      <td>Test Runner / Execution Interface → Configuration</td>
    </tr>

<tr style="background-color:#f9f9f9;">
      <td><code>01_framework/report_generator.py</code></td>
      <td>Reporting Component</td>
      <td>Common</td>
      <td><b style="color:#22863a;">IMPLEMENTED</b></td>
      <td>Existing reporting is integrated with the common test-result architecture<br>while preserving existing finding and module reporting.</td>
      <td>Result → Reporting</td>
    </tr>

<!-- 02_security_tests domain modules -->
<tr style="background-color:#ffffff;">
      <td><code>02_security_tests/can/</code></td>
      <td>Domain Module</td>
      <td>CAN</td>
      <td><b style="color:#22863a;">IMPLEMENTED</b></td>
      <td>Domain-specific implementation is integrated<br>through the common CAN Domain Adapter architecture.</td>
      <td>Test Runner → CAN Domain Adapter → CAN Domain Module</td>
    </tr>

<tr style="background-color:#f9f9f9;">
      <td><code>02_security_tests/uds/</code></td>
      <td>Domain Module</td>
      <td>UDS</td>
      <td><b style="color:#22863a;">IMPLEMENTED</b></td>
      <td>Domain-specific implementation is integrated<br>through the common UDS Domain Adapter architecture.</td>
      <td>Test Runner → UDS Domain Adapter → UDS Domain Module</td>
    </tr>

<tr style="background-color:#ffffff;">
      <td><code>02_security_tests/firmware/</code></td>
      <td>Domain Module</td>
      <td>Firmware</td>
      <td><b style="color:#22863a;">IMPLEMENTED</b></td>
      <td>Domain-specific artifact analysis is integrated<br>through the common Firmware Domain Adapter architecture.</td>
      <td>Test Runner → Firmware Domain Adapter → Firmware Domain Module</td>
    </tr>

<tr style="background-color:#f9f9f9;">
      <td><code>02_security_tests/ethernet/</code></td>
      <td>Domain Module</td>
      <td>Automotive Ethernet</td>
      <td><b style="color:#22863a;">IMPLEMENTED</b></td>
      <td>Domain-specific network scanning is integrated<br>through the common Ethernet Domain Adapter architecture.</td>
      <td>Test Runner → Ethernet Domain Adapter → Ethernet Domain Module</td>
    </tr>

<!-- Existing domain test structures -->
<tr style="background-color:#ffffff;">
      <td><code>02_security_tests/can/test_can_sniffer.py</code></td>
      <td>Existing Domain Test Structure</td>
      <td>CAN</td>
      <td><b style="color:#fb8c00;">PARTIALLY IMPLEMENTED</b></td>
      <td>Existing test structure is domain-specific<br>and does not establish the common Phase‑3 Test Case model.</td>
      <td>Test Case → Test Runner → CAN Domain Module</td>
    </tr>

<tr style="background-color:#f9f9f9;">
      <td><code>02_security_tests/uds/test_uds_security.py</code></td>
      <td>Existing Domain Test Structure</td>
      <td>UDS</td>
      <td><b style="color:#fb8c00;">PARTIALLY IMPLEMENTED</b></td>
      <td>Existing test structure is domain-specific<br>and does not establish the common Phase‑3 Test Case model.</td>
      <td>Test Case → Test Runner → UDS Domain Module</td>
    </tr>

<tr style="background-color:#ffffff;">
      <td><code>02_security_tests/firmware/test_firmware_validator.py</code></td>
      <td>Existing Domain Test Structure</td>
      <td>Firmware</td>
      <td><b style="color:#fb8c00;">PARTIALLY IMPLEMENTED</b></td>
      <td>Existing test structure is domain-specific<br>and does not establish the common Phase‑3 Test Case model.</td>
      <td>Test Case → Test Runner → Firmware Domain Module</td>
    </tr>

<tr style="background-color:#f9f9f9;">
      <td><code>02_security_tests/ethernet/test_ethernet_scan.py</code></td>
      <td>Existing Domain Test Structure</td>
      <td>Automotive Ethernet</td>
      <td><b style="color:#fb8c00;">PARTIALLY IMPLEMENTED</b></td>
      <td>Existing test structure is domain-specific<br>and does not establish the common Phase‑3 Test Case model.</td>
      <td>Test Case → Test Runner → Ethernet Domain Module</td>
    </tr>

<!-- Evidence -->
<tr style="background-color:#ffffff;">
      <td><code>03_evidence/&lt;domain&gt;/</code></td>
      <td>Evidence Artifact Structure</td>
      <td>Domain-specific</td>
      <td><b style="color:#6a737d;">EXISTING STRUCTURE</b></td>
      <td>Existing artifacts do not establish<br>the Phase‑4 Evidence Framework.</td>
      <td>Execution / Observation → Evidence Boundary</td>
    </tr>

<!-- Reports -->
 <tr style="background-color:#f9f9f9;">
      <td><code>05_security_reports/</code></td>
      <td>Reporting Artifacts</td>
      <td>Common</td>
      <td><b style="color:#6a737d;">EXISTING STRUCTURE</b></td>
      <td>Existing reports do not establish<br>the common Phase‑3 result or reporting architecture.</td>
      <td>Result → Reporting</td>
    </tr>

  </tbody>
</table>

---

## 6. Target and Planned Scope

The intended engineering scope is extended incrementally. Planned components include:

- Structured Security Test Architecture
- Unified Domain Adapter and Execution Architecture
- Machine-Readable Evidence Framework
- Evidence Validation and Provenance
- Security Finding Lifecycle
- Root-Cause-Analysis Workflow
- Retest and Regression Validation
- Requirement-to-Evidence Traceability
- Extended CAN Security Tests
- Extended UDS Security Tests
- Extended Firmware Security Tests
- Extended Automotive Ethernet Tests
- CI/CD-Based Security Validation
- Integrated Assessment Reporting
- Professional Assessment Packaging

The following Automotive Security areas form part of the intended extension context:

- CAN FD Security Testing
- LIN Security Assessment
- FlexRay Security Assessment
- Further Automotive Ethernet protocols, including SOME/IP
- OBD-II Security Assessment
- Bluetooth Security Assessment
- USB Security Assessment
- Wi-Fi Security Assessment
- Cellular Security Assessment
- OTA Security Assessment
- Secure Boot Validation
- Extended Firmware Analysis
- Static Code Analysis Integration
- Extended Threat Modeling
- Further Test Automation

These components represent scope and planned extensions. Their inclusion in the project definition describes the intended engineering direction and does not establish existing implementation or execution evidence.

---

## 7. Scope Boundaries

### 7.1 Functional Scope Boundary

The project focuses on technical automotive cybersecurity investigations involving ECUs, vehicle networks, diagnostics, firmware, and connected interfaces.

The scope includes investigation of:

- Communication interfaces
- Diagnostic functions
- Firmware integrity
- Security-relevant implementation aspects
- Network and Trust Boundary concepts
- Security Requirements and Risk Assessment
- Technical Security Controls

### 7.2 Implementation Boundary

The project definition describes a comprehensive engineering scope, while the current repository contains only a subset of this scope.

The following states are therefore handled separately:

```text
PROJECT DEFINITION
    |
    +-- Engineering Scope
    |
    +-- Current Implementation
    |
    +-- Execution State
    |
    +-- Evidence State
    |
    +-- Verification State
    |
    +-- Planned Extensions
```

A technically defined function is classified as implemented when corresponding implementation artifacts are present in the repository.

An implemented function is classified as executed when actual execution is supported by evidence.

An executed test is classified as verified when the required expectations, observations, and evidence are available.

### 7.3 Target Boundary

The project is designed for controlled security assessment and engineering environments.

Depending on the test, the technical environment can include:

- Local Python execution
- Virtual network environments
- Virtual CAN interfaces
- Provided firmware artifacts
- Simulated or emulated communication partners
- Available network targets

The concrete target and environment situation is documented separately for executed tests.

### 7.4 Simulation Boundary

The project explicitly distinguishes the technical origin and execution context of an assessment activity.

The following classifications are used:

```text
REAL
    Physical real-world hardware, target system, or vehicle environment.

VIRTUAL
    A technically virtualized interface or environment that provides
    test functionality without representing a physical target system.

SIMULATED
    Behaviour, communication, or system conditions that are deliberately
    reproduced or emulated for testing.

LOCAL
    Execution or analysis performed on the local development or test system,
    including locally stored technical artifacts.

STATIC
    Analysis of an existing artifact without active interaction with a
    running target system.

SYNTHETIC
    Artificially generated test data or test input that does not originate
    from observed real vehicle traffic or another real-world source.
```

The classifications describe the origin or execution context of the respective activity. More than one classification can apply to the same artifact or test.

The current repository contains the following examples:

```text
vcan0
→ VIRTUAL

Fake-CAN messages
→ SYNTHETIC
→ when transmitted through vcan0, additionally VIRTUAL

Local firmware files
→ LOCAL
→ when analysed without a running target, additionally STATIC

Local JSON / CSV / TXT reports
→ LOCAL
→ they may contain execution results, but their presence alone does not
  establish a REAL target or a verified execution context
```

The following distinctions are mandatory:

```text
Virtual execution
≠
real ECU execution

Synthetic input
≠
observed vehicle traffic

Local firmware analysis
≠
production firmware validation
```

Virtual, simulated, local, static, and synthetic activities remain valid laboratory activities when their technical context is explicitly identified. Their results are interpreted according to that context.

A virtual or simulated execution can establish behaviour within the corresponding laboratory environment. It does not by itself establish behaviour of a physical ECU, production vehicle, OEM system, or production fleet.

### 7.5 Real-World Validation Boundary

A statement about a real ECU, real vehicle, or real vehicle environment requires evidence that the assessment was actually performed against the respective real target.

The minimum evidence basis for such a statement consists of the following chain:

```text
REAL TARGET
    ↓
HARDWARE
    ↓
REAL ENVIRONMENT
    ↓
EXECUTION
    ↓
OBSERVATION
    ↓
EVIDENCE
    ↓
PROVENANCE
    ↓
VALIDATION CONCLUSION
```

The required elements have the following meaning:

```text
REAL TARGET
    The actual ECU, vehicle, or vehicle environment being assessed
    is identified.

HARDWARE
    The physical hardware used for the assessment is identified.

REAL ENVIRONMENT
    The relevant physical or vehicle environment in which the test
    was performed is identified.

EXECUTION
    The security test or validation activity was actually executed
    against the real target.

OBSERVATION
    The execution produced an identifiable technical observation.

EVIDENCE
    Artifacts supporting the observation are available.

PROVENANCE
    The origin and context of the evidence can be established.

VALIDATION CONCLUSION
    The resulting conclusion is limited to the real target and
    environment actually supported by the evidence.
```

Without corresponding hardware, environment, execution, observation, evidence, and provenance, no real ECU or real vehicle validation is claimed.

In particular:

```text
Virtual CAN
≠
real vehicle CAN

Local firmware file
≠
production firmware

Synthetic CAN traffic
≠
observed vehicle traffic

Local test execution
≠
real ECU execution
```

The current project evidence does not establish real ECU or production-vehicle validation.

### 7.6 Production and OEM Boundary

Statements concerning production systems, OEM environments, or vehicle fleets require corresponding evidence from those environments.

The presence of automotive terminology, ECU models, protocol implementations, simulation environments, or example artifacts does not establish production or OEM validation.

The project therefore distinguishes between:

```text
Laboratory Assessment
        |
        +-- Local
        +-- Virtual
        +-- Simulated
        +-- Static
        +-- Synthetic

Real-World Assessment
        |
        +-- Physical Hardware
        +-- Real Environment
        +-- Actual Execution
        +-- Observation
        +-- Evidence
        +-- Provenance
```

The scope of any real-world conclusion remains limited to the target and environment supported by the corresponding evidence.

---

## 8. Non-Scope

The current project status focuses on technical assessment statements supported by the available technical evidence.

The following activities require additional validation and are therefore outside the established project evidence scope:

- General security approval for production vehicles
- OEM production approval
- Certification evidence
- Complete vehicle homologation
- Productive fleet validation
- General security statements about a specific vehicle model without corresponding evidence
- Confirmed vulnerabilities without reproducible technical evidence

The project can produce technical assessment results and provides an engineering basis for security investigation. Production-related approval, certification, and homologation processes remain separate activities.

---

## 9. Assessment Methodology

The Security Assessment Methodology defines how a security assessment is planned, executed, evaluated, and verified within the laboratory.

The methodology consists of five connected activities:

1. SECURITY ANALYSIS
   System Understanding
   Asset Identification
   Security Property Definition
   Threat Analysis
   Attack Surface Analysis
   Attack Path Definition

2. TEST ENGINEERING
   Test Objective
   Test Preconditions
   Test Design
   Expected Result / Oracle

3. CONTROLLED EXECUTION
   Target and Environment
   Test Input / Action
   Test Execution
   Observation

4. EVIDENCE AND ASSESSMENT
   Evidence Preservation
   Result Evaluation
   Security Assessment
   Finding
   Impact
   Risk

5. REMEDIATION AND VERIFICATION
   Mitigation
   Retest
   Verification
   Residual Risk

```text
SYSTEM / SECURITY ANALYSIS
        |
        v
TEST ENGINEERING
        |
        v
CONTROLLED EXECUTION
        |
        v
EVIDENCE AND ASSESSMENT
        |
        v
REMEDIATION AND VERIFICATION
        |
        +----------------------+
        |                      |
        |              Retest / Verification
        |                      |
        +----------<-----------+
```

---

## 10. Security Engineering Goals

The project pursues the following engineering goals:

### 10.1 Reproducibility

Technical security investigations should be repeatable under comparable conditions.

### 10.2 Traceability

Security statements should be connected to their technical foundations wherever possible:

```text
1. SECURITY REQUIREMENT
   |
   +-- Requirement
   |     What must be fulfilled or protected?
   |
   +-- Security Objective / Property
         Which security property is relevant?
   |
   v
2. SECURITY DESIGN
   |
   +-- Design
   |     How should the security property be implemented technically?
   |
   +-- Implementation
         How was this solution actually implemented?
   |
   v
3. SECURITY TEST
   |
   +-- Test Objective
   |     What is to be tested or demonstrated?
   |
   +-- Test Design
   |     How is the assessment performed?
   |
   +-- Test Execution
         What was actually executed?
   |
   v
4. SECURITY EVIDENCE AND ASSESSMENT
   |
   +-- Evidence
   |     Which artifacts support the observation?
   |
   +-- Result
   |     What was actually determined?
   |
   +-- Finding / Assessment
         What security assessment follows from the result?
   |
   v
5. REMEDIATION AND VERIFICATION
   |
   +-- Mitigation
   |     Which measure addresses the result?
   |
   +-- Retest
   |     Was the change tested again?
   |
   +-- Verification
         Is the effectiveness of the measure demonstrated?
```

Missing relationships are identified explicitly.

### 10.3 Evidence-Oriented Assessment

Technical statements should be based on traceable observations and associated artifacts.

Depending on the test, suitable evidence information can include:

- Evidence ID
- Test ID
- Domain
- Target
- Environment
- Preconditions
- Input
- Expected Result
- Actual Result
- Observation
- Result
- Execution Status
- Timestamp
- Artifacts
- Tooling
- Command or Execution Method
- Notes
- Provenance

### 10.4 Controlled Security Findings

A Security Finding is assessed according to the available technical basis. A theoretical possibility alone does not establish a confirmed finding.

A confirmed finding requires a traceable relationship between expectation, test or verification activity, actual execution, observation, and supporting evidence.

Where this basis is not established, the respective situation is classified using an appropriate status such as:

- ATTACK HYPOTHESIS
- POTENTIAL FINDING
- PROPOSED
- UNVERIFIED
- INCONCLUSIVE
- BLOCKED

---

## 11. Security Domains

The project's Security Engineering context includes the following domains in particular:

### 11.1 CAN Security

Focus areas:

- CAN Message Capture
- Message Filtering
- Controlled Message Generation
- Communication Analysis
- Security-Relevant CAN Test Cases

### 11.2 UDS Diagnostic Security

Focus areas:

- Diagnostic Session
- Security Access
- Diagnostic Requests
- Response Handling
- Security-Relevant Diagnostic Tests

### 11.3 Firmware Security

Focus areas:

- Firmware Integrity
- SHA-256-Based Integrity Verification
- Firmware Comparison
- Firmware Security Review

### 11.4 Automotive Ethernet Security

Focus areas:

- IP Network Discovery
- Port Scanning
- Service Identification
- Security-Relevant Network Observation

### 11.5 Threat Modeling and Risk Assessment

Focus areas:

- Assets
- Security Properties
- Threats
- Attack Surfaces
- Attack Vectors
- Attacker Capabilities
- Impact
- Risk
- Mitigations

The concrete technical coverage of each domain depends on the available implementation and verification status.

---

## 12. Truth-State Model

Project information is classified according to its actual technical and evidentiary status. The status of an artifact or statement is determined by what has actually been designed, implemented, executed, observed, and verified.

The primary truth states are:

```text
PLANNED
  |
  | The functionality or activity is defined as intended scope.
  v
DESIGNED
  |
  | The technical approach or test concept has been specified.
  v
IMPLEMENTED
  |
  | The corresponding implementation exists in the repository.
  |
  +------------------------------+
  |                              |
  | not executed                 | executed
  v                              v
IMPLEMENTED                   EXECUTED
                                  |
                                  | An actual execution took place.
                                  v
                               OBSERVED
                                  |
                                  | The execution produced an identifiable
                                  | observation or result.
                                  v
                               VERIFIED
                                  |
                                  | The observation and supporting evidence
                                  | satisfy the applicable verification
                                  | criteria.
                                  v
                           VERIFIED STATE

DOCUMENTED is treated separately:

DOCUMENTED
    |
    +-- The corresponding project state, result, or evidence
        has been recorded in the appropriate documentation.
```

These states represent distinct technical conditions.

The following distinctions apply:

```text
DESIGNED      != IMPLEMENTED

IMPLEMENTED   != EXECUTED

EXECUTED      != OBSERVED

OBSERVED      != VERIFIED

DOCUMENTED    != IMPLEMENTED

DOCUMENTED    != VERIFIED

EXPECTED      != OBSERVED

SIMULATED     != REAL

TEST EXISTS   != TEST PASSED

CI CONFIGURED != CI VERIFIED
```

```text
TECHNICAL STATE

    PLANNED
    DESIGNED
    IMPLEMENTED

EXECUTION STATE

    NOT_RUN
    EXECUTED

OBSERVATION STATE

    NO_OBSERVATION
    OBSERVED

VERIFICATION STATE

    UNVERIFIED
    VERIFIED

DOCUMENTATION STATE

    UNDOCUMENTED
    DOCUMENTED
```

---

## 13. Test Result Model

Technical security tests use the following result states:

```text
PASS

FAIL

NOT_RUN

INCONCLUSIVE

BLOCKED
```

`PASS` requires:

- Actual test execution
- A defined and fulfilled test oracle or expectation
- Traceable observation
- Supporting evidence

An existing test case or result file provides a test artifact and requires corresponding execution evidence for classification as a successful test.

---

## 14. Evidence Lifecycle

Evidence is managed as a traceable record of a specific test execution, observation, or other technically relevant assessment result.

The lifecycle distinguishes the creation and validation of evidence from its association with assessment objects and its later archival status.

```text
                         +----------------+
                         |    CREATED     |
                         | Evidence has   |
                         | been captured  |
                         +-------+--------+
                                 |
                                 v
                         +----------------+
                         |   VALIDATED    |
                         | Structure,     |
                         | provenance and |
                         | content checked|
                         +-------+--------+
                                 |
                                 v
                         +----------------+
                         |   ASSOCIATED   |
                         | Linked to the  |
                         | relevant test, |
                         | result or      |
                         | finding        |
                         +-------+--------+
                                 |
                                 v
                         +----------------+
                         |    ACTIVE      |
                         | Current evidence|
                         | used by the    |
                         | assessment     |
                         +-------+--------+
                                 |
                    +------------+------------+
                    |                         |
                    | replaced by newer      |
                    | evidence                |
                    v                         |
             +----------------+               |
             |   SUPERSEDED   |               |
             | Retained for   |               |
             | traceability   |               |
             +-------+--------+               |
                     |                        |
                     +-----------+------------+
                                 |
                                 v
                         +----------------+
                         |    ARCHIVED    |
                         | Retained as    |
                         | historical     |
                         | project record |
                         +----------------+
```

Existing evidence is preserved as a distinct artifact. Changes or subsequent executions are assigned to new evidence or an updated status so that their history remains traceable.

```text
CREATED

    Evidence artifact has been generated or captured.

VALIDATED

    Basic integrity, provenance, structure, and contextual consistency
    have been checked.

ASSOCIATED

    The evidence has been linked to the corresponding test, execution,
    result, finding, or other assessment object.

ACTIVE

    The evidence is currently the applicable evidence for the associated
    assessment context.

SUPERSEDED

    A newer evidence artifact has replaced this artifact as the applicable
    evidence, while the original remains available for traceability.

ARCHIVED

    The evidence is retained as historical project information and is no
    longer part of the active assessment state.
```

The significance of an artifact depends on its origin, target, environment, execution method, timestamp, and association with the respective test.

---

## 15. Project Development Model

The project is developed incrementally through defined engineering phases.

Each phase has a defined purpose, expected outputs, and a completion gate.

The phase model provides the development structure.

The planned engineering phases are:

```text
+--------------------------------------------------------------+
| PHASE 0                                                     |
| Project Definition                                          |
|                                                              |
| Project identity, purpose, scope, boundaries, and methodology|
+-------------------------------+------------------------------+
                                |
                                v
+--------------------------------------------------------------+
| PHASE 1                                                     |
| Repository Foundation                                       |
+-------------------------------+------------------------------+
                                |
                                v
+--------------------------------------------------------------+
| PHASE 2                                                     |
| ECU / Security Domain Model                                  |
+-------------------------------+------------------------------+
                                |
                                v
+--------------------------------------------------------------+
| PHASE 3                                                     |
| Security Test Architecture                                   |
+-------------------------------+------------------------------+
                                |
                                v
+--------------------------------------------------------------+
| PHASE 4                                                     |
| Evidence Framework                                           |
+-------------------------------+------------------------------+
                                |
                                v
+--------------------------------------------------------------+
| PHASE 5                                                     |
| Core Security Test Cases                                     |
+-------------------------------+------------------------------+
                                |
                                v
+--------------------------------------------------------------+
| PHASE 6                                                     |
| Extended Security Test Cases                                 |
+-------------------------------+------------------------------+
                                |
                                v
+--------------------------------------------------------------+
| PHASE 7                                                     |
| Findings / Root Cause Analysis                               |
+-------------------------------+------------------------------+
                                |
                                v
+--------------------------------------------------------------+
| PHASE 8                                                     |
| Finding Documentation                                        |
+-------------------------------+------------------------------+
                                |
                                v
+--------------------------------------------------------------+
| PHASE 9                                                     |
| Regression Validation                                        |
+-------------------------------+------------------------------+
                                |
                                v
+--------------------------------------------------------------+
| PHASE 10                                                    |
| CI/CD                                                        |
+-------------------------------+------------------------------+
                                |
                                v
+--------------------------------------------------------------+
| PHASE 11                                                    |
| Professional Packaging                                       |
+-------------------------------+------------------------------+
                                |
                                v
+--------------------------------------------------------------+
| PHASE 12                                                    |
| Final Technical Review / Portfolio Integration               |
+--------------------------------------------------------------+
```

A phase is considered complete when its respective Completion Gate and documented technical results have been fulfilled.

```text
Phase Definition
       |
       v
Phase Work
       |
       v
Implementation / Documentation
       |
       v
Testing / Execution
       |
       v
Evidence and Review
       |
       v
Completion Gate
       |
       +---- NOT COMPLETE ----> Remaining Work / Blocker
       |
       +---- COMPLETE --------> Phase Status Recorded
                                      |
                                      v
                               Next Phase Allowed
```

---

## 16. Phase Structure

The project development is structured into the following phases:

```text
Phase 0  - Project Definition

Phase 1  - Repository Foundation

Phase 2  - ECU / Security Domain Model

Phase 3  - Security Test Architecture

Phase 4  - Evidence Framework

Phase 5  - Core Security Test Cases

Phase 6  - Extended Security Test Cases

Phase 7  - Findings / RCA

Phase 8  - Finding Documentation

Phase 9  - Regression Validation

Phase 10 - CI/CD

Phase 11 - Professional Packaging

Phase 12 - Final Technical Review / Portfolio Integration
```

The phases describe the intended development and working framework.

---

## 17. Phase History

### 17.1 Project Origin and Technical Foundation

The project was initially established through technical security tools, test structures, assessment examples, and result artifacts.

Early technical focus areas include:

- CAN Security Testing
- UDS Security Testing
- Firmware Validation
- Automotive Ethernet Scanning
- Basic Assessment Reports
- Technical Security Examples
- Evidence Artifacts

The later project structure formalizes these technical components into a consistent Automotive Cybersecurity Engineering Laboratory.

### 17.2 Formalization of Project Definition

During further project development, the project definition was formalized as a dedicated engineering component.

The following questions were separated in particular:

- What is ECU-Cyber-Integrity-Lab?
- What purpose does the project serve?
- Which Automotive Security areas form part of the technical context?
- What is currently implemented?
- What belongs to the planned scope?
- Which boundaries apply to simulation and real-world validation?
- How are tests, evidence, findings, and verification distinguished?

This separation keeps the technical target scope distinct from the current implementation status.

### 17.3 Documentation Structure Decision

The documentation structure was organized so that the project definition, current state, and technical architecture decisions serve distinct purposes.

The intended documentation roles are:

```text
README.md

    = Entry point and compact project overview

docs/project_definition_and_development_history.md

    = Project definition, scope, boundaries, and historical development

docs/current_state.md

    = Actual current repository, implementation, execution,
      evidence, and verification state

docs/architecture_decisions.md

    = Rationale for major technical architecture decisions

docs/testing.md

    = Execution and assessment of available tests
```

The detailed project definition is therefore kept separate from the current execution state.

### 17.4 Current Phase Context

This file defines the technical identity, purpose, intended scope, technical boundaries, and development history of the project.

The current repository, implementation, execution, evidence, and verification state are maintained separately. `docs/current_state.md` is authoritative for that information.

`docs/current_state.md` includes in particular:

- Repository structure
- Existing implementations
- Test status
- Execution Status
- Evidence Status
- Verification Status
- Known technical inconsistencies
- Blockers
- Traceability
- Remaining work for the current phase

This separation keeps the stable project definition distinct from the changing technical state of the repository.

### 17.5 Completion Results

The project is developed through defined engineering phases. Each phase has a specific engineering objective and produces a defined result when its completion criteria have been fulfilled.

The phase history records the actual development of the project. A phase is only recorded as completed when its implementation, applicable testing, evidence, review, and Completion Gate have been fulfilled and the result has been documented.

The phase history therefore distinguishes between:

```text
PLANNED

    Phase is defined in the project development model.

IN PROGRESS

    Phase work is actively being performed.

COMPLETED

    Phase Completion Gate has been fulfilled and the resulting state
    has been documented.

BLOCKED

    Phase completion is prevented by an identified blocker.

NOT STARTED

    Phase is defined but no phase work has been established.
```

---

## 18. Historical Project Principles

During project development, the following principles were established as the technical framework:

### 18.1 Separation of Definition and Reality

The project definition describes the engineering scope. Repository and execution documentation describe the technically established project state.

### 18.2 Evidence Before Confirmation

A technical security statement is presented as confirmed when the required supporting evidence is available.

### 18.3 Explicit Uncertainty

Technical matters with incomplete or insufficient evidence are explicitly classified as UNKNOWN, UNVERIFIED, ASSUMPTION, INCONCLUSIVE, or BLOCKED where the respective status applies.

### 18.4 Simulation Transparency

Simulated, virtual, or locally emulated test environments are clearly distinguished from real ECU or vehicle tests.

### 18.5 No Status Inflation

Documentation, implementation, execution, and verification are assessed separately. A higher status is established through its own supporting evidence.

---

## 19. Project Definition Summary

The project definition can be summarized as follows:

```text
PROJECT IDENTITY

    Automotive Cybersecurity Engineering Laboratory

PROJECT PURPOSE

    Structured examination and documentation of automotive
    cybersecurity aspects in ECU-oriented systems and
    connected vehicle architectures

CURRENT IMPLEMENTATION

    Selected Python-based security tools, common security-test
    architecture components, test structures, documentation,
    and assessment artifacts

CURRENT VERIFICATION

    Not established; assessed separately from implementation

TARGET / PLANNED SCOPE

    Integrated, evidence-oriented Automotive Security
    Assessment Environment

SIMULATION

    Permitted within explicitly controlled and documented
    laboratory boundaries

REAL ECU / VEHICLE VALIDATION

    Established only where corresponding target, hardware,
    environment, execution, observation, evidence, and provenance
    are available

PRODUCTION / OEM VALIDATION

    Established only where corresponding project evidence exists

CONFIRMED SECURITY FINDINGS

    Require execution, observation and supporting evidence
```

---

## 20. Phase 0 - Project Definition

**Objective**

Define the identity, purpose, technical scope, boundaries, methodology, and development framework of ECU-Cyber-Integrity-Lab.

**Phase Work**

During Phase 0, the project definition and its technical boundaries were established and documented. The work included:

- formalizing the project identity, purpose and automotive security context
- defining the Security Engineering Scope and separating current implementation, contextual scope and planned scope
- defining the White-Box assessment perspective and its information boundary
- defining the Non-Scope and the distinction between laboratory assessment and real-world automotive validation
- defining the Simulation Boundary and the REAL, VIRTUAL, SIMULATED, LOCAL, STATIC and SYNTHETIC classifications
- defining the Assessment Methodology, Security Engineering Goals and Security Domains
- establishing the Security Lifecycle and project-level traceability basis
- documenting the Truth-State Model, Test Result Model and Evidence Lifecycle
- defining the Project Development Model and phase structure
- establishing the documentation roles and the separation between stable project definition, phase history and the evolving current repository state
- reviewing documentation consistency and synchronizing the resulting Phase-0 state

**Phase Result**

- The project definition establishes:
- Project Identity
- Project Purpose
- Automotive Context
- Security Engineering Scope
- Current Implementation Scope
- Target and Planned Scope
- Scope Boundaries
- Simulation Boundary
- Real-World Validation Boundary
- Non-Scope
- Assessment Methodology
- Security Engineering Goals
- Assessment Traceability
- Truth-State Model
- Test Result Model
- Evidence Lifecycle
- Project Development Model

The project definition and phase history are maintained in this document.

The current repository and execution state are maintained separately in docs/current_state.md.

**Status: COMPLETED**

The Phase-0 Completion Gate has been fulfilled and the resulting project state has been reviewed and documented. Phase 0 is therefore recorded as completed.

## 20.1 Phase 1 - Repository Foundation

**Objective**

Establish the repository foundation required for the structured development and maintenance of the security assessment environment.

**Phase Work**

Phase 1 reviewed and established the repository foundation within the defined project scope.

The completed Phase-1 activities included:

- reviewing the repository structure and organization
- reviewing the project configuration and dependency definition
- establishing the technical development-environment baseline
- reviewing and documenting the documentation structure
- reviewing repository-to-documentation consistency
- correcting the identified documentation filename inconsistency
- preserving the existing implementation without introducing unnecessary later-phase changes
- synchronizing the current project state with the reviewed Phase-1 status
- reviewing the defined Phase-1 verification criteria
- documenting open technical issues and verification limitations
- completing the Phase-1 review
- performing the Phase-1 Completion Gate

The Phase-1 technical baseline established the following environment information:

```text
Python
→ 3.12.3

pytest
→ 9.1.1

Project Dependencies
→ VERIFIED AGAINST requirements.txt

Git Branch
→ main
```

The dependency verification confirms the declared project dependencies against the active development environment. It does not establish successful execution of the complete project test suite.

**Phase Result**

The Phase-1 repository foundation was established and reviewed.

The following completion conditions were satisfied:

```text
Repository Foundation
→ ESTABLISHED

Structure
→ REVIEWED AND CONSISTENT

Project Configuration
→ REVIEWED AND BASELINED

Documentation Structure
→ ESTABLISHED AND DOCUMENTED

Repository/Documentation Consistency
→ REVIEWED

Technical Baseline
→ ESTABLISHED

Current State
→ SYNCHRONIZED

Phase-1 Artifacts
→ COMPLETE

Verification Criteria
→ REVIEWED

Open Issues
→ DOCUMENTED

Blocking Issues
→ NONE IDENTIFIED

Phase-1 Review
→ COMPLETED
```

The Phase-1 Completion Gate was completed and documented in:

```text
docs/phase_1_completion_gate_review.md
```

The Phase-1 review record is maintained separately as:

```text
docs/phase_1_review_record.md
```

Phase 1 established the repository foundation and its associated documentation and baseline records. Project-wide test execution, complete security verification, regression validation, CI/CD implementation, and real ECU / vehicle validation remain separate technical states.

These states are therefore not part of the Phase-1 completion result.

**Status: COMPLETED**

## 20.2 Phase 2 - ECU / Security Domain Model

Objective

Define the ECU-oriented security domain model and establish the relationships between relevant ECU types, communication domains, interfaces, assets, and security properties.

Expected Phase Result:

A consistent ECU and Security Domain Model is established and connected to the technical assessment scope.

The completed work included:

- establishing the ECU-oriented model
- documenting relevant communication domains
- documenting relevant interfaces
- establishing the scoped asset model
- mapping applicable security properties
- establishing security-domain relationships
- documenting relevant security-domain boundaries
- connecting established assessment surfaces to the model
- establishing model-level traceability
- explicitly classifying unresolved model elements
- preserving the separation between model, implementation,
  execution, evidence and verification

Phase Result: 

The defined Phase-2 model scope is established. 
Remaining information gaps are explicitly classified. 
Completion does not imply physical ECU validation, security-control verification, execution evidence or confirmed security findings.

The resulting model is maintained in:

ecu_security_domain_model.md

The model does not establish security-test execution, security findings, evidence generation or security-control verification.

**Status: COMPLETED**

## 20.3 Phase 3 - Security Test Architecture

Objective
        |
        v
Expected Phase Result
        |
        v
Repository Architecture Mapping
        |
        v
Status

**Objective :** Establish the technical architecture for structured security testing across the supported security domains.

**Expected Phase Result :** A consistent Security Test Architecture defines test organization, domain separation, reusable test structures, execution interfaces, and the relationship between tests and assessment objectives.

**Repository Architecture Mapping**

The Phase-3 repository mapping establishes the relationship between existing repository components and the defined Security Test Architecture.

The mapping reflects the repository structure reviewed during Phase 3 and distinguishes existing implementation from architectural responsibilities that are defined but not yet implemented.

| Existing Component | Architecture Role | Domain | Current Implementation Status | Relevant Limitation | Required Architectural Relationship |
|---|---|---|---|---|---|
| `01_framework/base_test.py` | Common Test Framework Support | Common | IMPLEMENTED | Existing common test framework support is retained within the common security-test architecture. | Security Test Case → Test Runner |
| `01_framework/logger.py` | Logging Support | Common | IMPLEMENTED | Common logging boundary is established through the Phase-3 architecture. | Test Execution → Logging Boundary |
| `01_framework/config.py` | Configuration Support | Common | NOT IMPLEMENTED AS COMMON ARCHITECTURE | Configuration support exists as a repository component, but no common execution configuration architecture is established. | Test Runner / Execution Interface → Configuration |
| `01_framework/report_generator.py` | Reporting Component | Common | IMPLEMENTED | Existing reporting is integrated with the common test-result architecture while preserving existing finding and module reporting. | Result → Reporting |
| `02_security_tests/can/` | Domain Module | CAN | IMPLEMENTED | Domain-specific implementation is integrated through the common CAN Domain Adapter architecture. | Test Runner → CAN Domain Adapter → CAN Domain Module |
| `02_security_tests/uds/` | Domain Module | UDS | IMPLEMENTED | Domain-specific implementation is integrated through the common UDS Domain Adapter architecture. | Test Runner → UDS Domain Adapter → UDS Domain Module |
| `02_security_tests/firmware/` | Domain Module | Firmware | IMPLEMENTED | Domain-specific artifact analysis is integrated through the common Firmware Domain Adapter architecture. | Test Runner → Firmware Domain Adapter → Firmware Domain Module |
| `02_security_tests/ethernet/` | Domain Module | Automotive Ethernet | IMPLEMENTED | Domain-specific network scanning is integrated through the common Ethernet Domain Adapter architecture. | Test Runner → Ethernet Domain Adapter → Ethernet Domain Module |
| `02_security_tests/can/test_can_sniffer.py` | Existing Domain Test Structure | CAN | PARTIALLY IMPLEMENTED | Existing test structure is domain-specific and does not establish the common Phase-3 Test Case model. | Test Case → Test Runner → CAN Domain Module |
| `02_security_tests/uds/test_uds_security.py` | Existing Domain Test Structure | UDS | PARTIALLY IMPLEMENTED | Existing test structure is domain-specific and does not establish the common Phase-3 Test Case model. | Test Case → Test Runner → UDS Domain Module |
| `02_security_tests/firmware/test_firmware_validator.py` | Existing Domain Test Structure | Firmware | PARTIALLY IMPLEMENTED | Existing test structure is domain-specific and does not establish the common Phase-3 Test Case model. | Test Case → Test Runner → Firmware Domain Module |
| `02_security_tests/ethernet/test_ethernet_scan.py` | Existing Domain Test Structure | Automotive Ethernet | PARTIALLY IMPLEMENTED | Existing test structure is domain-specific and does not establish the common Phase-3 Test Case model. | Test Case → Test Runner → Ethernet Domain Module |
| `03_evidence/<domain>/` | Evidence Artifact Structure | Domain-specific | EXISTING STRUCTURE | Existing artifacts do not establish the Phase-4 Evidence Framework. | Execution / Observation → Evidence Boundary |
| `05_security_reports/` | Reporting Artifacts | Common | EXISTING STRUCTURE | Existing reports do not establish the common Phase-3 result or reporting architecture. | Result → Reporting |

<table style="width:100%; border-collapse:collapse;">
  <thead style="background-color:#f6f8fa;">
    <tr>
      <th>Existing Component</th>
      <th>Architecture Role</th>
      <th>Domain</th>
      <th>Current Implementation Status</th>
      <th>Relevant Limitation</th>
      <th>Required Architectural Relationship</th>
    </tr>
  </thead>
  <tbody>

<tr style="background-color:#ffffff;">
      <td><code>01_framework/base_test.py</code></td>
      <td>Common Test Framework Support</td>
      <td>Common</td>
      <td><b style="color:#22863a;">IMPLEMENTED</b></td>
      <td>Existing common test framework support<br>is retained within the common security-test architecture.</td>
      <td>Security Test Case → Test Runner</td>
    </tr>

<tr style="background-color:#f9f9f9;">
      <td><code>01_framework/logger.py</code></td>
      <td>Logging Support</td>
      <td>Common</td>
      <td><b style="color:#22863a;">IMPLEMENTED</b></td>
      <td>Common logging boundary is established<br>through the Phase‑3 architecture.</td>
      <td>Test Execution → Logging Boundary</td>
    </tr>

<tr style="background-color:#ffffff;">
      <td><code>01_framework/config.py</code></td>
      <td>Configuration Support</td>
      <td>Common</td>
      <td><b style="color:#d73a49;">NOT IMPLEMENTED AS COMMON ARCHITECTURE</b></td>
      <td>Configuration support exists as a repository component,<br>but no common execution configuration architecture is established.</td>
      <td>Test Runner / Execution Interface → Configuration</td>
    </tr>

<tr style="background-color:#f9f9f9;">
      <td><code>01_framework/report_generator.py</code></td>
      <td>Reporting Component</td>
      <td>Common</td>
      <td><b style="color:#22863a;">IMPLEMENTED</b></td>
      <td>Existing reporting is integrated with the common test-result architecture<br>while preserving existing finding and module reporting.</td>
      <td>Result → Reporting</td>
    </tr>

<tr style="background-color:#ffffff;">
      <td><code>02_security_tests/can/</code></td>
      <td>Domain Module</td>
      <td>CAN</td>
      <td><b style="color:#22863a;">IMPLEMENTED</b></td>
      <td>Domain-specific implementation is integrated<br>through the common CAN Domain Adapter architecture.</td>
      <td>Test Runner → CAN Domain Adapter → CAN Domain Module</td>
    </tr>

<tr style="background-color:#f9f9f9;">
      <td><code>02_security_tests/uds/</code></td>
      <td>Domain Module</td>
      <td>UDS</td>
      <td><b style="color:#22863a;">IMPLEMENTED</b></td>
      <td>Domain-specific implementation is integrated<br>through the common UDS Domain Adapter architecture.</td>
      <td>Test Runner → UDS Domain Adapter → UDS Domain Module</td>
    </tr>

<tr style="background-color:#ffffff;">
      <td><code>02_security_tests/firmware/</code></td>
      <td>Domain Module</td>
      <td>Firmware</td>
      <td><b style="color:#22863a;">IMPLEMENTED</b></td>
      <td>Domain-specific artifact analysis is integrated<br>through the common Firmware Domain Adapter architecture.</td>
      <td>Test Runner → Firmware Domain Adapter → Firmware Domain Module</td>
    </tr>

<tr style="background-color:#f9f9f9;">
      <td><code>02_security_tests/ethernet/</code></td>
      <td>Domain Module</td>
      <td>Automotive Ethernet</td>
      <td><b style="color:#22863a;">IMPLEMENTED</b></td>
      <td>Domain-specific network scanning is integrated<br>through the common Ethernet Domain Adapter architecture.</td>
      <td>Test Runner → Ethernet Domain Adapter → Ethernet Domain Module</td>
    </tr>

<tr style="background-color:#ffffff;">
      <td><code>02_security_tests/can/test_can_sniffer.py</code></td>
      <td>Existing Domain Test Structure</td>
      <td>CAN</td>
      <td><b style="color:#fb8c00;">PARTIALLY IMPLEMENTED</b></td>
      <td>Existing test structure is domain-specific<br>and does not establish the common Phase‑3 Test Case model.</td>
      <td>Test Case → Test Runner → CAN Domain Module</td>
    </tr>

<tr style="background-color:#f9f9f9;">
      <td><code>02_security_tests/uds/test_uds_security.py</code></td>
      <td>Existing Domain Test Structure</td>
      <td>UDS</td>
      <td><b style="color:#fb8c00;">PARTIALLY IMPLEMENTED</b></td>
      <td>Existing test structure is domain-specific<br>and does not establish the common Phase‑3 Test Case model.</td>
      <td>Test Case → Test Runner → UDS Domain Module</td>
    </tr>

<tr style="background-color:#ffffff;">
      <td><code>02_security_tests/firmware/test_firmware_validator.py</code></td>
      <td>Existing Domain Test Structure</td>
      <td>Firmware</td>
      <td><b style="color:#fb8c00;">PARTIALLY IMPLEMENTED</b></td>
      <td>Existing test structure is domain-specific<br>and does not establish the common Phase‑3 Test Case model.</td>
      <td>Test Case → Test Runner → Firmware Domain Module</td>
    </tr>

<tr style="background-color:#f9f9f9;">
      <td><code>02_security_tests/ethernet/test_ethernet_scan.py</code></td>
      <td>Existing Domain Test Structure</td>
      <td>Automotive Ethernet</td>
      <td><b style="color:#fb8c00;">PARTIALLY IMPLEMENTED</b></td>
      <td>Existing test structure is domain-specific<br>and does not establish the common Phase‑3 Test Case model.</td>
      <td>Test Case → Test Runner → Ethernet Domain Module</td>
    </tr>

<tr style="background-color:#ffffff;">
      <td><code>03_evidence/&lt;domain&gt;/</code></td>
      <td>Evidence Artifact Structure</td>
      <td>Domain-specific</td>
      <td><b style="color:#6a737d;">EXISTING STRUCTURE</b></td>
      <td>Existing artifacts do not establish<br>the Phase‑4 Evidence Framework.</td>
      <td>Execution / Observation → Evidence Boundary</td>
    </tr>

<tr style="background-color:#f9f9f9;">
      <td><code>05_security_reports/</code></td>
      <td>Reporting Artifacts</td>
      <td>Common</td>
      <td><b style="color:#6a737d;">EXISTING STRUCTURE</b></td>
      <td>Existing reports do not establish<br>the common Phase‑3 result or reporting architecture.</td>
      <td>Result → Reporting</td>
    </tr>

  </tbody>
</table>

Architecture DELTA Implementation
- Identified architecture deviations D1–D11.
- Implemented the technically necessary architecture corrections.
- Preserved existing domain-specific functionality.
- Added common architecture boundaries where required.
- Verification performed after implementation.

Result:
- Phase-3 architecture implementation advanced from the previously
  documented state to the current implementation state.

Reference:
- security_test_architecture_definition.md
- architecture_decisions.md
- current_state.md
- domain_architecture_matrix.md

The Phase-3 architecture implementation establishes the common Test Case, Test Runner, Domain Adapter, Execution Interface, Target / Model,
Observation / Result, Oracle / Evaluation, Traceability, Logging, and Reporting boundaries required for the defined Security Test Architecture.

The supported domain architecture is integrated through concrete adapters for CAN, UDS, Firmware, and Automotive Ethernet. Domain-specific security
functionality remains within the respective domain modules.

The Phase-3 implementation establishes architectural and implementation support. It does not establish successful execution of security test cases,
confirmed security findings, Evidence Framework completion, regression validation, or CI/CD validation.

**Status: COMPLETED**

```text
Security Test Architecture

        |

        +-- Architecture Definition
        |       → ESTABLISHED
        |
        +-- Common Test Architecture
        |       → IMPLEMENTED
        |
        +-- Test Runner
        |       → IMPLEMENTED
        |
        +-- Domain Adapters
        |       → IMPLEMENTED
        |
        +-- Execution Interface
        |       → IMPLEMENTED
        |
        +-- Target / Model Boundary
        |       → IMPLEMENTED
        |
        +-- Observation / Result
        |       → IMPLEMENTED
        |
        +-- Oracle / Evaluation
        |       → IMPLEMENTED
        |
        +-- Traceability
        |       → IMPLEMENTED
        |
        +-- CAN / UDS / Firmware / Ethernet Integration
        |       → IMPLEMENTED
        |
        +-- Security Test Execution
        |       → NOT ESTABLISHED AS GENERAL PROJECT STATE
        |
        +-- Evidence Framework
        |       → PHASE 4
        |
        +-- Core Security Test Cases
        |       → PHASE 5
        |
        +-- Regression
        |       → PHASE 9
        |
        +-- CI/CD
        |       → PHASE 10
```

The Phase-3 Completion Gate has been fulfilled for the defined Security Test Architecture scope. The resulting architecture, implementation mapping,
domain integration, and architectural boundaries have been documented.

---

## 20.4 Phase 4 - Evidence Framework

Objective

Establish a structured framework for creation, validation, association, provenance, storage, and lifecycle management of security assessment evidence.

Expected Phase Result

A consistent Evidence Framework provides traceable evidence records that can be associated with test executions, observations, results, findings, and verification activities.

Status: NOT STARTED

## 20.5 Phase 5 - Core Security Test Cases

Objective

Implement and validate the core security test cases for the defined security domains.

Expected Phase Result

The defined core test cases are implemented, executable within their supported environments, associated with evidence, and evaluated according to the applicable test result criteria.

Status: NOT STARTED

## 20.6 Phase 6 - Extended Security Test Cases

Objective

Extend the security assessment coverage with additional technically relevant test cases and security scenarios.

Expected Phase Result

Additional security test cases are implemented, executed where supported, documented, and integrated into the established test and evidence structure.

Status: NOT STARTED

## 20.7 Phase 7 - Findings / Root Cause Analysis

Objective

Establish the structured assessment of confirmed or potential security findings and their technical root causes.

Expected Phase Result

Security findings are traceable to their supporting tests and evidence, and root-cause analysis is documented where sufficient technical evidence exists.

Status: NOT STARTED

## 20.8 Phase 8 - Finding Documentation

Objective

Establish consistent technical documentation for security findings, including evidence, impact, risk, root cause, mitigation, and verification status.

Expected Phase Result

Security findings are documented in a consistent and traceable assessment format that preserves their technical basis and current verification status.

Status: NOT STARTED

## 20.9 Phase 9 - Regression Validation

Objective

Establish repeatable regression validation for implemented security controls, security tests, findings, and mitigations.

Expected Phase Result

Relevant security tests can be repeated after changes and their results can be compared with previous evidence to identify regressions or changes in security behavior.

Status: NOT STARTED

## 20.10 Phase 10 - CI/CD

Objective

Integrate applicable security validation activities into an automated CI/CD workflow.

Expected Phase Result

Applicable security tests and validation checks are integrated into the project's CI/CD workflow and their execution status is observable and traceable.

Status: NOT STARTED

## 20.11 Phase 11 - Professional Packaging

Objective

Prepare the implemented assessment environment and its documentation as a consistent professional engineering deliverable.

Expected Phase Result

The project provides a coherent technical structure, documentation, assessment outputs, evidence organization, and reproducibility information suitable for professional technical presentation.

Status: NOT STARTED

## 20.12 Phase 12 - Final Technical Review / Portfolio Integration

Objective

Perform the final technical review of the implemented project and integrate the resulting engineering documentation into the final project presentation.

Expected Phase Result

The final repository state, implementation, evidence, verification status, documentation, limitations, and assessment results are reviewed for technical consistency and completeness.

Status: NOT STARTED
