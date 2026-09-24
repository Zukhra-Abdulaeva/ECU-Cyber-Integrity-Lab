````text
# Test Lifecycle Definition

## 1. Purpose

The Test Lifecycle Definition defines the common sequence through which a security test progresses from a defined technical purpose to an evaluated result.

The common lifecycle is:

```text
Test Definition
  |
  v
Preconditions
  |
  v
Initialization
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
  |
  v
Reporting / Evidence Boundary
````

The lifecycle does not establish implementation, execution, observation, evidence, or verification.

## 2. Lifecycle States

### 2.1 Test Definition

The Test Definition contains the information required to define the technical purpose and evaluation basis of a security test.

It may include:

* Test ID
* Security Domain
* Assessment Objective
* Security Objective / Property
* Test Objective
* Target / Model
* Execution Context
* Inputs
* Expected Behaviour
* Evaluation Criterion

The Test Definition is design-time information. It does not represent an executed test.

### 2.2 Preconditions

Preconditions define conditions that must be satisfied before execution can meaningfully proceed.

They may include:

* Target / Model
* Execution Environment
* Configuration
* Inputs
* Interfaces
* Dependencies
* Initial State

Preconditions are evaluated before execution.

If a required precondition is not satisfied, execution is not represented as successfully completed. The applicable execution and result semantics determine the resulting state.

### 2.3 Initialization

Initialization prepares the context required for test execution.

It may include:

* environment setup
* Target / Model access
* domain interface initialization
* required configuration
* input preparation
* execution context initialization

Initialization belongs to the execution lifecycle.

Successful initialization does not constitute a test result. Initialization failure remains distinguishable from a security-test failure.

### 2.4 Execution

Execution performs the defined test activity against the applicable Target / Model.

Execution is controlled by the common execution architecture and domain-specific implementation.

The following distinctions apply:

`Test Definition != Execution`

`Expected Behaviour != Actual Observation`

`Execution Status != Test Result`

Applicable Execution Context classifications include:

* `REAL`
* `VIRTUAL`
* `SIMULATED`
* `LOCAL`
* `STATIC`
* `SYNTHETIC`

### 2.5 Observation

Observation represents actual behavior or output obtained from execution.

The relationship is:

```text
Execution
  |
  v
Actual Observation
```

Expected Behaviour must not substitute for Actual Observation.

Execution without an established observation does not automatically establish a successful result.

### 2.6 Evaluation

Evaluation determines whether the actual observation satisfies the defined evaluation criterion.

The evaluation uses an Oracle or equivalent evaluation criteria.

The relationship is:

```text
Actual Observation
+
Evaluation Criterion
|
v
Evaluation Outcome
```

Evaluation is distinct from:

* Expected Behaviour
* Observation
* Result
* Security Finding

A Result cannot be established from an undefined evaluation criterion.

### 2.7 Result

The Result represents the evaluated outcome of the security test.

Common Result states are:

* `PASS`
* `FAIL`
* `NOT_RUN`
* `INCONCLUSIVE`
* `BLOCKED`

The Result is determined from the applicable execution state, actual observation, and defined evaluation criteria.

`PASS` requires sufficient execution, observation, and evaluation support.

`FAIL` requires execution and observation showing that the applicable criterion was not satisfied.

`NOT_RUN` applies when the test was not executed.

`INCONCLUSIVE` applies when execution or observations are insufficient for reliable evaluation.

`BLOCKED` applies when a prerequisite prevents meaningful execution or evaluation.

No Result is established merely from test definition or implementation.

### 2.8 Reporting / Evidence Boundary

After Result determination, information may be transferred to downstream reporting and evidence handling.

The lifecycle ends at the downstream boundary:

```text
Result
  |
  v
Reporting / Evidence Boundary
```

Reporting presents established results.

The Evidence Boundary identifies the downstream evidence capability.

Detailed evidence creation, validation, provenance, association, storage, and lifecycle management belong to the Evidence Framework and are not implemented by the Test Lifecycle Definition.

Reporting cannot create unsupported claims.

## 3. Design-Time and Execution-Time Separation

Design-time information includes:

* Test Definition
* Preconditions
* Expected Behaviour
* Evaluation Criterion
* Target / Model Definition
* Execution Procedure

Execution-time information includes:

* Initialization Status
* Execution Status
* Actual Observation
* Evaluation Outcome
* Result

The distinction between design-time and execution-time information is mandatory.

Implementation does not establish observation.

Observation does not automatically establish a verified security conclusion.

## 4. Lifecycle Responsibility

The lifecycle responsibilities are:

| Component           | Responsibility                                                              |
| ------------------- | --------------------------------------------------------------------------- |
| Test Case           | defines the test and evaluation basis                                       |
| Test Runner         | controls lifecycle and execution flow                                       |
| Domain Adapter      | connects common semantics to domain-specific execution                      |
| Domain Module       | performs domain-specific interaction and processing                         |
| Target / Model      | represents the technical object or environment                              |
| Observation         | represents execution-derived information                                    |
| Evaluation / Oracle | determines criterion satisfaction                                           |
| Result              | represents the evaluated outcome                                            |
| Reporting           | presents results                                                            |
| Evidence Boundary   | separates execution and result handling from downstream evidence management |

The lifecycle does not require every responsibility to be implemented by a common software component.

## 5. Lifecycle Failure Boundaries

Failures are attributable to the applicable lifecycle stage.

Relevant conditions include:

* Precondition failure
* Initialization failure
* Execution failure
* Observation unavailable
* Evaluation inconclusive
* Test result

Infrastructure, initialization, or execution failure does not automatically mean a security-test failure.

A technical test failure does not itself establish a confirmed security finding.

## 6. Traceability

The primary lifecycle traceability relationship is:

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
Test Definition
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
  |
  v
Reporting / Evidence Boundary
```

The downstream relationship is maintained separately:

```text
Result
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

The downstream relationship must not be collapsed into the test lifecycle itself.

## 7. Architecture Status

Current status:

* Lifecycle Architecture: `ESTABLISHED`
* Common Lifecycle Definition: `DESIGNED`
* Common Lifecycle Implementation: `NOT ESTABLISHED`
* Lifecycle Execution: `NOT RUN`
* Lifecycle Observation: `NOT ESTABLISHED`
* Lifecycle Evidence: `NOT ESTABLISHED`
* Lifecycle Verification: `ARCHITECTURE REVIEW`
