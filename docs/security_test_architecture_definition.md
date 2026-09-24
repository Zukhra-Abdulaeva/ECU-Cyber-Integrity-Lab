# Security Test Architecture Definition

## 1. Architecture Objective

The Security Test Architecture defines the common technical structure for organized security testing across the supported security domains.

The architecture establishes:

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
Evaluation
        |
        v
Result
```

The architecture provides a common structure for test organization, domain separation, execution, observation, evaluation, result handling, and traceability.

The architecture is independent of the implementation status of individual components.

A defined architecture does not establish implementation, execution, observation, evidence, or verification.

---

## 2. Common Security Test Architecture

The common Security Test Architecture uses the following conceptual structure:

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
Evaluation
        |
        v
Result
```

Evidence is associated with the execution and observation lifecycle through a separate architectural boundary:

```text
Execution
    |
    v
Observation
    |
    +----> Evidence Boundary
    |
    v
Evaluation
    |
    v
Result
```

This separation preserves the distinction between:

```text
Expected Behaviour
    !=
Actual Observation

Observation
    !=
Result

Result
    !=
Finding
```

The architecture provides a common relationship between assessment objectives, security objectives, test definitions, execution, observation, evaluation, and results.

---

## 3. Assessment Objective

The Assessment Objective defines what security-related aspect is being assessed.

The assessment objective provides the upper-level context for the security objective and the corresponding test objectives.

Relevant questions include:

```text
What security property is being evaluated?

Which asset or component is involved?

Which threat or attack hypothesis is relevant?

Which attack surface is used?

Under which conditions is the assessment applicable?

Which test objectives provide technical evidence for the assessment?
```

The Assessment Objective is not itself a test case or test result.

---

## 4. Security Objective / Property

The Security Objective describes the security property or protection goal relevant to the assessment.

The Security Objective remains distinguishable from the individual Test Objective.

Depending on the assessment context, relevant security properties may include:

```text
Integrity
Authenticity
Confidentiality
Availability
Access Control
Diagnostic Security
Firmware Integrity
Communication Security
```

The applicable security property is determined from the respective assessment objective and technical context.

A defined security property does not establish that the corresponding protection is implemented or verified.

---

## 5. Test Objective

The Test Objective describes what the individual security test is intended to determine.

A Test Objective shall remain traceable to the applicable:

```text
Assessment Objective
Security Objective / Property
Security Test Case
```

A Test Objective may evaluate whether a defined security control or behaviour satisfies a specified security property under defined conditions.

The Test Objective does not constitute a finding or a successful security assessment by itself.

---

## 6. Security Test Case

A Security Test Case defines the technical test structure.

A Test Case shall conceptually contain:

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

The Test Case defines what is tested and under which conditions.

The Test Case definition does not constitute execution evidence.

Expected behaviour must remain separate from actual observation:

```text
Expected Behaviour
    !=
Actual Observation
```

---

## 7. Test Runner

The Test Runner controls the execution flow of a security test.

Its architectural responsibilities include:

```text
Test selection
Test initialization
Precondition handling
Execution control
Lifecycle handling
Result collection
Execution status handling
Error / exception handling
Completion handling
```

The Test Runner is responsible for execution orchestration.

Domain-specific protocol handling, target interaction, or technical processing belongs to the Domain Adapter and Domain Module.

The architecture therefore separates:

```text
Execution orchestration
    !=
Domain-specific interaction
```

---

## 8. Domain Adapter

The Domain Adapter provides the architectural connection between the common test structure and a specific technical domain.

Conceptually:

```text
Common Test Architecture
        |
        v
Domain Adapter
        |
        v
Domain Module
        |
        v
Technical Target / Model
```

The Domain Adapter provides a stable boundary between:

```text
Common test semantics
```

and:

```text
Domain-specific technical interaction
```

The architecture does not assume that all existing domain modules already implement such an adapter boundary.

---

## 9. Domain Module

The Domain Module contains domain-specific interaction or processing.

The architecture preserves domain-specific responsibilities within their respective domain.

Examples include:

```text
CAN communication handling
UDS diagnostic communication
Firmware analysis
Ethernet / IP network interaction
```

