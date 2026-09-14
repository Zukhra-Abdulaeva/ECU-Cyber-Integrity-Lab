# Architecture Decisions

## 1. Purpose

This document records the major architectural decisions of ECU-Cyber-Integrity-Lab and the technical rationale behind them.

The purpose is to provide a stable reference for the structure of the project, the separation of technical responsibilities, the handling of evidence and assessment results, and the relationship between security testing and subsequent verification activities.

The document describes architectural principles and defined target structures. It is separate from `docs/current_state.md`, which records the actual repository, implementation, execution, evidence and verification state.

The architecture is designed around the following engineering principles:

```text
Clear responsibilities
        |
        v
Separated technical states
        |
        v
Traceable execution and evidence
        |
        v
Evidence-bounded assessment
        |
        v
Reproducible security engineering
```

---

## 2. Decision Provenance

The architecture decisions documented here were established during the development of the project and are maintained as project-wide technical principles.

The document distinguishes between:

```text
Current architectural principles
        |
        +-- Stable technical decisions
        |
        +-- Defined interfaces and responsibilities
        |
        +-- Evidence and assessment rules
        |
        +-- Planned architectural extensions

Historical information
        |
        +-- Earlier architectural decisions
        +-- Development-related changes
        +-- Rationale for the resulting structure
```

The current implementation and verification state is maintained separately in `docs/current_state.md`.

A documented architecture therefore defines the intended technical structure and decision basis. Implementation, execution and verification are established separately through the corresponding repository state and technical evidence.

---

## 3. Documentation Architecture

### 3.1 README as Stable Project Entry Point

`README.md` is the stable entry point to the project.

It provides the compact project overview, the automotive security context, the principal engineering workflow, the implementation/planned-scope distinction and the main project boundaries.

Detailed architectural decisions, testing semantics and changing technical status are maintained separately.

```text
README.md
    |
    +-- Project entry point
    +-- Compact project overview
    +-- Scope and boundaries
    +-- Engineering context

Detailed documentation
    |
    +-- Project definition and history
    +-- Architecture decisions
    +-- Testing
    +-- Current technical state
```

### 3.2 Separation of Documentation Roles

The project documentation uses separate documents for different technical responsibilities:

```text
README.md
    Stable project entry point and compact project overview

docs/project_definition_and_phase_history.md
    Project definition, scope, boundaries and historical phase information

docs/architecture_decisions.md
    Architecture decisions and their technical rationale

docs/testing.md
    Security testing model, execution semantics and assessment criteria

docs/current_state.md
    Current repository, implementation, execution, evidence and verification state

docs/environment.md
    Development environment and setup information
```

This separation keeps stable project definition, architectural rationale, testing information and changing repository state distinguishable.

---

## 4. Separation of Repository Artifact Roles

### 4.1 Framework, Security Tests, Evidence, Examples, Reports, Documentation

The repository separates the main technical artifact roles:

```text
01_framework/
    Common framework and assessment components

02_security_tests/
    Security-test implementations and domain-specific test components

03_evidence/
    Evidence and assessment artifacts

04_examples/
    Example assessment material and methodology examples

05_security_reports/
    Assessment reports and report-generation outputs

docs/
    Project and technical documentation
```

The repository structure is part of the established project organization.

The concrete file-level implementation and current status remain maintained in `docs/current_state.md`.

### 4.2 Evidence Is Separate from Examples

Evidence and examples have different technical roles.

```text
Example
    |
    +-- Demonstrates a method, scenario or expected structure

Evidence
    |
    +-- Records a specific technical observation or assessment result
```

Example material can illustrate a security scenario or result structure.

Evidence is associated with a specific technical activity and its execution context.

An example therefore does not become evidence merely because it contains realistic technical values or assessment output.

### 4.3 Examples Are Separate from Reports

Examples illustrate assessment methods, possible results or documentation structures.

Reports represent assessment outputs associated with a defined assessment context.

The two artifact roles remain separate so that example material is not interpreted as an actual project assessment result.

### 4.4 Evidence Is Separate from Reports

Evidence records the technical basis of an observation or assessment activity.

Reports present assessment information derived from the available technical basis.

```text
Execution
    |
    v
Observation
    |
    v
Evidence
    |
    v
Assessment / Result
    |
    v
Report
```

A report is therefore not a substitute for the underlying evidence.

---

## 5. Separation of Technical States

### 5.1 Definition, Implementation, Execution, Observation, Verification

The project distinguishes technical states explicitly:

```text
PLANNED
DESIGNED
IMPLEMENTED
EXECUTED
OBSERVED
VERIFIED
DOCUMENTED
```

