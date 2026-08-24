from collections import Counter
from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass
class ConsensusResult:
    outcome: str
    winning_label: Optional[str] = None


def bounded_consensus(labels: Iterable[str], minimum_votes: int = 2, tie_outcome: str = "unresolved") -> ConsensusResult:
    counts = Counter(label for label in labels if label != "abstain")
    if not counts:
        return ConsensusResult(tie_outcome)

    most_common = counts.most_common()
    top_label, top_count = most_common[0]

    if top_count < minimum_votes:
        return ConsensusResult(tie_outcome)

    tied = [label for label, count in most_common if count == top_count]
    if len(tied) > 1:
        return ConsensusResult(tie_outcome)

    return ConsensusResult("selected", winning_label=top_label)


def confidence_permitted_use(record: dict, requested_use: str) -> bool:
    return record.get("permitted_use") == requested_use and requested_use != record.get("prohibited_use")