The Domain Module is not a generic Test Runner.

It must not redefine project-wide test semantics such as:

```text
Test lifecycle
Result states
Common test structure
Assessment traceability
```

These responsibilities belong to the common architecture.

---

## 10. Target / Model

The Target / Model represents the technical object, artifact, interface, environment, or model against which the test operates.

The architecture distinguishes the target from the test logic.

The applicable execution context may be classified as:

```text
REAL
VIRTUAL
SIMULATED
LOCAL
STATIC
SYNTHETIC
```

These classifications describe the technical context of the target, model, execution, or artifact.

More than one classification may apply to an activity or artifact.

The architecture preserves the distinction between:

```text
Physical target
Virtual interface
Simulated target
Local artifact
Static artifact
Synthetic input
```

The target context is part of the execution context and must not be interpreted independently of the corresponding execution and evidence.

The architecture does not imply real ECU or vehicle validation.

---

## 11. Execution

Execution represents the actual performance of the defined test action under the documented preconditions and execution context.

The common execution interface covers:

```text
Initialization
Preconditions
Input
Execution
Observation
Status
Error Handling
Result Handoff
```

The execution interface separates common test orchestration from domain-specific interaction.

The following states remain distinct:

```text
DESIGNED
IMPLEMENTED
EXECUTED
OBSERVED
VERIFIED
```

A designed test is not necessarily implemented.

An implemented test is not necessarily executed.

An executed test is not necessarily verified.

Documentation of a test does not establish that execution has taken place.

The existence of an execution interface definition does not establish that a corresponding executable interface exists in the repository.

---

## 12. Observation

Observation represents the actual output or behaviour obtained from execution.

Observation is execution-derived information.

The architecture requires the following distinction:

```text
Expected Behaviour
    !=
Actual Observation
```

Observation must remain distinct from:

```text
Test Design
Expected Behaviour
Assumptions
Hypotheses
Synthetic Examples
Planned Results
Result
Evidence
Finding
```

An expected response is not an observation.

A source-code value is not an execution observation unless the relevant execution establishes that interpretation.

If no actual execution has taken place, no executed observation may be claimed.

Observation is an input to evaluation; it is not itself the test result.

---

## 13. Oracle / Evaluation

The Oracle or Evaluation Criteria defines the basis for determining whether the observed behaviour satisfies the Test Objective.

The evaluation relationship is:

```text
Expected Behaviour
        +
Actual Observation
        +
Oracle / Evaluation Criteria
        |
        v
Evaluation
        |
        v
Result
```

The Oracle must be sufficiently defined to support a result decision.

Examples of evaluation criteria include:

```text
Authorization decision
State transition
Protocol response
Message validation
Signature verification
Firmware integrity verification
Rejected malformed input
Denied unauthorized operation
Permitted operation under valid authorization
```

The Oracle must not be derived from the observed result.

A result must not be inferred solely from:

```text
Test existence
Implementation existence
Expected Behaviour
Documentation
Previous status
```

---

## 14. Result

Result represents the evaluated outcome of a test execution.

The project-defined result states are:

```text
PASS
FAIL
NOT_RUN
INCONCLUSIVE
BLOCKED
```

Result evaluation is based on:

```text
Execution
+
Observation
+
Defined Oracle / Evaluation Criteria
```

The following relationship is mandatory:

```text
Observation
    !=
Result
```

Definitions:

```text
PASS
    Required execution occurred, sufficient observation exists,
    and the defined oracle was satisfied.

FAIL
    Required execution occurred and the observed behaviour
    violated the defined oracle.

NOT_RUN
    The test exists or is defined but execution did not occur.

INCONCLUSIVE
    Execution or analysis occurred, but the available information
    does not support a reliable conclusion.

BLOCKED
    Required execution could not meaningfully proceed because an
    identified prerequisite or technical condition was unavailable.
```

`PASS` and `FAIL` require actual execution and sufficient supporting evidence according to the applicable testing model.

A result must not be generated from an expectation alone.

A result does not itself establish a security finding.

---

## 15. Assessment Objective to Result Relationship