These states represent different engineering conditions.

In particular:

```text
DESIGNED      != IMPLEMENTED
IMPLEMENTED   != EXECUTED
EXECUTED      != OBSERVED
OBSERVED      != VERIFIED
DOCUMENTED    != IMPLEMENTED
DOCUMENTED    != VERIFIED
```

An implementation artifact establishes the presence of implementation material.

Execution requires an actual execution activity.

Observation requires an identifiable result or behavior from that execution.

Verification requires the applicable verification criteria and supporting evidence.

Documentation records a technical state but does not establish a higher technical state by itself.

### 5.2 Expected Behaviour and Actual Observation

Expected behavior and actual observation are separate technical fields.

```text
EXPECTED BEHAVIOUR
    |
    | Defined before or independently of execution
    v
TEST ORACLE
    |
    v
ACTUAL OBSERVATION
    |
    | Recorded from execution
    v
RESULT
```

The separation prevents an expected result from being interpreted as an observed result.

### 5.3 Documentation Does Not Establish Technical State

Documentation describes technical information according to its source and status.

The following distinction applies:

```text
Documentation
    !=
Implementation

Documentation
    !=
Execution

Documentation
    !=
Verification
```

The current technical state is therefore maintained separately in `docs/current_state.md`.

---

## 6. Evidence Architecture

### 6.1 Evidence as Independent Technical Layer

Evidence is treated as an independent technical layer between execution/observation and assessment.

```text
Security Test
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
Assessment
```

Evidence can contain information such as:

```text
Evidence ID
Test ID
Domain
Target
Environment
Preconditions
Input
Expected Result
Actual Result
Observation
Result
Execution Status
Timestamp
Artifacts
Tooling
Execution Method
Notes
Provenance
```

The actual availability and completeness of these fields depends on the respective technical activity.

### 6.2 Evidence Lifecycle

The defined evidence lifecycle is:

```text
CREATED
    |
    v
VALIDATED
    |
    v
ASSOCIATED
    |
    v
ACTIVE
    |
    +----> SUPERSEDED
                 |
                 v
             ARCHIVED
```

The lifecycle distinguishes evidence creation, validation, association, active use and historical retention.

```text
CREATED
    Evidence artifact has been generated or captured.

VALIDATED
    Structure, provenance and content have been checked.

ASSOCIATED
    Evidence has been linked to the relevant test, result,
    finding or assessment object.

ACTIVE
    Evidence is the applicable evidence for the associated
    assessment context.

SUPERSEDED
    Newer evidence has replaced the artifact as the applicable
    evidence while the original remains traceable.

ARCHIVED
    Evidence is retained as historical project information.
```

The lifecycle defines the architectural model. It does not establish that a unified evidence-management implementation is already available.

### 6.3 Evidence Provenance

Evidence significance depends on its technical origin and context.

Relevant provenance information includes:

```text
Target
Environment
Execution Method
Timestamp
Input
Observation
Artifacts
Tooling
Association with the respective test
```

Evidence is interpreted according to the context that can be established for the respective artifact.

---

## 7. Examples, Hypotheses, and Findings

### 7.1 Separation of Examples and Security Findings

Security examples, attack hypotheses and confirmed findings have different technical states.

```text
Example
    |
    v
Attack Hypothesis
    |
    v
Test Objective
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
Security Finding
```

A theoretical security possibility can be documented as an attack hypothesis or potential finding.

A confirmed finding requires the corresponding technical basis.

### 7.2 Evidence Before Confirmation

A confirmed security finding is based on an evidence-supported technical assessment.

The architectural rule is:

```text
Hypothesis
    |
    v
Test
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
Assessment
    |
    v
Finding
```

Where the required basis is incomplete, the situation remains classified according to the applicable status, for example:

```text
ATTACK HYPOTHESIS
POTENTIAL FINDING
PROPOSED
UNVERIFIED
INCONCLUSIVE
BLOCKED
```

This keeps technical possibilities distinguishable from confirmed security findings.

---

## 8. Simulation and Real-World Validation Boundaries

### 8.1 Context Classification

The project distinguishes assessment activities by their technical context:

```text
REAL
    Physical real-world hardware, target system or vehicle environment.

VIRTUAL
    Virtualized interface or environment used for testing.

SIMULATED
    Deliberately reproduced or emulated behavior, communication or
    system conditions.

LOCAL
    Execution or analysis within the local controlled laboratory
    environment.

STATIC
    Analysis of an artifact without active interaction with a running
    target system.

SYNTHETIC
    Artificially generated test input or data that does not originate
    from observed real-world traffic or another real-world source.
```

