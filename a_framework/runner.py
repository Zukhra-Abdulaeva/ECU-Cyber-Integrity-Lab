"""Runner for coordinating a single Phase-3 test execution.
The runner receives an already-selected domain adapter and its inputs.
Adapter execution and observation normalization are delegated to the
execution interface. Test evaluation and Phase-4 evidence handling
remain outside this module.
"""

from __future__ import annotations

from typing import Any, Mapping

from a_framework.domain_adapter import DomainAdapter
from a_framework.execution import (
    AdapterExecutionInterface,
    ExecutionInterface,
    ExecutionOutcome,
)


class TestRunner:
    """Coordinate one test execution through the common execution contract."""

    def __init__(
        self,
        execution_interface: ExecutionInterface | None = None,
    ) -> None:
        self._execution_interface = (
            execution_interface
            if execution_interface is not None
            else AdapterExecutionInterface()
        )

    def run(
        self,
        adapter: DomainAdapter,
        inputs: Mapping[str, Any],
    ) -> ExecutionOutcome:
        """Execute one selected adapter operation and return its outcome."""
        if not isinstance(adapter, DomainAdapter):
            raise TypeError("adapter must be a DomainAdapter instance")

        if not isinstance(inputs, Mapping):
            raise TypeError("inputs must be a mapping")

        return self._execution_interface.execute(
            adapter=adapter,
            inputs=dict(inputs),
        )


__all__ = ["TestRunner"]