The architecture establishes traceability from the Assessment Objective to the executable test structure.

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
Evaluation
        |
        v
Result
```

The relationship connects the purpose of the assessment with the technical result of the test.

Later assessment activities may extend this relationship through:

```text
Result
    |
    v
Assessment
    |
    v
Finding
```

Evidence provides supporting technical material for the applicable execution and observation.

---

## 16. Evidence Boundary

Evidence is an architectural boundary associated with execution and observation.

The architecture preserves the following distinctions:

```text
Test Design
    !=
Execution Evidence

Expected Behaviour
    !=
Observation

Synthetic Input
    !=
Executed Evidence

Simulation
    !=
Real-World Validation
```

Evidence may support the traceability of:

```text
Test
Execution
Observation
Result
```

The detailed creation, validation, provenance, association, storage, and lifecycle management of evidence are maintained separately from this architecture.

The architecture therefore defines the boundary to evidence without representing the complete Evidence Framework as implemented.

---

## 17. Reusable Test Structure

The architecture defines common test responsibilities that can be reused across domains.

Reusable concepts include:

```text
Test identification
Test metadata
Assessment Objective
Security Objective / Property
Test Objective
Preconditions
Inputs
Expected Behaviour
Oracle / Evaluation Criteria
Execution lifecycle
Result semantics
Execution status
Logging boundary
Reporting boundary
```

Domain-specific concepts remain within their respective domain boundaries.

The architecture avoids duplicating common test semantics independently within every domain.

---

## 18. Domain Separation

The architecture separates common test semantics from domain-specific implementation.

The separation is:

```text
COMMON TEST STRUCTURE
    |
    +-- Test Case
    +-- Test Objective
    +-- Preconditions
    +-- Expected Behaviour
    +-- Oracle
    +-- Result Semantics
    +-- Execution Lifecycle
    |
    v
DOMAIN ADAPTER
    |
    +-- CAN
    +-- UDS
    +-- Firmware
    +-- Ethernet
    +-- Other architecturally supported domains
    |
    v
DOMAIN MODULE
    |
    v
TARGET / MODEL
```

A domain-specific implementation must not silently redefine common test semantics or result states.

The architecture distinguishes:

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

## 19. Logging Boundary

Logging remains separate from test semantics.

The architecture distinguishes:

```text
Test Result
    !=
Execution Log
```

Logging may record:

```text
Execution start
Execution end
Execution information
Warnings
Errors
Diagnostic information
```

Logging does not replace:

```text
Observation
Evidence
Result
```

A log entry is not automatically an observation or evidence artifact.

Its technical role depends on the context and provenance of the recorded information.

---

## 20. Reporting Boundary

Reporting is downstream from the technical test result.

Conceptually:

```text
Observation
        |
        v
Evaluation
        |
        v
Result
        |
        v
Reporting
```

Reporting may present information derived from:

```text
Test Results
Observations
Evidence
Assessment Information
```

Reporting shall not create an execution result that does not exist in the underlying test execution.

Existing report-generation components may be connected architecturally where applicable.

The existence of a reporting component does not establish integrated assessment reporting as a completed capability.

---

## 21. Responsibility Separation

The principal architectural responsibilities are separated as follows:

```text
Test Case
    Defines test objective, inputs, preconditions,
    expected behaviour and evaluation criteria.

Test Runner
    Controls the execution flow of a test.

Domain Adapter
    Connects the common test structure to the
    respective technical domain.

Domain Module
    Implements domain-specific interaction or processing.

Target / Model
    Represents the technical target or model used
    by the activity.

Observation
    Records behaviour or output produced by execution.

Evidence Boundary
    Connects execution-derived information to the
    applicable evidence layer.

Result
    Represents the evaluated test outcome.

Logging
    Records execution-related information where applicable.

Reporting
    Presents information derived from available
    technical results and evidence.
```

The separation allows domain-specific implementation details to remain distinguishable from common test semantics.

---

## 22. Architectural Relationship Summary

The complete common test relationship is:

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
        +------> Evidence Boundary
        |
        v
Evaluation
        |
        v
Result
        |
        v
Reporting / Assessment
```

