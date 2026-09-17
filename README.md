# ECU-Cyber-Integrity-Lab

## Automotive White-Box Security Assessment

**Author:** Zukhra Abdulaeva

**Focus:** Automotive Cybersecurity • Embedded Systems • Security Testing • Python Automation

A practical laboratory project for the structured security assessment of connected vehicle systems and Electronic Control Units (ECUs).

The project applies a White-Box perspective to automotive cybersecurity and combines system and architecture analysis with technical security testing, diagnostic assessment, firmware review, risk assessment and engineering recommendations.

The repository contains selected implementations, test structures, documentation, examples and evidence artifacts. The current implementation state is documented separately from the broader project scope and planned extensions.

---

## Project Identity

`ECU-Cyber-Integrity-Lab` is an automotive cybersecurity engineering laboratory for structured White-Box assessment of ECU-oriented systems, communication interfaces, diagnostic services, firmware and related security mechanisms.

The project is organized around a traceable engineering workflow in which implementation, execution, observation, evidence and verification are treated as separate technical states.

---

## Project Purpose

The purpose of the project is to provide a reproducible technical environment for examining automotive cybersecurity concepts and carrying out security-assessment activities in a controlled laboratory context.

The engineering workflow connects:

```text
System and Architecture Understanding
            |
            v
Threat and Security Analysis
            |
            v
Technical Security Testing
            |
            v
Observation and Evidence
            |
            v
Risk and Root-Cause Analysis
            |
            v
Security Improvement
```

The workflow describes the intended engineering method. It does not imply that every activity is currently implemented, executed or verified in the repository.

---

## Project Overview

Modern vehicles integrate numerous ECUs, communication networks, diagnostic interfaces and software components. Increasing connectivity creates a complex attack surface that must be considered throughout the security-engineering process.

The project covers engineering activities including:

- system and architecture analysis
- threat modeling
- source-code and implementation review
- communication and network security testing
- UDS diagnostic security assessment
- firmware review
- Python-based security testing and automation
- risk assessment
- technical reporting
- engineering recommendations
- establishment of an ECU‑oriented security‑domain model
- structured definition of ECUs/components, communication domains, interfaces, assets, and security properties

These activities describe the project scope. The repository currently contains implementations for selected areas, while other activities remain contextual or planned.

---

## Assessment Workflow

The assessment workflow is structured around the following activities:

```text
1. Scope Definition
2. System Architecture Review
3. Threat Modeling
4. White-Box Code Analysis
5. Communication and Network Security Assessment
6. UDS Security Assessment
7. Firmware Review
8. Python Security Automation
9. Risk Assessment
10. Technical Reporting
11. Engineering Recommendations
```

Individual activities are represented by repository implementations, documentation, examples or planned extensions according to their respective scope.

---

## Automotive Context

The project is positioned within the security context of modern connected vehicle systems.

The automotive context includes technologies, system components and security mechanisms such as:

```text
Vehicle and ECU Architecture

* Electronic Control Units (ECUs)
* Gateway ECUs
* Body Control Modules (BCMs)
* Powertrain ECUs
* Infotainment ECUs
* Telematics Control Units (TCUs)
* ADAS Controllers

Vehicle Communication

* CAN
* CAN FD
* Automotive Ethernet
* LIN
* FlexRay

Diagnostics and External Interfaces

* UDS
* OBD-II
* Bluetooth
* USB
* Wi-Fi
* Cellular connectivity
* OTA update mechanisms

Security Engineering Areas

* Gateway and trust-boundary concepts
* Diagnostic services
* Firmware integrity
* Firmware security
* Secure Boot
* Network communication
* Remote connectivity
* Threat modeling
* Security requirements
* Risk assessment
```

The technologies and areas above define the automotive engineering context. Their inclusion does not indicate that the corresponding technology or security mechanism is implemented in the repository.

### Currently Implemented

The repository contains technical implementations for selected areas:

