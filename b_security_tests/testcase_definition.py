"""Tests for the common security TestCase definition."""
import pytest

from a_framework.test_architecture import TestCase


def test_legacy_test_case_constructor_remains_compatible():
    case = TestCase(
        test_case_id="CAN-LEGACY-001",
        name="Legacy CAN test",
        domain="CAN",
        objective="Check a legacy case can still be constructed",
    )
    assert case.test_case_id == "CAN-LEGACY-001"
    assert case.definition_issues()


def test_complete_a1_definition_is_accepted():
    case = TestCase(
        test_case_id="CAN-001",
        name="Capture configured CAN identifiers",
        domain="CAN",
        objective="Determine whether the capture filter is applied",
        preconditions=("A controlled virtual CAN bus is available",),
        inputs={"duration": 1, "filter_ids": [0x100]},
        tags=("phase-5", "virtual"),
        assessment_objective="Assess correct application of configured CAN capture filters",
        security_objective="Maintain reliable and scoped observation of CAN traffic",
        target_model="Controlled virtual CAN bus",
        attack_surface="CAN message receive/filter interface",
        attack_hypothesis="Messages outside the configured identifier set may be retained",
        test_steps=(
            "Inject one message with identifier 0x100",
            "Inject one message with identifier 0x200",
            "Capture traffic with filter_ids=[0x100]",
        ),
        expected_behaviour="Only messages with identifier 0x100 are retained",
        evaluation_criteria=("All retained messages have identifier 0x100",),
        security_oracle="Compare retained arbitration IDs with the configured allow-list",
    )
    assert case.definition_issues() == ()
    case.assert_definition_complete()


def test_assert_definition_complete_lists_missing_fields():
    case = TestCase(
        test_case_id="UDS-001",
        name="UDS access-control test",
        domain="UDS",
        objective="Assess the configured UDS security access behavior",
    )
    with pytest.raises(ValueError, match="assessment_objective.*security_objective"):
        case.assert_definition_complete()


def test_text_lists_reject_empty_or_non_string_items():
    with pytest.raises(ValueError, match=r"test_steps\[0\]"):
        TestCase(
            test_case_id="FW-001",
            name="Firmware test",
            domain="FIRMWARE",
            objective="Assess file integrity",
            test_steps=("",),
        )


def test_text_list_fields_reject_a_single_string():
    with pytest.raises(TypeError, match="test_steps must be an iterable"):
        TestCase(
            test_case_id="ETH-001",
            name="Ethernet test",
            domain="ETHERNET",
            objective="Assess target validation",
            test_steps="this is not a sequence of steps",
        )
