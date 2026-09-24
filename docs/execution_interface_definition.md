# Execution Interface Definition

## 1. Purpose

The Execution Interface defines the common architectural interface between the Security Test Architecture and domain-specific test execution.

It provides a consistent execution structure across the supported security domains:

- CAN
- UDS
- Firmware
- Ethernet

The common execution interface defines:

- Initialization
- Preconditions
- Input
- Execution
- Observation
- Status
- Error Handling
- Result Handoff

The interface is an architecture definition. Its existence does not establish implementation or execution.

## 2. Architectural Position

```text
Security Test Case
  |
  v
Test Runner
  |
  v
Execution Interface
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

The Execution Interface provides the common execution contract between the Test Runner and domain-specific execution components.

Domain-specific implementation remains within the Domain Adapter and Domain Module.

## 3. Execution Lifecycle

The common execution sequence is:

```text
Test Definition
  |
  v
Initialization
  |
  v
Preconditions
  |
  v
Input
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
Result Handoff
```

Status applies across the execution lifecycle and does not constitute a separate sequential lifecycle step.

Error Handling applies across the execution lifecycle.

The lifecycle distinguishes design-time definitions from execution-time state and observations.

## 4. Initialization

Initialization prepares the execution context required for the test.

Responsibilities include:

- preparing the execution environment
- initializing required interfaces
- preparing required configuration
- establishing access to the Target / Model
- preparing required execution resources

Inputs include:

- Test Case
- Execution Context
- required configuration
- required resources

Outputs include:

- Initialization Status
- initialized execution context
- initialization errors where applicable

Initialization status may be represented as:

- `INITIALIZATION SUCCESSFUL`
- `INITIALIZATION FAILED`

Initialization status is not a Test Result.

## 5. Preconditions

Preconditions define conditions that must be satisfied before execution can meaningfully proceed.

Precondition inputs may include:

- Test Case Preconditions
- Target / Model State
- Execution Environment
- Required Resources

Precondition outputs include:

- Precondition Status
- Satisfied Preconditions
- Unsatisfied Preconditions
- Blocking Information

If a required precondition is not satisfied, the test is not represented as normal successful execution. Depending on the execution and result semantics, the test may result in `NOT_RUN` or `BLOCKED`.

## 6. Input

Input is the data, stimulus, action, or parameter supplied to the Target / Model, interface, or execution environment.

Input is traceable to the Test Objective and Security Test Case.

Examples include:

- CAN message
- UDS diagnostic request
- Firmware artifact
- Network scan parameter

The common Execution Interface defines the existence and handoff of input. Technical interpretation of the input remains domain-specific.

## 7. Execution

Execution performs the defined test activity under the established preconditions and execution context.

The common execution handoff is:

```text
Test Runner
  |
  v
Execution Interface
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

Execution inputs include:

- Initialized Context
- Satisfied Preconditions
- Prepared Input
- Target / Model
- Domain Execution Parameters

Execution outputs include:

- Execution Status
- Domain Output
- Observation Input
- Execution Errors
- Execution Completion State

The Execution Interface does not define domain-specific implementation. It defines the invocation and return of execution state.

## 8. Observation

Observation represents the actual behavior or output obtained from execution.

The architectural relationship is:

```text
Execution
  |
  v
Actual Observation
```

Observation inputs may include:

- Execution Output
- Target / Model Response
- Domain Module Output
- Technical Measurement
- Returned Data

Observation outputs include:

- Actual Observation
- Observation Status
- Observation Context

The Observation boundary separates:

- Expected Behaviour
- Test Input
- Oracle
- Result
- Evidence

The distinction between expected and observed behavior is mandatory:

`EXPECTED != OBSERVED`

No observation may be represented as execution-derived unless execution occurred.

## 9. Status

Status communicates the state of the execution lifecycle and is distinct from the final Test Result.

Execution status may include:

- `NOT_STARTED`
- `INITIALIZING`
- `READY`
- `RUNNING`
- `COMPLETED`
- `FAILED`
- `BLOCKED`

Status inputs include:

- Initialization State
- Precondition State
- Execution State
- Observation State
- Error State

Status outputs include:

- Execution Status
- Completion State
- Execution Condition

`Execution Status != Test Result`

`COMPLETED` does not mean `PASS`. A result requires actual observation and applicable evaluation criteria.

## 10. Error Handling

Error Handling covers technical conditions that prevent, interrupt, or affect execution.

Possible error sources include:

- Initialization
- Preconditions
- Input handling
- Domain interaction
- Target / Model access
- Execution
- Observation
- Infrastructure

Error handling inputs may include:

- errors
- exceptions
- unavailable resources
- failed interfaces
- execution interruptions

Outputs may include:

- error information
- execution status
- blocking information
- diagnostic information

The boundary is:

`Technical Execution Error != Security Finding`

An execution error must be interpreted in the context of the applicable test and evaluation criteria.

## 11. Result Handoff

Result Handoff transfers the information required for result evaluation from the execution architecture to the common Result model.

Result Handoff occurs after execution and observation are available where applicable.

The relationship is:

```text
Execution
  |
  v
Observation
  |
  v
Oracle / Evaluation
  |
  v
Result Handoff
```

Inputs include:

