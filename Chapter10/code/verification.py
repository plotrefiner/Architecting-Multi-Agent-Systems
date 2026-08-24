from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CheckResult:
    status: str


@dataclass
class AcceptedVerification:
    status: str
    ref: str
    unsupported_claim_ids: List[str]


@dataclass
class VerificationOutcome:
    status: str
    ref: Optional[str] = None
    unsupported_claim_ids: Optional[List[str]] = None


@dataclass
class Policy:
    verifier_retained: bool = True
    maximum_redrafts: int = 1

    def build_verifier_context(self, draft_ref: str) -> dict:
        return {"draft_ref": draft_ref, "purpose": "claim_support_check"}


@dataclass
class Instance:
    redrafts_used: int = 0


class ClaimChecker:
    def __init__(self, status: str = "passed"):
        self.status = status

    def check(self, draft_ref: str) -> CheckResult:
        return CheckResult(self.status)


class Verifier:
    def verify(self, context: dict, output_contract: str) -> dict:
        return {"status": "revision_required", "unsupported_claim_ids": ["draft_claim_2"]}


class VerificationGate:
    def accept_verification(self, result: dict, instance: Instance) -> AcceptedVerification:
        return AcceptedVerification(
            status=result.get("status", "rejected"),
            ref="artifact:verify_601",
            unsupported_claim_ids=result.get("unsupported_claim_ids", []),
        )


@dataclass
class Services:
    claim_checker: ClaimChecker
    verifier: Verifier
    gate: VerificationGate


def run_bounded_verification(instance: Instance, draft_ref: str, services: Services, policy: Policy) -> VerificationOutcome:
    deterministic = services.claim_checker.check(draft_ref)

    if deterministic.status != "passed":
        return VerificationOutcome("deterministic_rejection")

    if not policy.verifier_retained:
        return VerificationOutcome("verifier_not_required")

    result = services.verifier.verify(
        context=policy.build_verifier_context(draft_ref),
        output_contract="verification_result_v1",
    )

    accepted = services.gate.accept_verification(result, instance)

    if accepted.status == "supported":
        return VerificationOutcome("supported", accepted.ref)

    if accepted.status != "revision_required":
        return VerificationOutcome("verification_rejected", accepted.ref)

    if instance.redrafts_used >= policy.maximum_redrafts:
        return VerificationOutcome("revision_budget_exhausted", accepted.ref)

    return VerificationOutcome(
        "one_redraft_permitted",
        accepted.ref,
        unsupported_claim_ids=accepted.unsupported_claim_ids,
    )