The architecture preserves the following distinctions:

```text
Expected Behaviour
    !=
Observation

Observation
    !=
Evaluation

Observation
    !=
Result

Result
    !=
Finding

Test Execution
    !=
Evidence Framework

Technical Result
    !=
Reporting
```

---

## 23. Architecture Status Semantics

The architecture distinguishes the following technical states:

```text
DESIGNED
    Architecture element is defined.

IMPLEMENTED
    Corresponding implementation artifact exists.

EXECUTED
    Corresponding functionality has actually been executed.

OBSERVED
    Execution produced a documented observation.

VERIFIED
    Required verification conditions are satisfied.
```

A higher state must not be inferred from a lower state.

In particular:

```text
DESIGNED
    !=
IMPLEMENTED

IMPLEMENTED
    !=
EXECUTED

EXECUTED
    !=
OBSERVED

OBSERVED
    !=
VERIFIED
```

An architecture component must not be marked `IMPLEMENTED` merely because it appears in an architecture document.

---

## 24. Architectural Boundaries

The architecture maintains the following boundaries:

```text
Assessment Objective
    !=
Test Objective

Test Case
    !=
Test Runner

Test Runner
    !=
Domain Adapter

Domain Adapter
    !=
Domain Module

Domain Module
    !=
Target / Model

Expected Behaviour
    !=
Observation

Observation
    !=
Result

Result
    !=
Finding

Test Execution
    !=
Evidence Framework

Technical Result
    !=
Reporting
```

These boundaries prevent responsibilities from being silently combined and preserve the distinction between design-time and execution-time information.

---

## 25. Architecture Implementation Principle

The architecture shall be implemented incrementally and only where the corresponding technical requirement is established.

Existing repository functionality shall be preserved unless an architectural correction requires a technically justified change.

Implementation changes shall:

```text
Preserve established functionality where possible
Remain within the defined architectural scope
Remain traceable
Avoid unnecessary architectural redesign
Avoid duplication of common functionality
Preserve domain separation
Preserve status distinctions
Not introduce unrelated future functionality
```

A component is considered implemented only when the corresponding implementation artifact exists.

Implementation does not establish execution or verification.

---

## 26. Repository Relationship

The architecture is mapped against the repository implementation.

Relevant repository components include:

```text
01_framework/base_test.py
01_framework/logger.py
01_framework/config.py
01_framework/report_generator.py

02_security_tests/can/
02_security_tests/uds/
02_security_tests/firmware/
02_security_tests/ethernet/

Existing test files
Existing evidence artifacts
Existing reporting components
```

The repository mapping determines which architectural elements are:

```text
COMMON ARCHITECTURE ELEMENT
DOMAIN-SPECIFIC ELEMENT
SUPPORTING COMPONENT
LEGACY / EXISTING STRUCTURE
PLANNED ARCHITECTURE ELEMENT
UNVERIFIED
NOT APPLICABLE
```

The classification must correspond to the actual repository.

Documentation of an architectural element does not establish its presence in the repository.

---

## 27. Architecture Gap Analysis

The defined architecture is compared with the repository implementation.

The following elements are relevant to the comparison:

```text
Common Test Case structure
Test Runner
Domain Adapter
Domain Module
Target / Model boundary
Observation handling
Result handling
Oracle representation
Logging boundary
Reporting boundary
Assessment-objective relationship
Domain separation
Reusable test structure
Execution interface
```

Each architectural element is assigned an applicable status:

```text
IMPLEMENTED
PARTIALLY IMPLEMENTED
DESIGNED
NOT IMPLEMENTED
UNVERIFIED
NOT APPLICABLE
```

The gap analysis identifies differences between the defined architecture and the current implementation.

An identified architectural gap does not by itself establish a security weakness.

The gap analysis does not establish implementation of capabilities belonging to other technical layers.

---

## 28. Architecture Classification

Architectural elements are classified according to their relationship to the repository and the common test architecture.

The applicable classifications are:

