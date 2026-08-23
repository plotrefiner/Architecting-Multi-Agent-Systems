"""Retry policy helpers."""


def should_retry(failure_class, attempts_so_far, policy, time_remaining=True):
    if failure_class in policy.get("never_retry", []):
        return False

    if not time_remaining and policy.get("workflow_deadline_required", False):
        return False

    if attempts_so_far >= policy["maximum_attempts"]:
        return False

    return failure_class in policy.get("retry_on", [])