```text
Communication and Diagnostics

* CAN message capture
* Virtual CAN message generation
* CAN security test structure
* UDS request and response handling
* UDS security-related test structure

Firmware

* Firmware SHA-256 integrity calculation
* Firmware integrity checking
* Firmware comparison

Network

* Ethernet / IP network scanning
* Nmap-based network and port scanning

Assessment and Reporting

* Python-based security assessment tooling
* Test infrastructure
* Report-generation component
* Assessment evidence and report artifacts
```

The repository also contains `config.py` and `logger.py` files. Their presence does not establish an implemented configuration or logging capability. The current implementation state of these components is documented in `docs/current_state.md`.

The listed implementations are not presented as fully integrated, end-to-end or real-vehicle functionality. Execution and verification are assessed separately from implementation.

### Planned / Future

The broader automotive context provides a basis for future extensions of the laboratory.

Potential extensions include:

```text
Communication and Network Security

* CAN FD security testing
* LIN security assessment
* FlexRay security assessment
* Extended Automotive Ethernet analysis
* SOME/IP security testing

Diagnostics and External Interfaces

* Extended OBD-II security assessment
* Bluetooth security assessment
* USB security assessment
* Wi-Fi security assessment
* Cellular security assessment
* OTA security assessment

Embedded and Firmware Security

* Extended firmware analysis
* Secure Boot validation
* Additional firmware security analysis

Security Engineering

* Extended threat modeling
* Additional security test automation
* Integrated evidence and finding workflows
* Regression security validation
* CI/CD security validation
```

These areas describe planned or future project scope. They are not presented as implemented functionality without corresponding implementation and supporting evidence.

### Context and Implementation Boundary

The relationship between project context, current implementation and planned extensions is:

```text
AUTOMOTIVE CONTEXT
    |
    +-- ECU architecture
    +-- Vehicle networks
    +-- Diagnostics
    +-- Firmware
    +-- External interfaces
    +-- Security mechanisms
    |
    v
ECU / SECURITY DOMAIN MODEL
    |
    +-- ECU / component context
    +-- Communication domains
    +-- Interfaces
    +-- Assets
    +-- Security properties
    +-- Security-domain relationships
    |
    v
CURRENT IMPLEMENTATION
    |
    +-- CAN
    +-- UDS
    +-- Firmware validation
    +-- Ethernet / IP network scanning
    +-- Reporting component
    +-- Python security tooling
    |
    v
PLANNED / FUTURE
    |
    +-- Additional automotive protocols
    +-- Extended security analysis
    +-- Additional test automation
    +-- Evidence and finding workflows
    +-- Regression validation
    +-- CI/CD security validation
```

This separation keeps the automotive engineering context distinct from repository functionality and planned scope.

---

## Non-Scope

The project does not represent:

```text
- Production vehicle security validation
- OEM fleet security validation
- Validation of a specific production ECU
- Validation of a production vehicle
- Real-world penetration testing of third-party systems
- Production security certification
- Formal ISO/SAE 21434 compliance certification
- OEM security approval
- Fleet-wide security assurance
```

Example data, simulated communication, local test execution and documented expectations are not treated as evidence of behavior in a production vehicle or production ECU.

---

## Simulation Boundary

The laboratory may use virtual, simulated or locally controlled environments to reproduce automotive security concepts.

Examples include:

```text
* Virtual CAN interfaces
* Locally generated CAN messages
* Local ECU or diagnostic models
* Protocol-level test scenarios
* Synthetic firmware inputs
* Locally generated security-test data
```

These activities are valid laboratory engineering activities when their execution context is explicitly identified. Simulation, emulation and synthetic data remain distinguishable from observations obtained from a real ECU, real vehicle, production network or OEM environment.

---

## Real-World Validation Boundary

Real-world validation requires an appropriate physical target, defined test environment and corresponding execution evidence.

Examples include:

```text
* Physical ECU
* Physical CAN or CAN FD network
* Physical Automotive Ethernet network
* Vehicle diagnostic interface
* Production-representative firmware
* Controlled vehicle test environment
```

