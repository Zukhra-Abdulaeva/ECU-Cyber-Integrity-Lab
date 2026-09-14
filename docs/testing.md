# Testing

## 1. Purpose

This document defines the testing model, test semantics, evidence handling, result interpretation, reproducibility requirements, and validity boundaries for the ECU-Cyber-Integrity-Lab.

The purpose is to provide a consistent basis for designing, executing, assessing, and documenting security tests.

Testing is understood as an engineering process:

```text
Security Requirement
→ Threat / Attack Hypothesis
→ Security Test
→ Controlled Execution
→ Observation
→ Evidence
→ Result
→ Assessment
→ Finding
→ Retest
→ Regression
```

This model defines the intended testing and assessment approach. It does not by itself establish that every described test component, execution path, evidence mechanism, regression mechanism, or CI/CD integration is implemented.

---

## 2. Assessment Context

Every security test is evaluated in a defined technical context.

The context describes where and how the test is performed and determines the validity of the resulting observation and evidence.

Relevant context classifications include:

```text
REAL
VIRTUAL
SIMULATED
LOCAL
STATIC
SYNTHETIC
```

The classification is part of the test result and evidence interpretation.

A result obtained in a simulated or virtual environment must not be presented as evidence of behaviour in a real ECU or vehicle environment.

The assessment context therefore remains separate from the security objective itself.

---

## 3. Security Test Model

A security test connects a security objective with a defined test action, an expected behaviour, an observable result, and an assessment.

The conceptual test flow is:

```text
Security Objective
→ Asset
→ Threat
→ Attack Surface
→ Attack Hypothesis
→ Preconditions
→ Test Input / Action
→ Expected Behaviour
→ Security Oracle
→ Test Execution
→ Actual Observation
→ Evidence
→ Result
→ Assessment
```

A security test should be sufficiently defined to answer:

* What security property is being evaluated?
* Which asset or component is involved?
* Which threat or attack hypothesis is being tested?
* Which attack surface is used?
* Under which preconditions is the test valid?
* Which input or action is performed?
* What behaviour is expected?
* How is the expected behaviour evaluated?
* What was actually observed?
* Which evidence supports the observation?
* What result follows from the observation?

The model does not imply that every test architecture component is already implemented.

---

## 4. Security Objective and Test Objective

The **Security Objective** describes the security property or protection goal that is relevant to the assessment.

The **Test Objective** describes what the individual test is intended to determine.

The two should remain distinguishable.

A test objective may, for example, evaluate whether a defined security control behaves according to an expected security property under specified conditions.

The test objective does not constitute a finding or a successful security assessment by itself.

---

## 5. Security Test Preconditions

Test preconditions define the conditions required before execution.

Relevant preconditions may include:

* required target or model state
* required communication state
* required configuration
* required input data
* required software or test environment
* required permissions or access conditions
* required initial state

Preconditions must be known before interpreting an execution result.

If required preconditions are not fulfilled, the resulting test state must not be interpreted as a normal successful execution.

---

## 6. Test Input and Action

The test input defines what is provided to the target, model, interface, or test environment.

The test action defines what the test performs.

Depending on the security-test domain, this may involve:

```text
CAN
UDS
Firmware
Ethernet
Bootloader / OTA
```

The input and action must remain traceable to the corresponding test objective and attack hypothesis.

---

## 7. Expected Behavior

Expected behaviour defines the behaviour against which the actual observation is evaluated.

Expected behaviour is not an observation.

It represents the defined expectation before or independently of the concrete execution result.

The following distinction is mandatory:

```text
EXPECTED ≠ OBSERVED
```

An expected secure response must therefore not be documented as if it had already been observed.

---

## 8. Security Oracle

The security oracle defines the criteria used to determine whether the observed behaviour satisfies the test objective.

The oracle must be sufficiently defined to support a result decision.

Conceptually:

```text
Expected Behaviour
        +
Security Oracle
        +
Actual Observation
        ↓
Test Result
```

A test result must not be inferred solely from the existence of a test case or from its expected behaviour.

---

## 9. Test Execution

Test execution is the actual performance of the defined test action under the documented preconditions and assessment context.

The following technical states must remain separate:

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

---

## 10. Actual Observation

