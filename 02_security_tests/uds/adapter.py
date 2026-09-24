import importlib

DomainAdapter = importlib.import_module("01_framework.domain_adapter").DomainAdapter
Observation = importlib.import_module("01_framework.test_architecture").Observation
ExecutionStatus = importlib.import_module("01_framework.test_architecture").ExecutionStatus


class UDSAdapter(DomainAdapter):
    domain = "UDS"

    def __init__(self, tester):
        super().__init__()
        self.tester = tester

    def execute(self, inputs):
        response = self.tester.send_request(inputs["request"])
        self._status = ExecutionStatus.COMPLETED
        return response

    def get_observation(self, execution_output):
        # Raw protocol response is the observation; evaluation remains outside the adapter.
        return Observation(value=execution_output, source="UDS.UDSSecurityTester")
