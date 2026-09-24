# Test Responsibility Matrix

## 1. Purpose

The Test Responsibility Matrix defines the responsibilities and architectural boundaries of the common Security Test Architecture.

For each common architecture component, the matrix establishes:

```text
Primary Responsibility
Inputs
Outputs
Dependencies
Boundary
Implementation Status
```

The matrix separates common test responsibilities from domain-specific implementation and distinguishes the defined architecture from the current repository implementation.

Implementation status reflects the current repository state.

```text
DESIGNED
IMPLEMENTED
PARTIALLY IMPLEMENTED
NOT IMPLEMENTED
UNVERIFIED
```

`IMPLEMENTED` does not imply execution or verification.

---

## 2. Responsibility Matrix

| Component             | Primary Responsibility                                                                                                                  | Inputs                                                                                                                                                                              | Outputs                                                                | Dependencies                                                                        | Boundary                                                                       | Implementation Status     |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------- |
| **Test Case**         | Defines what is tested and establishes the test-specific objectives, preconditions, inputs, expected behaviour and evaluation criteria. | Test ID, name, security domain, assessment objective, security objective/property, test objective, preconditions, inputs, actions, expected behaviour, oracle, target/model context | Defined test specification and executable test intent                  | Assessment Objective, Security Objective / Property, Test Objective, Target / Model | Separates test definition from execution and observation                       | **PARTIALLY IMPLEMENTED** |
| **Test Runner**       | Controls test selection, initialization, preconditions, execution lifecycle, status handling, result collection and completion.         | Test Case, execution context, preconditions, execution request                                                                                                                      | Execution state, observations/result handoff, execution status, errors | Test Case, Domain Adapter, execution environment                                    | Separates execution orchestration from domain-specific interaction             | **NOT IMPLEMENTED**       |
| **Domain Adapter**    | Provides the stable interface between common test semantics and domain-specific execution.                                              | Common test execution request, target/model context, domain-specific parameters                                                                                                     | Domain execution request, normalized interaction/observation handoff   | Test Runner, Domain Module, Target / Model                                          | Boundary between common architecture and domain-specific technical interaction | **NOT IMPLEMENTED**       |
| **Domain Module**     | Performs domain-specific technical interaction or processing.                                                                           | Domain-specific inputs, target/model, protocol or analysis parameters                                                                                                               | Domain-specific execution output and observations                      | Domain technology, target/model, domain-specific libraries/interfaces               | Keeps CAN, UDS, Firmware and Ethernet interaction within their domains         | **IMPLEMENTED**           |
| **Target / Model**    | Represents the technical object, environment or artifact against which a test operates.                                                 | Target configuration, model data, local artifacts, virtual/simulated interfaces where applicable                                                                                    | Target/model access and technical interaction context                  | Execution environment, domain module                                                | Separates the test architecture from the technical target/model                | **PARTIALLY IMPLEMENTED** |
| **Observation**       | Represents actual behaviour or output obtained from execution.                                                                          | Execution output, target response, measured or returned technical data                                                                                                              | Actual observation                                                     | Execution, Target / Model, Domain Module                                            | Separates actual execution-derived behaviour from expected behaviour           | **PARTIALLY IMPLEMENTED** |
| **Evidence Boundary** | Defines the architectural boundary through which execution/observation information can become assessment evidence.                      | Observation, execution metadata, relevant technical artifacts                                                                                                                       | Evidence input/boundary for later evidence processing                  | Observation, Execution, later Evidence Framework                                    | Separates Phase-3 test architecture from Phase-4 Evidence Framework            | **DESIGNED**              |
| **Result**            | Represents the evaluated outcome of a test based on execution, observation and defined evaluation criteria.                             | Execution state, observation, oracle/evaluation criteria                                                                                                                            | PASS, FAIL, NOT_RUN, INCONCLUSIVE or BLOCKED                           | Execution, Observation, Oracle                                                      | Separates evaluation outcome from test definition and raw observation          | **PARTIALLY IMPLEMENTED** |
| **Logging**           | Records execution-related information, diagnostics, warnings, errors and lifecycle information without replacing test semantics.        | Execution events, diagnostic information, warnings, errors                                                                                                                          | Log records                                                            | Test execution and logging infrastructure                                           | Separates execution logging from observation, evidence and result semantics    | **PARTIALLY IMPLEMENTED** |
| **Reporting**         | Presents technical test information and results without creating unsupported execution or assessment claims.                            | Test results, execution information, report data                                                                                                                                    | Reports and report artifacts                                           | Result, existing reporting components, available test data                          | Downstream from technical test execution and result generation                 | **PARTIALLY IMPLEMENTED** |