```text
COMMON ARCHITECTURE ELEMENT
    Part of the reusable common test structure.

DOMAIN-SPECIFIC ELEMENT
    Specific to an individual security-test domain.

SUPPORTING COMPONENT
    Supports execution, logging, configuration, reporting,
    or another architectural function without defining
    the common test semantics.

LEGACY / EXISTING STRUCTURE
    Existing repository structure that does not yet fully
    correspond to the defined architecture.

PLANNED ARCHITECTURE ELEMENT
    Architecturally defined but not yet implemented.

UNVERIFIED
    Technical status cannot yet be established sufficiently.

NOT APPLICABLE
    Element does not apply to the respective component or context.
```

Classification reflects the actual technical relationship and must not be used to inflate implementation status.

---

## 29. Traceability Principle

The architecture establishes the following technical relationship:

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
Evaluation
        |
        v
Result
```

Where applicable, evidence provides supporting traceability:

```text
Observation
        |
        v
Evidence
```

Later assessment relationships may extend the chain:

```text
Result
        |
        v
Assessment
        |
        v
Finding
```

The architecture does not require unsupported relationships to be invented.

Missing technical relationships remain identifiable as gaps.

---

## 30. Architecture Integrity Rules

The following rules apply to the architecture:

```text
Expected Behaviour
    must not be represented as Observation.

Observation
    must not be represented as Result.

Result
    must not be represented as Finding.

Test existence
    must not be represented as successful execution.

Implementation existence
    must not be represented as verification.

Architecture documentation
    must not be represented as execution evidence.

Synthetic input
    must not be represented as real-world evidence.

Simulation
    must not be represented as real ECU or vehicle validation.

A result
    must not be generated solely from expected behaviour.

PASS
    must not be assigned without the required execution,
    observation, evaluation and supporting evidence.

FAIL
    must not be assigned merely because a test exists
    or because implementation is incomplete.

Existing domain-specific code
    must not be represented as proof of a complete
    common test architecture.

Architectural terminology
    must not be used to imply implementation where
    the corresponding technical component does not exist.
```

These rules preserve the separation between architecture, implementation, execution, observation, evidence, result, and assessment.

---

## 31. Architectural Outcome

The Security Test Architecture establishes a common structure for organized security testing across the supported domains.

The resulting architecture provides:

```text
Common Test Case Structure
Test Responsibility Separation
Domain Separation
Reusable Test Structure
Test Runner Boundary
Domain Adapter Boundary
Domain Module Boundary
Target / Model Boundary
Execution Interface
Observation Boundary
Oracle / Evaluation Boundary
Result Semantics
Logging Boundary
Reporting Boundary
Assessment Objective Traceability
Evidence Boundary
Repository Relationship
Architecture Status Semantics
```

The architecture establishes the common structure required for later security-test implementation.

It does not itself establish:

```text
Successful Test Execution
Validated Evidence
Confirmed Security Findings
Real-World ECU Validation
Vehicle Validation
Production / OEM Validation
```

These conclusions require their respective technical implementation, execution, observation, evidence, and verification basis.

---

# Historical Project and Phase Context

The architecture described above evolved within the project's defined development model.

The historical phase relationship is retained here only as project history and does not define the current implementation state.

```text
PHASE 1
Repository Foundation

PHASE 2
ECU / Security Domain Model

PHASE 3
Security Test Architecture

PHASE 4
Evidence Framework

PHASE 5
Core Security Test Cases

PHASE 6
Extended Security Test Cases

PHASE 7
Findings / Root Cause Analysis

PHASE 8
Finding Documentation / Risk Assessment

PHASE 9
Regression Validation

PHASE 10
CI/CD

PHASE 11
Professional Packaging

PHASE 12
Final Technical Review / Portfolio Integration
```

The development model separates the responsibilities of the individual phases.

The architecture provides inputs for later implementation and assessment activities but does not establish completion of those later activities.

The historical project and phase development is maintained separately in:

```text
docs/project_definition_and_development_history.md
```

The current repository and implementation state is maintained separately in:

```text
docs/current_state.md
```

Architecture decisions are maintained separately in:

```text
docs/architecture_decisions.md
```

Testing guidance and execution-related information are maintained separately in:

```text
docs/testing.md
```

The separation prevents historical phase information from being interpreted as current implementation or execution status.
