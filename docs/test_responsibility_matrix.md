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

`IMPLEMENTED` does not imply execution or verification. Status labels describe the specific component and scope in the current repository snapshot; they must not be interpreted as claims of complete end-to-end integration or real ECU / vehicle validation.

---

## 2. Responsibility Matrix

| Component             | Primary Responsibility                                                                                                                  | Inputs                                                                                                                                                                              | Outputs                                                                | Dependencies                                                                        | Boundary                                                                       | Implementation Status     |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------- |
| **Test Case**         | Defines what is tested and establishes the test-specific objectives, preconditions, inputs, expected behaviour and evaluation criteria. | Test ID, name, security domain, assessment objective, security objective/property, test objective, preconditions, inputs, actions, expected behaviour, oracle, target/model context | Defined test specification and executable test intent                  | Assessment Objective, Security Objective / Property, Test Objective, Target / Model | Separates test definition from execution and observation                       | **PARTIALLY IMPLEMENTED** |
| **Test Runner**       | Coordinates one already-selected adapter operation and returns a common execution outcome. Full test selection and end-to-end lifecycle orchestration are not established. | Selected adapter operation, execution inputs, context | ExecutionOutcome, execution status, observations, errors | Execution Interface, Domain Adapter | Separates single-operation coordination from domain-specific interaction and later evaluation | **PARTIALLY IMPLEMENTED** |
| **Domain Adapter**    | Defines a common adapter contract and connects a selected operation to domain-specific execution. | Execution inputs, target/model context, domain parameters | Domain output and normalized observations | Execution Interface, Domain Module | Boundary between common architecture and domain-specific technical interaction | **IMPLEMENTED**           |
| **Domain Module**     | Performs domain-specific technical interaction or processing.                                                                           | Domain-specific inputs, target/model, protocol or analysis parameters                                                                                                               | Domain-specific execution output and observations                      | Domain technology, target/model, domain-specific libraries/interfaces               | Keeps CAN, UDS, Firmware and Ethernet interaction within their domains         | **IMPLEMENTED**           |
| **Target / Model**    | Represents the technical object, environment or artifact against which a test operates. | Target configuration, model data, local artifacts, virtual/simulated interfaces | Target/model access and technical interaction context | Execution environment, domain module | Separates the test architecture from the technical target/model | **PARTIALLY IMPLEMENTED** |
| **Observation**       | Represents raw or normalized output obtained from an execution operation. | Execution output, target response, measured or returned technical data | Common Observation objects and domain outputs | Execution Interface, Domain Adapter, Domain Module | Separates actual execution-derived behaviour from expected behaviour | **IMPLEMENTED** for the common model; domain-wide integration remains partial |
| **Evidence Boundary** | Defines how execution/observation information can be represented and validated as evidence. | Observation, execution metadata, relevant technical artifacts | Evidence records, artifact references, validation and repository operations | Execution/observation data, Evidence Framework | Separates evidence lifecycle management from execution; automatic creation for every domain run is not established | **IMPLEMENTED** in the Phase-4 framework; automatic domain integration remains partial |
| **Result**            | Represents the evaluated outcome of a test based on execution, observation and defined evaluation criteria. | Execution state, observation, oracle/evaluation criteria | Common TestResult model and result states | Execution, Observation, Oracle | Separates evaluation outcome from test definition and raw observation; runner does not assign PASS/FAIL automatically | **PARTIALLY IMPLEMENTED** |
| **Logging**           | Records execution-related information, diagnostics, warnings, errors and lifecycle information without replacing test semantics. | Execution events, diagnostics, warnings, errors | Log records | Common logging boundary and Python logging | Separates execution logging from observation, evidence and result semantics | **PARTIALLY IMPLEMENTED** |
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
PARTIALLY IMPLEMENTED
```

`a_framework/runner.py` implements `TestRunner` coordination for one already-selected adapter operation through the common execution interface. It returns an `ExecutionOutcome`; it does not implement complete test selection/scheduling, automatic oracle evaluation, final PASS/FAIL assignment, or automatic evidence creation. Therefore the single-operation runner is implemented, while the full responsibility described above is only partially implemented.

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
IMPLEMENTED
```