---

## 3. Test Case

### Primary Responsibility

The Test Case defines the test itself.

It establishes:

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

The Test Case therefore defines test intent and test structure.

It does not represent actual execution.

### Inputs

```text
Assessment Objective
Security Objective / Property
Test Objective
Test metadata
Preconditions
Inputs / Stimulus
Target / Model context
Expected Behaviour
Oracle / Evaluation Criteria
```

### Outputs

```text
Defined Test Case
Test execution intent
Expected Behaviour
Evaluation criteria
Traceability information
```

### Dependencies

```text
Assessment Objective
Security Objective / Property
Test Objective
Target / Model
Common Test Architecture
```

### Boundary

The Test Case ends at test definition.

It must remain separate from:

```text
Actual Execution
Actual Observation
Evidence
Result
Finding
```

In particular:

```text
Expected Behaviour
    !=
Actual Observation
```

### Implementation Status

```text
PARTIALLY IMPLEMENTED
```

The repository contains a common `BaseSecurityTest` and domain-specific test structures, but the complete Phase-3 common Test Case model is not implemented as a unified architecture.

---

## 4. Test Runner

### Primary Responsibility

The Test Runner controls the common execution lifecycle.

Responsibilities include:

```text
Test selection
Initialization
Precondition handling
Execution control
Lifecycle handling
Result collection
Execution status
Error / exception handling
Completion
```

### Inputs

```text
Test Case
Execution Context
Preconditions
Execution Request
Target / Model Context
```

### Outputs

```text
Execution Status
Execution Outcome
Observation Handoff
Result Handoff
Execution Errors
Completion State
```

### Dependencies

```text
Test Case
Domain Adapter
Execution Environment
Target / Model
```

### Boundary

The Test Runner provides execution orchestration.

It does not own:

```text
CAN protocol logic
UDS protocol logic
Firmware analysis logic
Ethernet scanning logic
Target-specific implementation
```

Those responsibilities remain domain-specific.

### Implementation Status

```text
NOT IMPLEMENTED
```

The current repository contains a common base-test structure but no complete common Test Runner corresponding to the Phase-3 responsibility model.

---

## 5. Domain Adapter

### Primary Responsibility

The Domain Adapter provides the stable boundary between common test semantics and domain-specific execution.

### Inputs

```text
Common Test Case information
Execution request
Target / Model context
Domain-specific parameters
```

### Outputs

```text
Domain execution request
Normalized execution interaction
Observation handoff
Execution status
Domain errors
```

### Dependencies

```text
Test Runner
Domain Module
Target / Model
Domain-specific execution environment
```

### Boundary

The boundary is:

```text
COMMON TEST ARCHITECTURE
        |
        v
DOMAIN ADAPTER
        |
        v
DOMAIN-SPECIFIC IMPLEMENTATION
```

The adapter must not redefine common test semantics.

### Implementation Status

```text
NOT IMPLEMENTED
```

The repository contains domain modules but does not establish the common Phase-3 Domain Adapter boundary as an implemented reusable interface.

---

## 6. Domain Module

### Primary Responsibility

The Domain Module performs technical interaction or processing specific to a security-test domain.