The presence of test code or example artifacts does not by itself establish validation against a physical ECU, production vehicle, OEM environment or fleet.

---

## White-Box Approach

The project is based on a White-Box assessment model in which technical information about the assessment target is available for analysis.

Depending on the assessment scope, this may include:

```text
* ECU Documentation
* Source Code
* Firmware Images
* ODX / PDX Diagnostic Descriptions
* Communication Matrix
* Network Architecture
* Security Requirements
```

The White-Box approach allows security analysis to consider implementation details, architectural dependencies and potential root causes in addition to externally observable behavior. The depth of an assessment depends on the technical information available for the respective assessment target.

---

## Assessment Methodology

The assessment methodology incorporates established automotive cybersecurity concepts and engineering practices, including:

```text
* ISO/SAE 21434
* Secure Development Lifecycle (SDL)
* Threat Modeling
* Secure Coding
* Root Cause Analysis
* Risk Assessment
```

These concepts provide methodological guidance for structuring security assessment activities and documenting technical results. Their inclusion does not constitute a compliance or certification claim.

---

## Security Engineering Goals

The primary engineering goals are:

```text
* Understand the system and its security boundaries
* Identify relevant assets and security properties
* Identify threats and attack surfaces
* Define technically meaningful security tests
* Execute tests within a controlled environment
* Capture actual observations
* Preserve reproducible evidence
* Distinguish confirmed observations from assumptions and examples
* Assess security impact and risk
* Identify technically supported root causes
* Derive practical security improvements
* Support retesting and regression validation
```

The engineering focus is on traceability between security objectives, technical tests, observations, evidence and resulting assessments.

---

## Security Domains

### ECU / Security Domain Model

The project defines an ECU / Security Domain Model covering:

```text
ECU / Component
Communication Domains
Interfaces
Assets
Security Properties
Security-Domain Relationships
Attack-Surface Context
Traceability
Boundaries
```

The model provides the structural relationship between ECU-oriented elements and the existing technical security-assessment scope.

### Communication and Network Security

The communication and network security domain covers technologies relevant to the project context and its implementations:

```text
CAN
CAN FD
Automotive Ethernet
SocketCAN
Wireshark
Scapy
CANoe
```

The current repository contains CAN-related Python tooling and network-scanning functionality. Other technologies listed here provide broader technical context unless corresponding implementation and execution evidence is available.

### Diagnostic Security

The diagnostic security domain includes:

```text
UDS
ISO 14229
Security Access
Diagnostic Services
```

The repository contains Python-based UDS request and response handling and a corresponding test structure.

### Firmware Security

The firmware-security domain includes:

```text
Firmware Images
Binwalk
Firmware Mod Kit
Secure Boot
Firmware Review
```

The repository contains firmware hashing, integrity comparison and firmware review material. Additional firmware-security technologies remain contextual or planned unless corresponding implementation and evidence are available.

### Source-Code and Static Analysis

The White-Box and static-analysis domain includes:

```text
CodeQL
Coverity
SonarQube
Cppcheck
```

These tools represent analysis technologies within the project context. Their inclusion does not indicate that the corresponding analysis has been executed.

### Security Automation

The Python-based automation environment includes:

```text
Python
pytest
python-can
can-isotp
python-nmap
```

These technologies support the project's security-testing and automation approach.

### Risk Assessment

The risk-assessment domain includes:

```text
CVSS
Risk Assessment
Security Findings
Root Cause Analysis
```

Risk assessment and root-cause analysis are part of the engineering workflow. Example findings and proposed assessments are not automatically confirmed security findings.

---

## Evidence Principle

Security conclusions are limited to what the available evidence supports.

A test definition, source-code implementation or documented expectation does not establish that the corresponding behavior was observed during execution.

Where applicable, evidence records preserve:

