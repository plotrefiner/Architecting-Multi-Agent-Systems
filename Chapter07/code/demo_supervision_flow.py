"""Demo supervision flow."""

from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from delegation import authorize_delegation
from aggregation import validate_worker_result
from routing import choose_route

@dataclass
class Request:
    text: str

@dataclass
class State:
    version: int = 3
    has_current_matching_approval: bool = False
    def required_fields_missing(self, request, intent):
        return ["order_id"] if intent == "refund_case" and "order" not in request.text.lower() else []
    def is_delegation_current(self, delegation_id, state_version):
        return state_version == self.version

class Classifier:
    def classify(self, text):
        text = text.lower()
        if "chargeback" in text and "replacement" in text:
            return "composite_support_case"
        if "return window" in text:
            return "refund_policy_question"
        return "refund_case"

class Supervisor:
    def route(self, packet):
        return {"route": "composite_support_case", "supervisor_required": True, "selected_responsibilities": ["retrieve_policy", "retrieve_order", "retrieve_chargeback_status"]}

@dataclass
class Task:
    assigned_worker: str
    responsibility: str
    delegation_depth: int = 1
    may_redelegate: bool = False

class Registry:
    def workers_for(self, responsibility):
        return {"retrieve_order": ["order_lookup_service"]}.get(responsibility, [])
    def validate(self, output_contract, payload):
        if not isinstance(payload, dict):
            raise ValueError("payload must be a dict")
    def require_evidence_scope(self, evidence_refs, evidence_scope):
        if evidence_scope not in evidence_refs:
            raise ValueError("missing evidence scope")

@dataclass
class Budget:
    maximum_depth: int = 1
    remaining_tasks: int = 3

@dataclass
class Delegation:
    delegation_id: str = "del_301"
    assigned_worker: str = "order_lookup_service"
    output_contract: str = "order_summary_v1"
    state_version: int = 3
    deadline: object = None
    evidence_scope: str = "order_lookup:order_456"
    def __post_init__(self):
        if self.deadline is None:
            self.deadline = datetime.now(timezone.utc) + timedelta(minutes=5)

@dataclass
class Result:
    delegation_id: str = "del_301"
    producer: str = "order_lookup_service"
    payload: dict = None
    state_version: int = 3
    created_at: object = None
    evidence_refs: list = None
    def __post_init__(self):
        if self.payload is None:
            self.payload = {"delivery_age_days": 12}
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)
        if self.evidence_refs is None:
            self.evidence_refs = ["order_lookup:order_456"]
    def to_accepted_artifact(self):
        return {"artifact_id": "order_202", "payload": self.payload}

def main():
    request = Request("The item arrived damaged. I already filed a chargeback, but I would accept a replacement.")
    state = State()
    print("Route:", choose_route(request, state, Classifier(), Supervisor()))
    print("Delegation authorized:", authorize_delegation(Task("order_lookup_service", "retrieve_order"), Registry(), [], Budget()))
    print("Accepted artifact:", validate_worker_result(Result(), Delegation(), Registry(), state))

if __name__ == "__main__":
    main()
