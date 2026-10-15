# System Implementation Reference

## 1. Purpose and scope

This document describes the implementation represented by the repository snapshot and maps concrete files to their technical responsibilities. It complements, rather than replaces, the architecture definition, execution-interface definition, lifecycle definition, evidence definition, traceability model, and responsibility matrices.

The source of truth for implementation statements is the code and tests in the repository. Architecture documents describe intended structure; they are not evidence that a component executes successfully.

## 2. Status semantics

Use these terms consistently:

- **Present**: a file or artifact exists in the repository snapshot.
- **Implemented**: the file contains executable logic for the stated responsibility.
- **Integrated**: a component is connected to another component through code, not merely described or placed beside it.
- **Executed**: a run is evidenced by an execution record or reproducible command output.
- **Verified**: a defined verification procedure and its result support the claim.
- **End-to-end verified**: the complete path, including the relevant domain operation, observation, evaluation/result, evidence association, and report where applicable, has been exercised and checked.

These states are not interchangeable. A test file containing only `assert True`, a placeholder file, sample output, or an existing report artifact does not establish domain validation or end-to-end verification.

## 3. Repository structure

| Path | Responsibility | Current interpretation |
|---|---|---|
| `a_framework/` | Shared framework models, execution, adapters, evidence, traceability, logging, and reporting | Contains both implemented components and explicit placeholders; see component map below. |
| `b_security_tests/can_tests/` | CAN domain module, adapter, and domain tests | Concrete domain-specific structure exists; domain behavior and common-framework end-to-end coverage must be assessed separately. |
| `b_security_tests/uds_tests/` | UDS domain module, adapter, and domain tests | Concrete module/adapter files exist; the listed pytest test is a placeholder. |
| `b_security_tests/ethernet_tests/` | Ethernet domain module, adapter, and domain tests | Concrete module/adapter files exist; the listed pytest test is a placeholder. |
| `b_security_tests/firmware_tests/` | Firmware domain module, adapter, and domain tests | Concrete module/adapter files exist; the listed pytest test is a placeholder. |
| `c_evidence/` | Domain artifacts and framework-verification records | Existing artifacts do not automatically prove common execution provenance or complete traceability. |
| `d_examples/` | Example threat, firmware, risk, and UDS material | Examples, not by themselves verified assessment outcomes. |
| `e_security_reports/` | Assessment/report artifacts | The snapshot identifies generated report artifacts as incomplete, placeholder, inconsistent, or not end-to-end verified. |
| `docs/` | Architecture, lifecycle, evidence, traceability, environment, testing, and project-state documentation | Specialized documents remain authoritative for their respective subjects. |

## 4. Shared framework implementation

### 4.1 `a_framework/test_architecture.py`

Defines shared data models and status semantics, including `ExecutionStatus`, `TestCase`, `ExecutionContext`, `Observation`, `TestResult`, and `ExecutionRecord`. It imports `ContextClassification` and `ResultStatus` from `a_framework.evidence`.

`ExecutionStatus` describes execution progress (`NOT_STARTED`, `INITIALIZED`, `RUNNING`, `COMPLETED`, `FAILED`, `BLOCKED`, `CANCELLED`). It is distinct from `ResultStatus`, which represents an evaluated test outcome (`PASS`, `FAIL`, `NOT_RUN`, `INCONCLUSIVE`, `BLOCKED`). Do not conflate execution completion with a PASS result.

### 4.2 `a_framework/domain_adapter.py`

Defines the abstract `DomainAdapter` boundary. Concrete adapters implement `execute(inputs)` and `get_observation(execution_output)`. The base class tracks adapter status and provides a `run()` wrapper that changes status and propagates execution exceptions. Evaluation and evidence creation are outside this class.

### 4.3 `a_framework/execution.py`

Defines `ExecutionInterface`, `AdapterExecutionInterface`, and the frozen `ExecutionOutcome` data object. The interface runs an adapter and obtains normalized observations. `ExecutionOutcome` carries execution status, observations, timestamps, optional error information, and metadata. It represents an execution outcome before evaluation; it is not a `TestResult` and does not itself assign PASS/FAIL.

### 4.4 `a_framework/runner.py`

`TestRunner` accepts an already selected `DomainAdapter` and input mapping, delegates to an `ExecutionInterface` (defaulting to `AdapterExecutionInterface`), and returns `ExecutionOutcome`. Its own docstring explicitly leaves test evaluation and Phase-4 evidence handling outside the runner. Do not describe this class as a scheduler, multi-test orchestrator, evaluator, or evidence producer unless those responsibilities are implemented elsewhere.

### 4.5 `a_framework/evidence.py`