Actual observation records what occurred during an execution.

Observation must be distinguished from:

* expected behaviour
* test design
* assumptions
* hypotheses
* synthetic examples
* planned results

The observation is the basis for interpreting the execution result.

If no actual execution took place, there is no executed observation to document as an execution result.

---

## 11. Evidence

Evidence supports the traceability of a test execution and its resulting observation.

Evidence should allow the relevant result to be connected to:

```text
Test Case
→ Execution
→ Observation
→ Evidence
→ Result
```

Evidence is separate from examples and reports.

### 11.1 Evidence Types

The following evidence classifications are used:

```text
SYNTHETIC
SIMULATED
EXECUTED
```

**SYNTHETIC** evidence represents constructed or generated material that does not document an actual execution.

**SIMULATED** evidence represents output produced in a simulated or virtual execution context.

**EXECUTED** evidence represents evidence originating from an actual execution of the corresponding test.

The classification must remain visible when evidence is used for assessment.

Synthetic or simulated material must not be presented as real-world execution evidence.

---

## 12. Evidence Lifecycle

Evidence follows a defined conceptual lifecycle:

```text
CREATED
→ VALIDATED
→ ASSOCIATED
→ ACTIVE
→ SUPERSEDED
→ ARCHIVED
```

The lifecycle describes how evidence can be created, checked, associated with the relevant test context, used for assessment, replaced, and retained historically.

Lifecycle terminology does not by itself establish that an evidence-management implementation exists.

---

## 13. Test Result Model

Test results use explicit result states.

```text
PASS
FAIL
NOT_RUN
INCONCLUSIVE
BLOCKED
```

The result describes the outcome of the test under its actual execution and evidence conditions.

### 13.1 PASS

`PASS` requires:

* actual test execution
* fulfilled test expectation according to the security oracle
* traceable actual observation
* supporting evidence

A designed or planned test cannot be marked `PASS` without actual execution.

### 13.2 FAIL

`FAIL` indicates that an executed test did not satisfy the defined expected behaviour or security oracle.

The result must be supported by the corresponding observation and evidence.

A `FAIL` result must not be inferred solely from a security hypothesis.

### 13.3 NOT_RUN

`NOT_RUN` indicates that the test was defined but not executed.

It must not be interpreted as `PASS` or `FAIL`.

### 13.4 INCONCLUSIVE

`INCONCLUSIVE` indicates that execution or available evidence does not provide a sufficiently clear basis for a definitive `PASS` or `FAIL`.

### 13.5 BLOCKED

`BLOCKED` indicates that execution could not be performed because a required condition, dependency, environment, target, or other prerequisite was unavailable or prevented execution.

---

## 14. Result Semantics

The following distinctions are mandatory:

```text
DESIGNED ≠ IMPLEMENTED
IMPLEMENTED ≠ EXECUTED
EXECUTED ≠ VERIFIED

EXPECTED ≠ OBSERVED

SIMULATED ≠ REAL

ONE TEST ≠ SECURITY VALIDATED
```

A test result therefore always requires interpretation in the context of its execution state, evidence, and validity scope.

A test case description alone does not establish an execution result.

A single successful test does not establish comprehensive security validation.

---

## 15. Reproducibility

A security test should be reproducible to the extent permitted by its execution environment.

Relevant information includes:

* test identifier
* preconditions
* environment
* test input
* execution method
* expected behaviour
* security oracle
* evidence
* result
* cleanup requirements
* validity scope

Reproducibility requires that the relevant execution conditions are sufficiently documented to repeat or assess the test.

---

## 16. Validity Scope

A result is valid only within the context supported by its execution and evidence.

The validity scope must therefore distinguish, where applicable:

```text
Virtual
Simulated
Local
Static
Synthetic
Real ECU / Vehicle
```

Evidence generated in one context must not automatically be generalized to another context.

In particular:

```text
Virtual / Simulated Execution
≠
Real ECU / Vehicle Validation
```

Real-world automotive validation requires corresponding real-world evidence.

---

## 17. Simulation and Real-World Boundary

The project may use virtual, simulated, local, static, or synthetic contexts for reproducible security engineering.

Such contexts are valid for the scope they actually represent.

They do not establish real vehicle or ECU validation.