Current repository domains include:

```text
CAN
UDS
Firmware
Ethernet
```

### Inputs

Depending on the domain:

```text
Protocol parameters
Target information
Test-specific inputs
Domain-specific configuration
Local artifacts
Execution parameters
```

### Outputs

```text
Domain-specific technical output
Execution information
Domain-specific observations
Analysis output
```

### Dependencies

Domain-specific modules may depend on:

```text
Python libraries
Protocol interfaces
Local artifacts
Target / Model
Execution environment
```

### Boundary

Domain-specific functionality remains inside its domain.

The Domain Module does not define:

```text
Common Test Case semantics
Common Test Runner semantics
Project-wide Result semantics
Evidence Framework lifecycle
Finding lifecycle
```

### Implementation Status

```text
IMPLEMENTED
```

The repository contains domain-specific implementation for CAN, UDS, Firmware and Ethernet. The existence of these modules does not establish their integration into the complete common Phase-3 architecture.

---

## 7. Target / Model

### Primary Responsibility

The Target / Model represents the technical object, environment or artifact against which a test operates.

The project distinguishes contexts such as:

```text
REAL
VIRTUAL
SIMULATED
LOCAL
STATIC
SYNTHETIC
```

### Inputs

```text
Target configuration
Model information
Local artifacts
Virtual interfaces
Simulation parameters
Domain-specific target parameters
```

### Outputs

```text
Target access
Model state
Technical interaction context
Target responses
```

### Dependencies

```text
Execution Environment
Domain Module
Target-specific interfaces
Available artifacts
```

### Boundary

The Target / Model remains separate from common test logic.

The architecture must preserve:

```text
Test Logic
    !=
Target / Model
```

and:

```text
SIMULATED
    !=
REAL-WORLD VALIDATION
```

### Implementation Status

```text
PARTIALLY IMPLEMENTED
```

The repository contains virtual/local/simulated target contexts and domain-specific target interaction, but no unified Phase-3 Target / Model interface is established.

---

## 8. Observation

### Primary Responsibility

Observation represents actual output or behaviour obtained from execution.

### Inputs

```text
Execution
Target / Model response
Domain Module output
Technical measurements or returned data
```

### Outputs

```text
Actual Observation
Observation data
Execution-derived technical information
```

### Dependencies

```text
Execution
Target / Model
Domain Module
Execution environment
```

### Boundary

Observation must remain separate from:

```text
Expected Behaviour
Oracle
Result
Evidence
Finding
```

The mandatory distinction is:

```text
Expected Behaviour
    !=
Actual Observation
```

### Implementation Status

```text
PARTIALLY IMPLEMENTED
```

The domain-specific implementations produce result/output structures and execution-derived information, but the common Phase-3 Observation abstraction is not implemented as a unified architecture component.

---

## 9. Evidence Boundary

### Primary Responsibility

The Evidence Boundary defines where execution and observation information can enter the later evidence layer.

### Inputs

```text
Observation
Execution information
Execution context
Relevant technical artifacts
```

### Outputs

```text
Evidence input
Evidence association boundary
Traceability information
```

### Dependencies

```text
Observation
Execution
Phase-4 Evidence Framework
```

### Boundary

Phase 3 defines only the architectural boundary.

The following remain Phase-4 responsibilities:

```text
Evidence creation
Evidence validation
Evidence provenance
Evidence association
Evidence storage
Evidence lifecycle
```

### Implementation Status

```text
DESIGNED
```

The Phase-3 architecture defines the boundary. The complete Evidence Framework is explicitly outside Phase 3.

---

## 10. Result

### Primary Responsibility

Result represents the evaluated outcome of the test.

The defined result states are:

```text
PASS
FAIL
NOT_RUN
INCONCLUSIVE
BLOCKED
```

### Inputs

```text
Execution state
Actual Observation
Oracle / Evaluation Criteria
Test validity context
```

