import importlib

DomainAdapter = importlib.import_module("01_framework.domain_adapter").DomainAdapter
Observation = importlib.import_module("01_framework.test_architecture").Observation
ExecutionStatus = importlib.import_module("01_framework.test_architecture").ExecutionStatus


class EthernetAdapter(DomainAdapter):
    domain = "Ethernet"

    def __init__(self, scanner):
        super().__init__()
        self.scanner = scanner

    def execute(self, inputs):
        self.scanner.scan(ports=inputs.get("ports", "22,80,443,13400,30490"))
        self._status = ExecutionStatus.COMPLETED
        return list(self.scanner.results)

    def get_observation(self, execution_output):
        return Observation(value=execution_output, source="Ethernet.AutomotiveEthernetScanner")
