import importlib

DomainAdapter = importlib.import_module("01_framework.domain_adapter").DomainAdapter
Observation = importlib.import_module("01_framework.test_architecture").Observation
ExecutionStatus = importlib.import_module("01_framework.test_architecture").ExecutionStatus


class FirmwareAdapter(DomainAdapter):
    domain = "Firmware"

    def __init__(self, validator):
        super().__init__()
        self.validator = validator

    def execute(self, inputs):
        operation = inputs.get("operation", "information")
        if operation == "information":
            output = self.validator.firmware_information(inputs["filename"])
        elif operation == "verify_integrity":
            output = self.validator.verify_integrity(inputs["filename"], inputs["expected_hash"])
        elif operation == "compare":
            output = self.validator.compare_firmware(inputs["firmware_a"], inputs["firmware_b"])
        else:
            raise ValueError(f"Unsupported firmware operation: {operation}")
        self._status = ExecutionStatus.COMPLETED
        return output

    def get_observation(self, execution_output):
        return Observation(value=execution_output, source="Firmware.FirmwareValidator")