The repository contains the common abstract contract in `a_framework/domain_adapter.py` and domain-specific adapters under `b_security_tests/*/adapter.py`. This establishes the adapter boundary. It does not by itself prove that every domain operation is orchestrated through one complete end-to-end runner path.

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

The repository contains domain-specific implementation for CAN, UDS, Firmware and Automotive Ethernet. Local tests cover CAN, UDS and Firmware behavior using controlled inputs/test doubles. The Ethernet scanner implementation exists, but the snapshot's `b_security_tests/ethernet_tests/test_ethernet_scan.py` contains no `test_*` functions. Domain implementation and local tests do not establish real ECU / vehicle validation or complete end-to-end integration.

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

The shared architecture defines `ExecutionContext`, and domain code can operate on local artifacts, virtual interfaces, or synthetic/test-double inputs. A general target/model abstraction for real ECU and vehicle execution is not established. Context must be described according to the actual evidence available.

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

The shared `Observation` model and `ExecutionOutcome` are implemented, and the execution interface returns normalized observations for a selected adapter operation. Integration across all domain paths and automatic downstream evaluation remain partial. Synthetic/test-double observations must not be described as real-target observations.

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
IMPLEMENTED WITH INTEGRATION LIMITS
```

The Phase-4 Evidence Framework is implemented in `a_framework/evidence.py`, with validation, artifact integrity checks, lifecycle handling, and JSON-backed repository operations. Evidence framework tests exist in `a_framework/test_evidence.py`. This does not mean every domain execution automatically creates and associates an evidence record; that integration is not established as a universal path.

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

The repository contains common result/status data models in `a_framework/test_architecture.py`, including `TestResult` and result states. However, `TestRunner` returns `ExecutionOutcome` and does not itself apply the oracle or assign a final PASS/FAIL result. The common result model exists; automatic project-wide evaluation orchestration remains partial.

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

`a_framework/logging_boundary.py` provides the common logging functions, and domain/base-test code also uses Python logging. `a_framework/logger.py` remains a structural placeholder. The logging boundary is implemented, but a complete centrally configured logging architecture is not established.

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

The repository contains `a_framework/report_generator.py` and domain-specific export functions. The report generator consolidates existing JSON inputs, but end-to-end integration from `ExecutionOutcome` through evaluation, evidence, and final reporting is not established. Existing report-generation code does not prove that all report artifacts are current or generated by a verified integrated run.

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

| Component | Current status | Scope / limitation |
| --- | --- | --- |
| Test Case | **PARTIALLY IMPLEMENTED** | Common and domain-specific test structures exist; a complete unified test-case catalog/model is not established. |
| Test Runner | **PARTIALLY IMPLEMENTED** | Coordinates one selected adapter operation; no full scheduling or automatic evaluation. |
| Domain Adapter | **IMPLEMENTED** | Common contract and domain adapter implementations exist; end-to-end routing is not universal. |
| Domain Module | **IMPLEMENTED** | CAN, UDS, Firmware and Ethernet functionality exists within documented domain-specific limits. |
| Target / Model | **PARTIALLY IMPLEMENTED** | Local, static, virtual and synthetic contexts exist; real ECU/vehicle target integration is not established. |
| Observation | **IMPLEMENTED** | Common observation model and execution outcome exist; downstream evaluation integration is partial. |
| Evidence Boundary / Framework | **IMPLEMENTED WITH INTEGRATION LIMITS** | Evidence record validation and repository exist; automatic record creation for every domain execution is not established. |
| Result | **PARTIALLY IMPLEMENTED** | Common result data model exists; runner does not automatically assign final PASS/FAIL. |
| Logging | **PARTIALLY IMPLEMENTED** | Common logging boundary exists; `a_framework/logger.py` remains a placeholder. |
| Reporting | **PARTIALLY IMPLEMENTED** | Report generation code exists; complete execution-to-report integration is not established. |

```text
LOCAL TEST EXECUTION
REPORTED SUCCESSFUL FOR PHASE 5

