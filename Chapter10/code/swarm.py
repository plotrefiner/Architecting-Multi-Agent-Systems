from dataclasses import dataclass, field
from typing import Set


@dataclass
class SwarmBudget:
    maximum_participants: int
    maximum_tasks: int
    maximum_messages: int
    maximum_rounds: int
    participants_used: int = 0
    tasks_used: int = 0
    messages_used: int = 0
    rounds_used: int = 0

    def can_spawn_task(self) -> bool:
        return self.tasks_used < self.maximum_tasks

    def consume_task(self) -> None:
        if not self.can_spawn_task():
            raise RuntimeError("swarm task budget exhausted")
        self.tasks_used += 1


@dataclass
class CandidateMerger:
    seen_keys: Set[str] = field(default_factory=set)

    def add_candidate(self, dedupe_key: str) -> bool:
        if dedupe_key in self.seen_keys:
            return False
        self.seen_keys.add(dedupe_key)
        return True