No simulated ECU behaviour, virtual CAN communication, static analysis result, or synthetic evidence may be represented as observed behaviour from a real vehicle or ECU without corresponding evidence.

---

## 18. Negative and Boundary Testing

Security testing includes negative and boundary conditions where relevant to the test objective.

Examples of test conditions may include:

* invalid input
* unexpected input
* boundary values
* incorrect sequencing
* unavailable prerequisites
* rejected access conditions

The expected security behaviour must be defined before interpreting the resulting observation.

Negative testing does not automatically imply that a vulnerability exists.

---

## 19. Test-to-Finding Relationship

A finding must be traceable to sufficient technical evidence.

The conceptual relationship is:

```text
Test
→ Execution
→ Observation
→ Evidence
→ Result
→ Assessment
→ Finding
```

A security hypothesis is not itself a confirmed finding.

Where evidence is insufficient to support a finding, the result must remain appropriately qualified rather than being presented as confirmed.

---

## 20. Retest and Regression

A retest evaluates whether a previously assessed condition has changed after remediation or another relevant change.

The conceptual relationship is:

```text
Finding
→ Remediation
→ Retest
→ Result
→ Regression Assessment
```

Regression testing extends this principle to relevant future changes.

Regression identifiers and automated regression mechanisms must only be treated as implemented where the corresponding implementation and execution are established.

---

## 21. Domain Coverage

The testing model covers the following security-test domains:

```text
CAN
UDS
Firmware
Ethernet
Bootloader / OTA
```

The common testing model provides consistent terminology and result semantics across these domains.

Domain-specific execution remains dependent on the respective target, model, adapter, tooling, and available evidence.

---

## 22. Test Architecture Scope

The common test architecture is defined conceptually as:

```text
Security Test Case
→ Test Runner
→ Domain Adapter
→ Domain Module
→ Target / Model
→ Observation
→ Evidence
→ Result
```

The responsibilities are separated conceptually:

```text
Test Case
    defines what is tested

Test Runner
    controls test execution

Domain Adapter
    connects the common test model to a domain

Domain Module
    provides domain-specific interaction

Target / Model
    provides the system or modeled target under test

Observation
    records the actual execution outcome

Evidence
    supports traceability of the observation

Result
    represents the assessed test outcome
```

This architecture describes the testing model and separation of responsibilities. It must not be interpreted as proof that every component is implemented.

---

## 23. Verification and Test Quality

A security test is technically meaningful when its purpose, preconditions, action, expected behaviour, oracle, observation, evidence, result, and validity scope can be traced.

Test quality therefore depends on more than the existence of test code.

The relevant chain is:

```text
Purpose
→ Preconditions
→ Action
→ Expected Behaviour
→ Oracle
→ Execution
→ Observation
→ Evidence
→ Result
```

Missing or unclear elements reduce the ability to make a defensible assessment.

A documented test design is not equivalent to a verified execution.

---

## 24. Current Documentation Scope

This document defines the testing model and the semantics used for test execution and assessment.

The actual implementation and execution state of the testing components must be established from the repository and corresponding evidence.

Conceptual test architecture, evidence handling, regression, and CI/CD integration must not be interpreted as implemented solely because they are described here.

Current implementation, execution, evidence, and verification states are maintained separately from this testing model.

---

## 25. Core Testing Principles

The testing approach follows these principles:

1. Every test has a defined purpose.
2. Security objectives and test objectives remain traceable.
3. Preconditions are defined before execution.
4. Expected behaviour is separated from actual observation.
5. A security oracle provides the basis for result interpretation.
6. Test execution is distinguished from test design.
7. Evidence is distinguished from examples and reports.
8. Evidence is classified according to its origin and execution context.
9. PASS requires actual execution and supporting evidence.
10. Test results use explicit and distinguishable result states.
11. Simulation is not represented as real-world validation.
12. Findings require sufficient technical evidence.
13. Retests are connected to the original finding and remediation context.
14. Regression is treated separately from the original test execution.
15. Reproducibility and validity scope are part of the assessment.
16. Planned architecture is not presented as implemented functionality.

The central principle is:

```text
A security test is only as strong as the traceable connection between
its objective, execution, observation, evidence, and result.
```