REAL ECU / VEHICLE VALIDATION
NOT ESTABLISHED

UNIVERSAL END-TO-END INTEGRATION
NOT ESTABLISHED
```

---

## 16. Responsibility Model and Current Repository

The current repository contains shared framework components alongside domain-specific technical components. The architecture is implemented in part, but the full path is not automatically orchestrated end to end.

```text
Common Test / Execution Models
        |
        +-- TestRunner
        |      -> coordinates one selected adapter operation
        |
        +-- ExecutionInterface / AdapterExecutionInterface
        |      -> returns ExecutionOutcome and observations
        |
        +-- DomainAdapter contract
        |
        +-- Evidence Framework
        |      -> validates and stores explicitly created records
        |
        +-- In-memory Traceability Registry
        |
        +-- Common Logging Boundary
        |
        v
Domain-Specific Implementation
        +-- CAN
        +-- UDS
        +-- Firmware
        +-- Automotive Ethernet
```

Current boundaries and limitations:

- The common `TestRunner`, execution interface, and adapter contract exist.
- The runner handles a selected operation; it does not provide a full test scheduler or automatic PASS/FAIL evaluation.
- `ExecutionOutcome` is execution-level output, not a final `TestResult`.
- The common Evidence Framework can validate and persist evidence records, but domain execution does not universally create them automatically.
- Traceability is an in-memory relationship index, not a persistent project-wide traceability database.
- `a_framework/config.py` and `a_framework/logger.py` remain structural placeholders.
- The report generator exists, but end-to-end execution-to-result-to-evidence-to-report integration is not established.
- Local tests and synthetic/test-double executions do not establish real ECU or vehicle validation.

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

Phase 5 covers the core security-test implementation and local test execution reported as successful. The following capabilities remain outside the established current implementation state or are not verified as complete:

```text
Extended Security Test Cases
Finding Lifecycle and Root-Cause Analysis
Integrated automatic evidence creation for every domain execution
End-to-end result / evidence / reporting orchestration
Regression Validation
CI/CD Automation
Professional Packaging
Final Assessment
Real ECU Validation
Vehicle Validation
```

The Evidence Framework itself is implemented; the limitation is its universal integration with every domain execution, not the absence of the framework. Phase-5 local test success must not be interpreted as a security finding, physical ECU validation, or completion of later phases.

---

## 21. Completion State

```text
Test Responsibility Matrix
    ESTABLISHED

Responsibility Separation
    ESTABLISHED

Common Execution Interface / Adapter Contract
    IMPLEMENTED

Single-Operation Test Runner
    IMPLEMENTED

Phase-5 Local Test Execution
    REPORTED SUCCESSFUL

Evidence Framework
    IMPLEMENTED; DOMAIN-WIDE AUTOMATIC INTEGRATION NOT ESTABLISHED

End-to-End Evaluation / Evidence / Reporting
    NOT ESTABLISHED

Regression / CI/CD
    NOT IMPLEMENTED AS COMPLETE PROJECT CAPABILITIES

Real ECU / Vehicle Validation
    NOT ESTABLISHED
```

The Phase-5 execution status reflects the project status reported by the user. This document does not assert an aggregate test count or invent a run identifier. The detailed code-to-architecture mapping and snapshot-based verification limits are maintained in [`system_implementation_reference.md`](system_implementation_reference.md).

## Implementation Alignment

The shared framework currently includes `TestRunner`, `DomainAdapter`, `ExecutionInterface`/`AdapterExecutionInterface`, shared data models, the Evidence Framework, an in-memory traceability registry, and a logging boundary. The runner executes one already-selected adapter operation and returns `ExecutionOutcome`; final evaluation and automatic evidence creation are not performed by that runner. `a_framework/config.py` and `a_framework/logger.py` are structural placeholders in the repository snapshot, while `a_framework/logging_boundary.py` provides the common logging functions. For file-level detail and verification boundaries, see [`system_implementation_reference.md`](system_implementation_reference.md).