- Execution Status
- Actual Observation
- Oracle / Evaluation Criteria
- Test Case
- Execution Context
- Relevant Error Information

Outputs include:

- Result Input
- Execution Context
- Observation Reference
- Evaluation Context

Result Handoff does not manufacture a final result.

## 12. Result Evaluation Boundary

The Execution Interface ends before common Result semantics are redefined by a domain.

The evaluation relationship is:

```text
Actual Observation
+
Oracle / Evaluation Criteria
+
Execution Context
|
v
Result
```

Common Result states are:

- `PASS`
- `FAIL`
- `NOT_RUN`
- `INCONCLUSIVE`
- `BLOCKED`

Domain Modules must not redefine project-wide Result semantics.

## 13. Complete Interface Contract

The common interface contract is:

```text
INITIALIZATION
  |
  v
PRECONDITIONS
  |
  v
INPUT
  |
  v
EXECUTION
  |
  v
OBSERVATION
  |
  v
RESULT HANDOFF
```

Status applies across the lifecycle.

Error Handling is available across the lifecycle.

The architectural relationship is:

```text
Test Runner
  |
  v
Execution Interface
  |
  +--------------------> Execution Status
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
Result Handoff
```

## 14. Domain Integration

The common Execution Interface is domain-independent.

The same lifecycle is applied across:

- CAN
- UDS
- Firmware
- Ethernet

The domain-specific execution path may be represented as:

```text
Input
  |
  v
Domain Execution
  |
  v
Domain Observation
```

Domain meaning remains specific to the respective security domain. Lifecycle and common status/result boundaries remain shared.

## 15. Execution Context

The Execution Context identifies the technical context in which execution takes place.

Applicable context classifications include:

- `REAL`
- `VIRTUAL`
- `SIMULATED`
- `LOCAL`
- `STATIC`
- `SYNTHETIC`

Execution Context must not be promoted beyond the available evidence.

The following distinctions apply:

`VIRTUAL != REAL ECU VALIDATION`

`STATIC != RUNTIME EXECUTION`

`SYNTHETIC != OBSERVED REAL-WORLD INPUT`

## 16. Expected Behaviour and Observation

Expected Behaviour is defined by the Test Case.

Actual Observation is obtained from execution.

The relationship is:

```text
Test Case
  |
  v
Expected Behaviour

Execution
  |
  v
Actual Observation

Oracle
  |
  v
Result
```

Expected Behaviour must not be copied into Actual Observation.

An expected result must not be assigned as an actual result without the applicable execution, observation, and evaluation basis.

## 17. Execution and Result Semantics

The result relationship is:

`Execution Occurred + Actual Observation + Defined Oracle → Result`

The following distinctions apply:

`Execution Completed != PASS`

`Execution Error != FAIL`

An execution error does not establish `FAIL` without applicable technical evaluation.

## 18. Interface Responsibility Separation

| Component | Responsibility |
|---|---|
| Test Runner | lifecycle and execution flow |
| Execution Interface | common execution contract |
| Domain Adapter | translates and commonizes interaction between common semantics and domain execution |
| Domain Module | domain-specific interaction and processing |
| Target / Model | technical target or model |
| Observation | actual execution-derived behaviour |
| Oracle | evaluation criteria |
| Result | evaluated test outcome |

## 19. Current Repository Status

The current repository contains domain-specific execution capabilities and common test-base functionality, but the complete common Execution Interface is not implemented as a unified interface.

Current status:

- Execution Interface: `DESIGNED`
- Common Test Runner: `NOT IMPLEMENTED`
- Common Domain Adapter: `NOT IMPLEMENTED`
- Domain Modules: `IMPLEMENTED`
- Unified Execution Contract: `NOT IMPLEMENTED`

## 20. Implementation Boundary

The Execution Interface Definition does not require implementation as part of the architecture definition.

Implementation is a separate activity.

No execution result or execution evidence is generated by this artifact.

## 21. Traceability

The architectural traceability relationship is:

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
Test Runner
  |
  v
Execution Interface
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
Oracle / Evaluation
  |
  v
Result
```

The Evidence Boundary is downstream from execution and observation.

## 22. Architecture Integrity Rules

The following distinctions are mandatory:

- Initialization != Test Execution
- Fulfilled Preconditions != Test Result
- Input != Observation
- Execution Status != Test Result
- Execution Errors != automatically Security Findings
- Expected Behaviour != Actual Observation
- No `PASS` from completion alone
- No `FAIL` from execution failure alone without applicable evaluation
- Domain Modules cannot redefine common Result semantics
- Virtual / Simulated / Static / Synthetic != Real-World Validation
- Execution Interface Definition != Implementation Evidence

## 23. Architectural Outcome

The Execution Interface establishes a common execution contract across the supported security domains.

The contract includes:

- Initialization
- Preconditions
- Input
- Execution
- Observation
- Status
- Error Handling
- Result Handoff

It provides a common execution path while preserving domain-specific implementation.

## 24. Status

Current status:

- Execution Interface Definition: `ESTABLISHED`
- Architecture: `DEFINED`
- Implementation: `NOT IMPLEMENTED AS COMMON INTERFACE`
- Execution: `NOT RUN`
- Observation: `NOT ESTABLISHED`
- Evidence: `NOT ESTABLISHED`
- Verification: `PENDING REVIEW`