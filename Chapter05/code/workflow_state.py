"""Durable workflow-state sketch."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class WorkflowState:
    workflow_id: str
    current_status: str = "in_progress"
    current_step: str = "start"
    completed_steps: list[str] = field(default_factory=list)
    pending_steps: list[str] = field(default_factory=list)
    agent_outputs: dict[str, Any] = field(default_factory=dict)
    tool_results: dict[str, Any] = field(default_factory=dict)
    approval_status: str = "not_required"
    retry_counts: dict[str, int] = field(default_factory=dict)
    errors: list[dict[str, Any]] = field(default_factory=list)

    def mark_step_completed(self, step_name: str) -> None:
        if step_name not in self.completed_steps:
            self.completed_steps.append(step_name)
        self.current_step = step_name

    def add_agent_output(self, agent_name: str, output: Any) -> None:
        self.agent_outputs[agent_name] = output

    def add_error(self, error_type: str, message: str) -> None:
        self.errors.append({"error_type": error_type, "message": message})
        self.current_status = "error"

    def to_dict(self) -> dict[str, Any]:
        return {
            "workflow_id": self.workflow_id,
            "current_status": self.current_status,
            "current_step": self.current_step,
            "completed_steps": self.completed_steps,
            "pending_steps": self.pending_steps,
            "agent_outputs": self.agent_outputs,
            "tool_results": self.tool_results,
            "approval_status": self.approval_status,
            "retry_counts": self.retry_counts,
            "errors": self.errors,
        }
