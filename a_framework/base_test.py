"""
==========================================================
Automotive White-Box Security Assessment Framework

Base Test Class

Author:
    Zukhra Abdulaeva

Description:
    Common base class for all Automotive Security Tests.

Derived modules

- CAN Sniffer
- UDS Security Tester
- Ethernet Scanner
- Firmware Validator

==========================================================
"""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
import json
from a_framework.logging_boundary import configure_logging, get_logger


class BaseSecurityTest(ABC):
    """
    Base class for all security test modules.
    """

    def __init__(self, test_name: str):
        if not isinstance(test_name, str) or not test_name.strip():
            raise ValueError("test_name must be a non-empty string")

        self.test_name = test_name.strip()
        self.start_time = None
        self.end_time = None
        self.results = []

        self.logger = self._configure_logger()

    # -----------------------------------------------------

    def _configure_logger(self):
        configure_logging()
        return get_logger(self.test_name)

    # -----------------------------------------------------

    def start(self):

        self.start_time = datetime.now(timezone.utc)

        self.logger.info(
            f"Starting {self.test_name}"
        )

    # -----------------------------------------------------

    def stop(self):
        if self.start_time is None:
            raise RuntimeError("Cannot stop a test before it has started")
        self.end_time = datetime.now(timezone.utc)

        duration = self.end_time - self.start_time

        self.logger.info(
            f"Finished {self.test_name}"
        )

        self.logger.info(
            f"Duration: {duration}"
        )

    # -----------------------------------------------------

    def add_result(
        self,
        finding,
        severity,
        status,
        recommendation
    ):

        self.results.append({

            "timestamp":

                datetime.now(timezone.utc).isoformat(),

            "finding":

                finding,

            "severity":

                severity,

            "status":

                status,

            "recommendation":

                recommendation

        })

    # -----------------------------------------------------

    def print_results(self):

        print()

        print("=" * 60)

        print(self.test_name)

        print("=" * 60)

        if not self.results:

            print("No findings.")

        for item in self.results:

            print(f"Finding       : {item['finding']}")
            print(f"Severity      : {item['severity']}")
            print(f"Status        : {item['status']}")
            print(f"Recommendation: {item['recommendation']}")
            print("-" * 60)

    # -----------------------------------------------------

    def export_json(self, filename=None):

        if filename is None:

            filename = (
                self.test_name
                .lower()
                .replace(" ", "_")
                + ".json"
            )

        report = {

            "assessment":

                self.test_name,

            "generated":

                datetime.now(timezone.utc).isoformat(),

            "start_time":

                self.start_time.isoformat()
                if self.start_time else None,

            "end_time":

                self.end_time.isoformat()
                if self.end_time else None,

            "results":

                self.results

        }

        with open(filename, "w", encoding="utf-8") as file:

            json.dump(
                report,
                file,
                indent=4
            )

        self.logger.info(
            f"JSON exported -> {filename}"
        )

    # -----------------------------------------------------

    def export_markdown(self, filename=None):

        if filename is None:

            filename = (
                self.test_name
                .lower()
                .replace(" ", "_")
                + ".md"
            )

        with open(filename, "w", encoding="utf-8") as file:

            file.write(f"# {self.test_name}\n\n")

            file.write(
                f"Generated: {datetime.now(timezone.utc)}\n\n"
            )

            for result in self.results:

                file.write(
                    f"**Finding**: {result['finding']}\n\n"
                )

                file.write(
                    f"**Severity**: {result['severity']}\n\n"
                )

                file.write(
                    f"**Status**: {result['status']}\n\n"
                )

                file.write(
                    f"**Recommendation**:\n\n"
                )

                file.write(
                    result["recommendation"]
                )

                file.write("\n\n")

        self.logger.info(
            f"Markdown exported -> {filename}"
        )

    # -----------------------------------------------------

    def save(self):

        self.export_json()

        self.export_markdown()

    # -----------------------------------------------------

    @abstractmethod
    def run(self):
        """
        Execute security test.
        Must be implemented
        by derived classes.
        """
        pass