### Outputs

```text
PASS
FAIL
NOT_RUN
INCONCLUSIVE
BLOCKED
```

### Dependencies

```text
Execution
Observation
Oracle / Evaluation Criteria
Test Case
```

### Boundary

Result is distinct from:

```text
Expected Behaviour
Observation
Evidence
Finding
```

The architectural evaluation is:

```text
Execution
+
Observation
+
Oracle
=
Result
```

### Implementation Status

```text
PARTIALLY IMPLEMENTED
```

The repository contains result/status structures inside existing domain implementations and the common base test, but the project-wide Phase-3 Result semantics are not implemented as a unified common result model.

---

## 11. Logging

### Primary Responsibility

Logging records execution-related information without replacing test semantics.

Potential information includes:

```text
Execution start
Execution end
Execution information
Warnings
Errors
Diagnostic information
```

### Inputs

```text
Execution events
Lifecycle events
Warnings
Errors
Diagnostic information
```

### Outputs

```text
Log records
Diagnostic output
Execution-related log information
```

### Dependencies

```text
Execution
Logging infrastructure
Test / Domain components
```

### Boundary

Logging must remain separate from:

```text
Observation
Evidence
Result
```

A log record does not automatically constitute evidence.

### Implementation Status

```text
PARTIALLY IMPLEMENTED
```

The common `BaseSecurityTest` configures and uses Python logging, while `01_framework/logger.py` is documented as a structural placeholder. The current repository therefore contains logging functionality but not a complete common Phase-3 logging architecture.

---

## 12. Reporting

### Primary Responsibility

Reporting presents information derived from technical test execution and results.

### Inputs

```text
Test information
Execution information
Results
Available technical artifacts
```

### Outputs

```text
Report artifacts
JSON output
Markdown output
Other supported report representations
```

### Dependencies

```text
Test results
Existing report-generation component
Available test data
```

### Boundary

Reporting is downstream from technical test results.

It must not create:

```text
Unsupported Execution
Unsupported Observation
Unsupported Result
Unsupported Finding
```

### Implementation Status

```text
PARTIALLY IMPLEMENTED
```

The repository contains `report_generator.py` and report-generation functionality in domain-specific components. The complete common reporting boundary defined by Phase 3 is not established as a unified architecture.

---

## 13. Cross-Component Responsibility Boundaries

The responsibility separation is:

```text
Assessment Objective
    defines assessment purpose

Security Objective / Property
    defines relevant security property

Test Objective
    defines what the test determines

Test Case
    defines what is tested

Test Runner
    controls execution

Domain Adapter
    connects common test semantics to a domain

Domain Module
    performs domain-specific interaction

Target / Model
    represents the technical target or model

Execution
    performs the test activity

Observation
    represents actual execution-derived behaviour

Oracle
    defines evaluation criteria

Result
    represents the evaluated outcome

Evidence Boundary
    connects observation/execution to the later evidence layer

Logging
    records execution-related information

Reporting
    presents technical test information
```

No component shall silently assume the primary responsibility of another component.

---

## 14. Responsibility Separation Rules

The following boundaries are mandatory:

```text
Test Case
    !=
Test Runner
```

```text
Test Runner
    !=
Domain Adapter
```

```text
Domain Adapter
    !=
Domain Module
```

```text
Domain Module
    !=
Target / Model
```

```text
Expected Behaviour
    !=
Observation
```

```text
Observation
    !=
Result
```

```text
Result
    !=
Finding
```

```text
Observation
    !=
Evidence
```

```text
Logging
    !=
Evidence
```

```text
Result
    !=
Reporting
```

These boundaries establish the responsibility model without requiring every boundary to be implemented in the current repository.

---

## 15. Implementation Status Summary

