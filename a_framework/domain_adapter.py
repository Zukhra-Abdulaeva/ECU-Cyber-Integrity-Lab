"""Common adapter boundary for security-test domains.
Concrete CAN, UDS, Firmware, and Ethernet adapters implement ``execute`` and
``get_observation`` while retaining ownership of domain-specific interaction.
The common layer manages adapter lifecycle/status only;
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Mapping

from a_framework.test_architecture import ExecutionStatus, Observation


class DomainAdapter(ABC):
    """Base contract implemented by each security-domain adapter.

    Subclasses should implement ``execute`` to interact with their domain
    module and ``get_observation`` to expose the raw or normalized output as a
    shared ``Observation``. Evaluation and evidence creation remain outside
    this class.
    """

    domain: str = "UNSPECIFIED"

    def __init__(self) -> None:
        self._status = ExecutionStatus.NOT_STARTED

    @property
    def status(self) -> ExecutionStatus:
        """Current adapter execution status."""
        return self._status

    def mark_failed(self) -> None:
        """Mark the adapter execution as failed."""
        self._status = ExecutionStatus.FAILED
        
    def initialize(self) -> None:
        """Mark the adapter initialized before a test execution begins."""
        if self._status in (ExecutionStatus.RUNNING, ExecutionStatus.COMPLETED):
            raise RuntimeError(
                f"Cannot initialize adapter while status is {self._status.value}"
            )
        self._status = ExecutionStatus.INITIALIZED

    @abstractmethod
    def execute(self, inputs: Mapping[str, Any]) -> Any:
        """Execute one domain operation and return its raw output."""
        raise NotImplementedError

    @abstractmethod
    def get_observation(self, execution_output: Any) -> Observation:
        """Convert execution output into the common observation model."""
        raise NotImplementedError

    def run(self, inputs: Mapping[str, Any]) -> Any:
        """Run an adapter operation with consistent lifecycle/error handling.

        Existing domain adapters can keep their ``execute`` implementation.
        The runner should call this wrapper when it needs consistent status
        transitions and exception handling across domains.
        """
        if not isinstance(inputs, Mapping):
            raise TypeError("inputs must be a mapping")
        if self._status == ExecutionStatus.RUNNING:
            raise RuntimeError("Adapter is already running")

        self._status = ExecutionStatus.RUNNING
        try:
            output = self.execute(dict(inputs))
        except Exception:
            self._status = ExecutionStatus.FAILED
            raise

        # Concrete adapters may already set COMPLETED. Normalize the status
        # here so the common wrapper also works with simpler implementations.
        self._status = ExecutionStatus.COMPLETED
        return output

__all__ = ["DomainAdapter"]