More than one classification can apply to the same artifact or test.

### 8.2 Virtual and Simulated Execution Is Not Real-World Validation

The architectural interpretation is:

```text
Virtual execution
    !=
Physical ECU execution

Synthetic input
    !=
Observed vehicle traffic

Local firmware analysis
    !=
Production firmware validation
```

Virtual, simulated, local, static and synthetic activities remain valid laboratory activities when their context is identified correctly.

Their conclusions remain limited to that context.

### 8.3 Real-World Validation Boundary

A statement concerning a real ECU, real vehicle or real vehicle environment requires evidence corresponding to the respective physical target and execution context.

The defined relationship is:

```text
REAL TARGET
    |
    v
HARDWARE
    |
    v
REAL ENVIRONMENT
    |
    v
EXECUTION
    |
    v
OBSERVATION
    |
    v
EVIDENCE
    |
    v
PROVENANCE
    |
    v
VALIDATION CONCLUSION
```

The conclusion remains limited to the target and environment supported by the evidence.

This architectural boundary is separate from the current project status. The current state of real-world validation is maintained in `docs/current_state.md`.

---

## 9. Test Architecture

### 9.1 Common Test Architecture

The project defines a common test architecture for security-test activities:

```text
Security Requirement
        |
        v
Threat / Attack Hypothesis
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
CAN / UDS / Firmware / Ethernet
        |
        v
Target / Model
        |
        v
Observation
        |
        v
Evidence
        |
        v
Result
```

The architecture provides a common relationship between the security objective, test definition, execution, observation, evidence and result.

The defined architecture is independent of the current implementation status of the individual components.

### 9.2 Separation of Test Responsibilities

The principal responsibilities are separated as follows:

```text
Test Case
    Defines test objective, inputs, preconditions,
    expected behavior and evaluation criteria.

Test Runner
    Controls the execution flow of a test.

Domain Adapter
    Provides the interface between the common test structure
    and the respective technical domain.

Domain Module
    Implements domain-specific interaction or processing.

Target / Model
    Represents the technical target or model used by the activity.

Observation
    Records behavior or output produced by execution.

Evidence
    Preserves the technical basis associated with the observation.

Result
    Represents the evaluated test outcome.

Logging
    Records execution-related information where applicable.

Reporting
    Presents assessment information derived from the available
    technical results and evidence.
```

The separation allows domain-specific implementation details to remain distinguishable from common test semantics.

### 9.3 Evidence Classification

Security-test evidence is classified according to its origin and execution context.

The project distinguishes in particular:

```text
SYNTHETIC
    Generated test data or input.

SIMULATED
    Behavior or execution involving a simulated target or condition.

EXECUTED
    Evidence originating from an actual test execution.
```

The evidence classification must correspond to the actual origin of the artifact.

Synthetic or simulated material is not classified as executed evidence merely because it represents an executable scenario.

---

## 10. Security Engineering Lifecycle

The architecture connects the security engineering activities through a traceable technical relationship:

```text
Security Requirement
        |
        v
Security Objective / Property
        |
        v
Threat / Attack Hypothesis
        |
        v
Attack Surface
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
Assessment / Finding
        |
        v
Mitigation
        |
        v
Retest
        |
        v
Verification
        |
        v
Regression
```

The complete sequence is not required for every individual activity.

It defines the relationship between the engineering stages and provides the basis for traceability.

---

## 11. Finding-Driven Regression

Regression is derived from security findings and their associated controls.

The defined relationship is:

```text
Finding
    |
    v
Security Control / Mitigation
    |
    v
Retest
    |
    v
Regression Test
    |
    v
Future Change Trigger
```

Relevant future change triggers include changes to:

```text
Firmware
Diagnostic behavior
Network configuration
OTA functionality
ECU or gateway behavior
Security configuration
```

A regression test becomes part of the implemented project capability only when the corresponding implementation and execution state are established.

The architectural model therefore remains separate from the current regression implementation status.

---

## 12. CI/CD Architecture

The defined CI/CD architecture follows the sequence:

```text
Checkout
    |
    v
Environment Setup
    |
    v
Dependency Installation
    |
    v
Static Checks
    |
    v
Unit Tests
    |
    v
Security Tests
    |
    v
Evidence Generation
    |
    v
Regression Tests
    |
    v
Report Generation
    |
    v
Artifact Upload
    |
    v
Security Gate
```

CI/CD automation is limited to activities that are technically reproducible within the configured execution environment.

The architecture separates:

