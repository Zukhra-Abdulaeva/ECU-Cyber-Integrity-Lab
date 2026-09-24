import importlib

DomainAdapter = importlib.import_module("01_framework.domain_adapter").DomainAdapter
Observation = importlib.import_module("01_framework.test_architecture").Observation


class CANAdapter(DomainAdapter):
    domain = "CAN"

    def __init__(self, sniffer):
        super().__init__()
        self.sniffer = sniffer

    def execute(self, inputs):
        self.sniffer.receive_messages(
            duration=inputs.get("duration", 10),
            filter_ids=inputs.get("filter_ids"),
        )
        self._status = importlib.import_module("01_framework.test_architecture").ExecutionStatus.COMPLETED
        return list(self.sniffer.messages)

    def get_observation(self, execution_output):
        return Observation(value=execution_output, source="CAN.CANSniffer")