Defines evidence-related enums, records, validation and repository behavior. The model includes `ResultStatus`, `ContextClassification`, and `EvidenceLifecycle`, and supports artifact reference/hash-related functions and evidence repository operations. The presence of this framework and its unit tests supports claims about those implemented evidence functions only; it does not establish automatic evidence creation from every domain execution.

The snapshot's model contains both `execution_status` and `result` fields typed with `ResultStatus`. This reference records that as a schema detail rather than silently redefining its meaning. Any schema correction requires a separate compatibility-aware change and corresponding tests.

### 4.6 `a_framework/traceability.py`

Defines `TraceabilityRecord` and `TraceabilityRegistry`. Records can relate an objective, test case, optional execution ID, optional `TestResult`, and evidence IDs. Validation checks relevant identifiers and associations. The registry is in-memory and indexes records by queries; it is not persistent storage and does not own result evaluation or evidence lifecycle transitions.

### 4.7 `a_framework/logging_boundary.py`

Defines `get_logger(name)` and `configure_logging(level=logging.INFO, stream=None)`. Logging setup configures the root logger only if it has no handlers, avoiding duplicate handler setup. `a_framework/base_test.py` uses this boundary.

### 4.8 `a_framework/base_test.py`

Defines the abstract `BaseSecurityTest` used by legacy/domain-oriented test modules. It validates `test_name`, records timezone-aware start/end timestamps, logs lifecycle messages, collects domain-level result entries, and provides output/export helpers. Its `results` list is not interchangeable with the common `Observation`, `TestResult`, or `ExecutionOutcome` models.

### 4.9 `a_framework/config.py` and `a_framework/logger.py`

Both files are explicit structural placeholders in the snapshot (`Structural placeholder: not implemented.`). Do not describe them as implemented configuration or logger services. The functional logging boundary is `a_framework/logging_boundary.py`.

### 4.10 `a_framework/report_generator.py`

Contains the legacy/common report-generator implementation for consolidating domain assessment data. The existence of report-generation code does not prove all listed input artifacts exist, are current, or are generated from a common verified execution path. The snapshot describes generated report artifacts as incomplete/placeholder/inconsistent and end-to-end report generation as not verified.

### 4.11 `a_framework/test_evidence.py`

Contains tests for evidence-record validation, lifecycle transitions, artifact integrity, missing artifacts, repository write/round-trip behavior, and evidence/result metadata constraints. These tests verify the covered framework behavior, not CAN/UDS/Ethernet/Firmware security behavior against a real ECU or vehicle.

## 5. Domain implementation map

| Domain | Main module | Adapter | Domain pytest file | Snapshot interpretation |
|---|---|---|---|---|
| CAN | `b_security_tests/can_tests/can_sniffer.py` | `b_security_tests/can_tests/adapter.py` | `b_security_tests/can_tests/test_can_sniffer.py` | Domain code and adapter exist; the test file contains at least a `test_save_message` test. This does not alone establish end-to-end common-framework verification. |
| UDS | `b_security_tests/uds_tests/uds_security.py` | `b_security_tests/uds_tests/adapter.py` | `b_security_tests/uds_tests/test_uds_security.py` | The listed pytest test is `test_placeholder` with `assert True`; it is not evidence of UDS security validation. |
| Ethernet | `b_security_tests/ethernet_tests/ethernet_scan.py` | `b_security_tests/ethernet_tests/adapter.py` | `b_security_tests/ethernet_tests/test_ethernet_scan.py` | The listed pytest test is a placeholder; it is not evidence of network-scan validation. |
| Firmware | `b_security_tests/firmware_tests/firmware_validator.py` | `b_security_tests/firmware_tests/adapter.py` | `b_security_tests/firmware_tests/test_firmware_validator.py` | The listed pytest test is a placeholder; it is not evidence of firmware-validation coverage. |

The adapter boundary provides a common interface, while protocol- or artifact-specific behavior remains in the domain module. The existence of an adapter file is not by itself proof that a full test case, oracle/evaluation, evidence association, and reporting flow is wired end-to-end.

## 6. Execution and result flow

The common implemented execution path represented in the code is:

```text
Already-selected domain operation + input mapping
    -> TestRunner.run(...)
    -> ExecutionInterface.execute(...)
    -> DomainAdapter.run(...)
    -> DomainAdapter.execute(...)
    -> DomainAdapter.get_observation(...)
    -> ExecutionOutcome
```

This path returns execution status and observations. It does not, by itself, evaluate observations against an oracle, assign a `TestResult`, create an `EvidenceRecord`, persist traceability, or generate a final assessment report. Those are separate responsibilities and must only be described as integrated where a concrete code path and verification support that statement.

## 7. Evidence and traceability boundaries

The Evidence Framework provides record validation and repository-related behavior, including integrity-related checks covered by `a_framework/test_evidence.py`. `TraceabilityRegistry` provides in-memory associations. The two components have distinct ownership:

