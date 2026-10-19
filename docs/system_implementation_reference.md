# System Implementation Reference

## 1. Purpose and scope

This document maps the repository's concrete implementation files to their technical responsibilities and records the boundaries between implemented components and integrated workflows. It complements the architecture definition, execution-interface definition, lifecycle definition, evidence definition, traceability model, and responsibility matrices.

Implementation statements are grounded in the code and test files in the supplied repository snapshot. Phase-5 core test execution was reported as successful, and domain evidence artifacts were reported as created. This status does not establish validation against a physical ECU, production vehicle, or production network. A component's presence, a successful software test, and end-to-end security validation remain distinct claims.

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
| `b_security_tests/uds_tests/` | UDS domain module, adapter, and domain tests | Concrete UDS request handling and response-classification logic, adapter, and behavioral pytest tests are present. |
| `b_security_tests/ethernet_tests/` | Ethernet scanning module and adapter | The scanning implementation is present in `test_ethernet_scan.py`; the supplied file does not contain pytest functions named `test_*`, so it must not be described as domain pytest coverage. |
| `b_security_tests/firmware_tests/` | Firmware domain module, adapter, and domain tests | Concrete firmware hash, integrity-comparison, file-comparison and JSON-export logic, adapter, and behavioral pytest tests are present. |
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

| Domain | Main module | Adapter | Test / pytest file | Snapshot interpretation |
|---|---|---|---|---|
| CAN | `b_security_tests/can_tests/can_sniffer.py` | `b_security_tests/can_tests/adapter.py` | `b_security_tests/can_tests/test_can_sniffer.py` | Domain code and adapter exist. Pytest functions cover message normalization, filtered and unfiltered capture using test doubles, disconnected-bus and duration validation, CSV export, and statistics. These tests do not establish physical CAN validation or common-framework end-to-end verification. |
| UDS | `b_security_tests/uds_tests/uds_security.py` | `b_security_tests/uds_tests/adapter.py` | `b_security_tests/uds_tests/test_uds_security.py` | The implementation and adapter are present. Tests cover request construction, response-ID filtering, invalid input, positive/negative/malformed response classification, JSON export, and bus shutdown using a fake bus. These are software-level tests, not validation against a real ECU. |
| Ethernet | `b_security_tests/ethernet_tests/test_ethernet_scan.py` | `b_security_tests/ethernet_tests/adapter.py` | The supplied `test_ethernet_scan.py` contains the `AutomotiveEthernetScanner` implementation rather than pytest test functions. | Scanner code provides bounded target validation, port validation, TCP connect scanning, service inventory, cautious service review hints, summary and JSON export. The file naming does not establish that pytest coverage exists for this module. |
| Firmware | `b_security_tests/firmware_tests/firmware_validator.py` | `b_security_tests/firmware_tests/adapter.py` | `b_security_tests/firmware_tests/test_firmware_validator.py` | The implementation and adapter are present. Tests cover SHA-256, file metadata, matching and mismatching digests, invalid expected hashes, firmware comparison, missing files, JSON export, and evidence-file naming. These tests validate static file operations, not Secure Boot or a physical ECU. |

The adapter boundary provides a common interface, while protocol- or artifact-specific behavior remains in the domain module. The presence of an adapter file is not by itself proof that a complete test case, oracle/evaluation, evidence association, and reporting flow is wired end-to-end.

Phase-5 core test execution was reported as successful by the project owner, with evidence artifacts created for the supported domains. This document does not assert a consolidated test count or claim that each domain has independently verified end-to-end integration. In particular, the current Ethernet source filename and contents should be reconciled with the intended pytest layout before claiming dedicated pytest coverage for the scanner.

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

The repository contains framework evidence tests and behavioral pytest tests for CAN, UDS, and firmware. The supplied Ethernet file `b_security_tests/ethernet_tests/test_ethernet_scan.py` contains scanner implementation code but no pytest test functions in the snapshot inspected for this document. Its filename alone is not evidence of pytest coverage.

Phase-5 core test execution was reported as successful, and domain evidence artifacts were reported as created. The supplied snapshot does not provide a single authoritative consolidated transcript of the latest complete Phase-5 pytest invocation in this document, so no aggregate count is asserted here. Historical counts must remain tied to their original execution records.

Evidence-framework tests support claims about the evidence-model validation, lifecycle rules, repository behavior, and artifact-integrity checks covered by those tests. CAN, UDS, and firmware tests use software-level conditions and test doubles where shown. They do not establish real-ECU, vehicle, OEM, production, or complete domain security validation. The Ethernet scanner's implementation supports bounded network-scan operations, but the current source snapshot does not establish dedicated pytest coverage for that scanner.

## 10. Implementation gaps and boundaries

The snapshot supports the following statements:

1. `a_framework/config.py` and `a_framework/logger.py` are structural placeholders; the common logging boundary is implemented in `a_framework/logging_boundary.py`.
2. The runner performs one already-selected adapter operation, not full scheduling or multi-test orchestration.
3. `ExecutionOutcome` is pre-evaluation and distinct from `TestResult`.
4. The traceability registry is in-memory, not persistent storage.
5. The Evidence Framework implements evidence-record validation and repository-related behavior, but does not establish automatic evidence creation from every domain execution.
6. Behavioral pytest tests are present for CAN, UDS and firmware. The supplied Ethernet scanner file contains implementation code, but dedicated pytest coverage for that scanner is not established by this snapshot.
7. Report-generation code is present; complete end-to-end report generation is not established by the component mapping alone.
8. Regression and CI/CD remain documented elsewhere as not implemented or not established.

These statements describe the supplied repository snapshot together with the reported Phase-5 execution status. Any subsequent code change or fresh verification run may change them; update the relevant documentation when that occurs.

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

`README.md` remains the project entry point and `current_state.md` remains the evolving status summary.