| Component         | Status                    |
| ----------------- | ------------------------- |
| Test Case         | **PARTIALLY IMPLEMENTED** |
| Test Runner       | **NOT IMPLEMENTED**       |
| Domain Adapter    | **NOT IMPLEMENTED**       |
| Domain Module     | **IMPLEMENTED**           |
| Target / Model    | **PARTIALLY IMPLEMENTED** |
| Observation       | **PARTIALLY IMPLEMENTED** |
| Evidence Boundary | **DESIGNED**              |
| Result            | **PARTIALLY IMPLEMENTED** |
| Logging           | **PARTIALLY IMPLEMENTED** |
| Reporting         | **PARTIALLY IMPLEMENTED** |

The status describes implementation maturity only.

It does not imply:

```text
EXECUTED
OBSERVED
VERIFIED
```

---

## 16. Responsibility Model and Current Repository

The current repository provides domain-specific technical components and a basic common test base.

The documented architecture therefore currently has the following relationship:

```text
COMMON ARCHITECTURE
        |
        +-- Base Test Structure
        |
        +-- Logging / Reporting Support
        |
        v
DOMAIN-SPECIFIC IMPLEMENTATION
        |
        +-- CAN
        +-- UDS
        +-- Firmware
        +-- Ethernet
```

The following common architectural elements remain unimplemented:

```text
Common Test Runner
Common Domain Adapter
Unified Execution Interface
```

The following elements remain only partially represented:

```text
Common Test Case Model
Target / Model Boundary
Observation Boundary
Common Result Model
Common Logging Boundary
Common Reporting Boundary
```

The Evidence Boundary is architecturally defined but intentionally remains outside the Phase-3 implementation scope.

---

## 17. Relationship to Domain Separation

The responsibility model preserves the existing domain separation.

The domain modules are responsible for domain-specific technical interaction.

The common architecture is responsible for:

```text
Test Definition
Execution Organization
Common Semantics
Result Semantics
Traceability
Architectural Boundaries
```

The intended integration is:

```text
Common Test Case
        |
        v
Common Test Runner
        |
        v
Domain Adapter
        |
        +---- CAN
        +---- UDS
        +---- Firmware
        +---- Ethernet
        |
        v
Domain Module
        |
        v
Target / Model
```

The current repository does not yet implement the complete common integration path.

---

## 18. Reusability

The following responsibilities are intended to be reusable across domains:

```text
Test identification
Test metadata
Assessment objective
Security objective / property
Test objective
Preconditions
Inputs
Expected behaviour
Oracle
Execution lifecycle
Result semantics
Execution status
Logging boundary
Reporting boundary
```

Domain-specific technical interaction remains domain-specific.

This separation prevents common test semantics from being duplicated independently inside CAN, UDS, Firmware and Ethernet implementations.

---

## 19. Responsibility Model Status

```text
Test Responsibility Matrix
→ ESTABLISHED
```

The responsibility model establishes:

```text
Primary Responsibilities
Inputs
Outputs
Dependencies
Boundaries
Implementation Status
```

for the required common architecture components.

The matrix does not establish implementation of the components marked:

```text
NOT IMPLEMENTED
PARTIALLY IMPLEMENTED
DESIGNED
```

---

## 20. Scope Integrity

It does not implement:

```text
Evidence Framework
Core Security Test Cases
Extended Security Test Cases
Finding Lifecycle
Root-Cause Analysis
Regression Validation
CI/CD Automation
Professional Packaging
Final Assessment
Real ECU Validation
Vehicle Validation
```

The Evidence Boundary is defined only as an architectural interface to the later evidence layer.

---

## 21. Completion State

```text
Test Responsibility Matrix
    ESTABLISHED

Responsibility Separation
    ESTABLISHED

Domain Separation
    ESTABLISHED

Reusable Test Responsibilities
    ESTABLISHED

Current Implementation Status
    DOCUMENTED

Implementation
    NOT MODIFIED

Execution
    NOT RUN

Evidence
    NOT ESTABLISHED

Phase-3 Completion
    IN PROGRESS
```