```text
Test Identifier
Target
Environment
Preconditions
Input
Expected Behavior
Actual Observation
Execution Status
Result
Timestamp
Artifacts
Tooling / Execution Method
Provenance
```

Evidence is interpreted according to its actual provenance and execution context.

---

## Truth-State Model

The project distinguishes between the following technical states:

```text
Planned
Designed
Implemented
Executed
Observed
Verified
Documented
```

These states describe different engineering conditions and are not interchangeable.

In particular:

```text
Implemented != Executed
Executed != Observed
Observed != Verified
Expected != Observed
Example != Evidence
Simulation != Real-World Validation
```

---

## Security Assessment and Findings

Security analysis follows a traceable engineering chain:

```text
Asset
  |
  v
Security Property
  |
  v
Threat
  |
  v
Attack Surface
  |
  v
Attack Vector
  |
  v
Attacker Capability
  |
  v
Preconditions
  |
  v
Attack Path
  |
  v
Test Objective
  |
  v
Test Design
  |
  v
Execution
  |
  v
Observation
  |
  v
Evidence
  |
  v
Finding
  |
  v
Impact
  |
  v
Risk
  |
  v
Mitigation
  |
  v
Retest / Verification
```

A confirmed security finding requires sufficient execution and evidence to support the conclusion.

Where evidence is incomplete, an assessment can instead be represented as:

```text
ATTACK HYPOTHESIS
POTENTIAL FINDING
PROPOSED
UNVERIFIED
INCONCLUSIVE
BLOCKED
```

Example findings and example assessment results remain examples unless supporting evidence establishes the corresponding security condition.

---

## Assessment Results

Executable security tests use explicit result semantics:

```text
PASS
FAIL
NOT_RUN
INCONCLUSIVE
BLOCKED
```

A `PASS` or `FAIL` result requires actual execution, a defined evaluation criterion and supporting evidence. Expected behavior is recorded separately from actual observation.

---

## Repository Structure

The repository is organized into the following main areas:

```text
01_framework/
    Common assessment framework components

02_security_tests/
    Technical security tests and test implementations

03_evidence/
    Assessment evidence and execution-related artifacts

04_examples/
    Assessment methodology and example documentation

05_security_reports/
    Assessment reports and report-generation outputs

docs/
    Project and technical documentation
```

The structure reflects the current repository organization; individual components may have different implementation and verification states.

---

## Documentation Structure

The README is the stable project entry point. Detailed project definition, current state and technical documentation are maintained separately.

```text
README.md
    Stable project entry point and compact project overview

docs/project_definition_and_phase_history.md
    Project definition, detailed scope, engineering models,
    phase structure and historical phase information

docs/environment.md
    Development environment and setup information

docs/architecture_decisions.md
    Architecture decisions and their technical rationale

docs/testing.md
    Testing approach and execution guidance

docs/ecu_security_domain_model.md

    ECU-oriented security domain model including ECU / component
    context, communication domains, interfaces, assets, security
    properties, relationships, boundaries and model traceability

docs/current_state.md
    Current repository, implementation, execution,
    evidence and verification state

docs/White-Box-Ansatz.png
    White-Box assessment concept

docs/Automotive_Security_Assessment.pdf
    Automotive security assessment reference material
```

The documentation separates stable project definition and methodology from the evolving technical current state so that implementation, execution, evidence and verification remain traceable.

---

## Reproducibility

The project is structured to support reproducible laboratory work through:

```text
Defined repository structure
Version-controlled project files
Python dependencies
Documented development environment
Explicit test procedures
Separate evidence artifacts
Defined execution and result semantics
```

The development environment and setup requirements are documented in `docs/environment.md`.

Reproducibility depends on the availability of the required software, interfaces, test targets and execution environment for the respective activity.

---

## Engineering Principle

The project applies one fundamental rule when interpreting technical results:

```text
Implementation
     |
     v
Execution
     |
     v
Observation
     |
     v
Conclusion
```

Each conclusion must remain within the scope established by the preceding technical evidence.
