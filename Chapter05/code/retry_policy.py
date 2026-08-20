"""Retry-policy helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RetryDecision:
    should_retry: bool
    reason: str
    next_attempt: int | None = None


@dataclass(frozen=True)
class RetryPolicy:
    retryable_errors: set[str]
    non_retryable_errors: set[str]
    max_attempts: int = 3
    backoff: str = "exponential"

    def evaluate(self, error_type: str, attempt_number: int) -> RetryDecision:
        if error_type in self.non_retryable_errors:
            return RetryDecision(False, f"{error_type} is non-retryable.")

        if error_type not in self.retryable_errors:
            return RetryDecision(False, f"{error_type} is not in retryable_errors.")

        if attempt_number >= self.max_attempts:
            return RetryDecision(False, "Maximum retry attempts reached.")

        return RetryDecision(
            True,
            f"Retry allowed with {self.backoff} backoff.",
            next_attempt=attempt_number + 1,
        )


DEFAULT_RETRY_POLICY = RetryPolicy(
    retryable_errors={
        "timeout",
        "temporary_rate_limit",
        "transient_service_unavailable",
    },
    non_retryable_errors={
        "permission_denied",
        "missing_required_input",
        "policy_violation",
    },
    max_attempts=3,
)
