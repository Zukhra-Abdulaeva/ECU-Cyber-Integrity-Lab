# Assessment Objective Traceability Model

## 1. Purpose

The Assessment Objective Traceability Model defines how an Assessment Objective is connected to the security-test structure and to the resulting technical test result.

The model consolidates the traceability relationships already defined across the Security Test Architecture, Execution Interface, and Test Lifecycle definitions.

The model does not define additional test architecture components, execution mechanisms, lifecycle states, evidence framework functions, or finding lifecycle functions.

Traceability establishes the relationship between defined elements. It does not establish implementation, execution, observation, or verification status.

---

## 2. Traceability Model

The primary assessment-to-result traceability relationship is:

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
Result
```

The model connects the assessment objective to the technical test structure and its resulting test result.

The technical execution architecture between Test Case and Execution remains defined by the existing architecture:

```text
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
```

These components are part of the existing Security Test Architecture and are not redefined by this traceability model.

---

## 3. Traceability Relationships

The primary traceability relationships are:

| Source | Relationship | Target | Traceability Meaning |
|---|---|---|---|
| Assessment Objective | addresses | Security Objective / Property | Identifies the security objective or property relevant to the assessment objective. |
| Security Objective / Property | is evaluated by | Test Objective | Defines what the test is intended to determine with respect to the security objective or property. |
| Test Objective | is implemented by | Test Case | Connects the intended test determination to a concrete test definition. |
| Test Case | is executed through | Execution | Connects the defined test to its execution activity. |
| Execution | produces | Observation | Connects the execution activity to actual execution-derived information. |
| Observation | contributes to | Result | Connects observed behaviour to the evaluation that establishes the resulting test state. |

The relationships are traceability relationships and do not by themselves establish implementation or execution status.

---

## 4. Relationship Semantics

### 4.1 Assessment Objective to Security Objective / Property

An Assessment Objective identifies what is to be assessed.

The associated Security Objective / Property identifies the security-related objective or property addressed by the assessment.

```text
Assessment Objective
        |
        v
Security Objective / Property
```

The relationship establishes the security context for the subsequent test objective.

---

### 4.2 Security Objective / Property to Test Objective

The Test Objective defines what the security test is intended to determine with respect to the identified Security Objective / Property.

```text
Security Objective / Property
        |
        v
Test Objective
```

The relationship connects the assessment requirement to the intended technical test determination.

---

### 4.3 Test Objective to Test Case

The Test Case provides the concrete test definition associated with the Test Objective.

```text
Test Objective
        |
        v
Test Case
```

The Test Case may define, as applicable:

- Test ID
- Security Domain
- Assessment Objective
- Security Objective / Property
- Test Objective
- Preconditions
- Inputs
- Actions
- Expected Behaviour
- Oracle / Evaluation Criteria
- Validity Scope
- Target / Model

The Test Case structure is defined by the existing Security Test Architecture and Test Lifecycle definitions. This model only establishes its traceability relationship to the Test Objective.

---

### 4.4 Test Case to Execution

Execution connects the defined Test Case to an actual execution activity.

```text
Test Case
    |
    v
Execution
```

The relationship does not imply that a Test Case has been executed.

The following states remain distinct:

```text
Test Case defined
    !=
Test Case implemented
    !=
Test Case executed
```

Execution status is established independently through the execution architecture and lifecycle.

---

### 4.5 Execution to Observation

Observation represents actual information derived from execution.

```text
Execution
    |
    v
Observation
```

An Observation therefore requires an execution context from which the observed information originates.

The following distinction remains mandatory:

```text
Expected Behaviour
    !=
Actual Observation
```

Expected Behaviour is defined as part of the Test Case.

Actual Observation is derived from execution.

Expected Behaviour must not be copied or treated as an Actual Observation.

---

### 4.6 Observation to Result

The Result represents the evaluated outcome of the executed test.

The existing evaluation boundary is:

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

The traceability relationship can therefore be represented as:

```text
Observation
    |
    v
Evaluation
    |
    v
Result
```

Evaluation is not a separate assessment objective traceability level. It is the established mechanism through which the observed execution behaviour is evaluated against the applicable evaluation criteria before the Result is established.

The following distinctions remain mandatory:

```text
Observation != Result
Execution Completed != PASS
Execution Error != FAIL
```

A Result must not be manufactured from execution completion alone.

---

## 5. Result Traceability

The complete assessment-to-result relationship is:

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

The traceability model provides a continuous relationship from the assessment objective to the technical test result.

Traceability does not establish:

```text
Traceability != Implementation
Traceability != Execution
Traceability != Observation
Traceability != Verification
```

A complete traceability relationship may therefore exist while one or more technical elements remain designed, unimplemented, unexecuted, unobserved, or unverified.

The implementation and execution status of the individual elements remains governed by the existing architecture status model.

---

## 6. Evidence Boundary

Evidence is associated with the execution and observation context but is not part of the primary Assessment Objective to Result traceability chain.

The boundary is represented as:

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

The Evidence Boundary identifies where execution-derived information may become part of the evidence context.

Evidence is distinct from:

```text
Evidence != Observation
Evidence != Result
Evidence != Finding
```

This model does not define:

- evidence creation
- evidence validation
- evidence provenance
- evidence association
- evidence lifecycle management

These functions belong to the subsequent Evidence Framework scope.

The Evidence Boundary therefore identifies the relationship without introducing Evidence Framework implementation into the Security Test Architecture.

---

## 7. Finding Boundary

A Security Finding is not established directly by a Test Case, Execution, Observation, or Result.

The downstream relationship is represented as:

```text
Result
    |
    v
Evidence / Assessment
    |
    v
Finding
```

The relationship identifies the later connection between technical test results and assessment or finding activities.

```text
Result != Finding
```

A test Result does not automatically establish a Security Finding.

This model does not define:

- finding creation
- finding validation
- root-cause analysis
- risk treatment
- mitigation
- retest handling
- finding lifecycle management

The Finding Boundary therefore remains downstream of the Security Test Architecture and does not extend the  test traceability chain.

---

## 8. Traceability and Status Integrity

Traceability describes relationships between architecture and test elements.

It does not change the status of those elements.

The following distinctions remain applicable:

```text
DESIGNED
    !=
IMPLEMENTED
    !=
EXECUTED
    !=
OBSERVED
    !=
VERIFIED
```

A traceability relationship must therefore not be interpreted as evidence that the related element has been implemented, executed, observed, or verified.

Examples:

```text
Defined Test Case
    |
    v
Traceable Test Objective
```

does not establish:

```text
Test Case Executed
```

Similarly:

```text
Execution
    |
    v
Observation
```

defines the required relationship but does not establish that an execution or observation has actually occurred.

A Result may only be established according to the existing Result semantics defined by the Security Test Architecture and Test Lifecycle.

---

## 9. Architectural Outcome

The Assessment Objective Traceability Model consolidates the existing assessment-to-test relationships into one explicit traceability model.

The established relationship is:

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
Result
```

The model additionally establishes the downstream boundaries:

```text
Execution / Observation
        |
        +----> Evidence Boundary

Result
    |
    v
Evidence / Assessment
    |
    v
Finding
```

No additional Security Test Architecture component, execution mechanism, lifecycle state, Evidence Framework function, or Finding lifecycle function is introduced by this artifact.

The traceability model is therefore limited to consolidation and semantic clarification of the relationships already established by the existing Security Test Architecture.