- Evidence records/repository: evidence metadata, validation, lifecycle and artifact-integrity responsibilities implemented in `evidence.py`.
- Traceability registry: relationship records and lookup operations in memory.
- Test runner/execution interface: adapter execution and observation handoff.
- Result evaluation: not performed by `TestRunner` or `ExecutionOutcome`.
- Reporting: consumes available report inputs; report artifacts in the snapshot are not proof of a complete verified pipeline.

Do not claim that every domain execution automatically produces persistent, validated, traceable evidence unless that path is implemented and tested.

## 8. Logging, configuration and reporting

`logging_boundary.py` is the implemented common logging entry point used by `BaseSecurityTest`. `logger.py` and `config.py` are placeholders in the snapshot. `report_generator.py` contains report-generation code, but the output artifacts and end-to-end generation status are not established as complete in the snapshot. Therefore, logging-boundary implementation and end-to-end operational readiness must be reported separately.

## 9. Verification scope represented by the snapshot

The pytest cache lists framework evidence tests and domain tests. The listed UDS, Ethernet and Firmware tests are placeholders; the CAN test includes a save-message test. A pytest cache is not a substitute for a fresh test run or its output. This reference does not claim that tests were re-executed while preparing this document.

Evidence-framework tests can support claims about evidence model validation, lifecycle rules, repository behavior and artifact integrity to the extent covered by each test. They do not demonstrate real-ECU, vehicle, OEM, production, or full domain security validation.

## 10. Implementation gaps and boundaries

The snapshot supports the following conservative statements:

1. `config.py` and `logger.py` are placeholders.
2. The runner performs a single already-selected adapter operation, not full scheduling/orchestration.
3. `ExecutionOutcome` is pre-evaluation and distinct from `TestResult`.
4. Traceability is in-memory, not persistent.
5. The presence of the Evidence Framework does not prove end-to-end evidence generation for all domain modules.
6. UDS, Ethernet and Firmware pytest files shown in the snapshot are placeholders.
7. Report artifacts and end-to-end report generation are identified as incomplete or not verified.
8. Regression and CI/CD are described elsewhere in the snapshot as not established/not implemented.

These are snapshot-based findings. A later code change or fresh verification run may change them; update the relevant documentation when that occurs.

## 11. File-to-architecture mapping

| File | Primary role | Authoritative companion document |
|---|---|---|
| `a_framework/test_architecture.py` | Shared test/execution/observation/result data models | `test_lifecycle_definition.md`, `test_responsibility_matrix.md` |
| `a_framework/domain_adapter.py` | Domain adapter contract and lifecycle | `execution_interface_definition.md`, `domain_architecture_matrix.md` |
| `a_framework/execution.py` | Execution interface and `ExecutionOutcome` | `execution_interface_definition.md` |
| `a_framework/runner.py` | Single adapter-operation coordination | `security_test_architecture_definition.md`, `test_responsibility_matrix.md` |
| `a_framework/evidence.py` | Evidence records, validation, lifecycle and repository | `evidence.md` |
| `a_framework/test_evidence.py` | Evidence-framework tests | `evidence.md`, `testing.md` |
| `a_framework/traceability.py` | In-memory traceability records/index | `assessment_objective_traceability_model.md` |
| `a_framework/logging_boundary.py` | Common logging API | `test_responsibility_matrix.md`, `environment.md` |
| `a_framework/config.py`, `a_framework/logger.py` | Structural placeholders | `test_responsibility_matrix.md` |
| `a_framework/base_test.py` | Legacy/domain-test base class | `test_lifecycle_definition.md`, `test_responsibility_matrix.md` |
| `a_framework/report_generator.py` | Report generation/consolidation | `testing.md`, `test_responsibility_matrix.md` |
| `b_security_tests/*/adapter.py` | Concrete domain adapter | `domain_architecture_matrix.md` |
| `b_security_tests/*/*.py` | Domain-specific technical logic | `ecu_security_domain_model.md`, `domain_architecture_matrix.md` |
| `b_security_tests/*/test_*.py` | Domain pytest coverage | `testing.md` |
| `c_evidence/` | Evidence and verification artifacts | `evidence.md` |
| `e_security_reports/` | Report artifacts | `testing.md`, `current_state.md` |

## 12. Documentation ownership

This file is the central description of how the implementation components fit together. Detailed normative architecture remains in `security_test_architecture_definition.md`; the execution contract remains in `execution_interface_definition.md`; lifecycle semantics remain in `test_lifecycle_definition.md`; evidence behavior remains in `evidence.md`; traceability semantics remain in `assessment_objective_traceability_model.md`; domain mapping remains in `domain_architecture_matrix.md`; and test responsibilities remain in `test_responsibility_matrix.md`.

`README.md` remains the project entry point and `current_state.md` remains the evolving status summary. Neither is replaced by this reference.