```text
CI Configuration
    !=
CI Execution
    !=
CI Verification
```

A configured workflow provides an automation definition. Successful execution and verification require their own technical basis.

The CI/CD architecture is a defined project architecture. Its implementation and verification status are maintained in `docs/current_state.md`.

---

## 13. Completion Status and Quality Level

### 13.1 Completion Gates

Engineering work is associated with explicit completion criteria.

The architectural principle is:

```text
Defined Work
    |
    v
Implementation / Documentation
    |
    v
Applicable Testing
    |
    v
Execution
    |
    v
Evidence / Review
    |
    v
Completion Gate
```

Completion is recorded only after the applicable completion criteria have been fulfilled and the resulting technical state has been documented.

### 13.2 Quality Levels

The project uses the following internal quality interpretation:

```text
Q0 — Undefined
Q1 — Initial / Fragmented
Q2 — Basic / Partially Verified
Q3 — Structured / Reproducible
Q4 — Evidence-Based / Consistently Verified
Q5 — Mature / Fully Controlled
```

These levels describe project maturity within the project's internal engineering model.

They do not represent external certification or compliance with an external standard.

The current quality level is maintained in `docs/current_state.md`.

---

## 14. Architecture Integrity Principles

### 14.1 State Separation

The architecture maintains explicit separation between technical states:

```text
PLANNED
DESIGNED
IMPLEMENTED
EXECUTED
OBSERVED
VERIFIED
DOCUMENTED
```

The states are interpreted independently.

A higher state requires the corresponding technical basis.

### 14.2 Evidence-Bounded Conclusions

Technical conclusions remain within the scope established by the available evidence.

```text
Execution
    |
    v
Observation
    |
    v
Evidence
    |
    v
Assessment
    |
    v
Conclusion
```

A conclusion is therefore limited by the target, environment, execution, observation and evidence that support it.

### 14.3 Reproducibility

The architecture supports reproducible laboratory work through:

```text
Defined repository structure
Version-controlled project files
Documented dependencies
Documented development environment
Explicit test procedures
Separate evidence artifacts
Defined execution and result semantics
```

Reproducibility depends on the availability of the required software, interfaces, targets and execution environment for the respective activity.

---

## 15. Historical Architecture Principles

The project architecture developed toward a more explicit separation of technical states, evidence and assessment information.

The following principles were established during that development:

```text
Implementation, execution, observation and verification are distinct states.

Security findings require evidence-backed technical reasoning.

Simulation and virtual execution remain distinguishable from physical
ECU or vehicle validation.

Example assessment material remains distinguishable from confirmed
project findings.

Documentation records technical information but does not replace
execution evidence.

Completion is controlled through explicit engineering criteria.

Current technical state remains separate from stable project definition
and historical project information.
```

These principles remain part of the architectural basis of the project.

Detailed project and phase history is maintained in:

```text
docs/project_definition_and_phase_history.md
```

---

## 16. Decision Summary

The architecture is based on the following decisions:

```text
1. README.md serves as the stable project entry point.

2. Project definition and phase history are maintained separately
   from changing repository state.

3. Architecture decisions are documented independently from
   current implementation status.

4. Testing information is maintained independently from architecture
   rationale and current project status.

5. Repository artifacts are separated according to their technical role.

6. Evidence is treated as an independent technical layer.

7. Evidence is kept separate from examples.

8. Examples are kept separate from assessment reports.

9. Evidence is kept separate from reports.

10. Planned, designed, implemented, executed, observed and verified
    states are interpreted separately.

11. Expected behavior is kept separate from actual observation.

12. Evidence provenance and lifecycle are treated as technical
    assessment properties.

13. Security hypotheses and potential findings are separated from
    confirmed findings.

14. Simulation, virtual execution, local analysis and synthetic input
    are classified according to their actual context.

15. Real-world ECU or vehicle validation requires corresponding
    physical-target evidence and provenance.

16. Security testing follows a common conceptual architecture with
    test cases, runners, domain adapters, targets, observations,
    evidence and results.

17. Security assessment follows a traceable engineering lifecycle.

18. Findings provide the basis for retest and future regression.

19. Regression is treated as a separate architectural capability.

20. CI/CD is structured around reproducible technical activities
    and an explicit security gate.

21. CI configuration, CI execution and CI verification are treated
    as separate states.

22. Architecture quality and project maturity are assessed separately
    from external certification or compliance claims.
```

The decisions above define the architectural basis of ECU-Cyber-Integrity-Lab. They do not by themselves establish the implementation, execution or verification status of the corresponding technical capabilities.