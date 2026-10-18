import pytest

from a_framework.test_architecture import TestCase
from b_security_tests.inventory import (
    EvidenceState,
    ExecutionState,
    ImplementationState,
    InventoryRecord,
    TestInventory,
    VerificationState,
)


def make_case(test_case_id="CAN-001", domain="CAN", complete=True):
    kwargs = {}
    if complete:
        kwargs = {
            "assessment_objective": "Assess configured CAN filter behavior",
            "security_objective": "Keep traffic observation scoped",
            "target_model": "Controlled virtual CAN bus",
            "attack_surface": "CAN receive/filter interface",
            "attack_hypothesis": "Unexpected identifiers may be retained",
            "test_steps": ("Inject allowed identifier", "Inject disallowed identifier", "Capture filtered traffic"),
            "expected_behaviour": "Only configured identifiers are retained",
            "evaluation_criteria": ("All retained identifiers are allowed",),
            "security_oracle": "Compare observed IDs with configured allow-list",
        }
    return TestCase(
        test_case_id=test_case_id,
        name=f"{domain} test {test_case_id}",
        domain=domain,
        objective="Assess the testable security behavior",
        **kwargs,
    )


def test_inventory_adds_and_retrieves_record():
    record = InventoryRecord(make_case())
    inventory = TestInventory([record])
    assert len(inventory) == 1
    assert inventory.get("CAN-001") is record


def test_duplicate_test_case_ids_are_rejected():
    inventory = TestInventory([InventoryRecord(make_case())])
    with pytest.raises(ValueError, match="Duplicate test_case_id"):
        inventory.add(InventoryRecord(make_case()))


def test_inventory_filters_by_domain_case_insensitively():
    inventory = TestInventory([
        InventoryRecord(make_case("CAN-001", "CAN")),
        InventoryRecord(make_case("UDS-001", "UDS")),
        InventoryRecord(make_case("CAN-002", "can")),
    ])
    assert [row.test_case.test_case_id for row in inventory.by_domain("can")] == ["CAN-001", "CAN-002"]


def test_new_records_do_not_claim_execution_or_verification():
    record = InventoryRecord(make_case())
    assert record.implementation is ImplementationState.UNKNOWN
    assert record.execution is ExecutionState.NOT_EXECUTED
    assert record.evidence is EvidenceState.NOT_ASSESSED
    assert record.verification is VerificationState.NOT_VERIFIED


def test_incomplete_a1_definitions_are_listed():
    inventory = TestInventory([
        InventoryRecord(make_case("CAN-001", complete=True)),
        InventoryRecord(make_case("UDS-001", "UDS", complete=False)),
    ])
    assert [r.test_case.test_case_id for r in inventory.incomplete_definitions()] == ["UDS-001"]


def test_inventory_rows_include_a1_fields_and_lifecycle_statuses():
    inventory = TestInventory([InventoryRecord(make_case())])
    row = inventory.to_dicts()[0]
    assert row["test_case_id"] == "CAN-001"
    assert row["expected_behaviour"] == "Only configured identifiers are retained"
    assert row["execution"] == "NOT_EXECUTED"
    assert row["verification"] == "NOT_VERIFIED"


def test_unknown_id_and_empty_domain_are_reported():
    inventory = TestInventory([InventoryRecord(make_case())])
    with pytest.raises(KeyError, match="Unknown test_case_id"):
        inventory.get("MISSING")
    with pytest.raises(ValueError, match="domain"):
        inventory.by_domain(" ")
