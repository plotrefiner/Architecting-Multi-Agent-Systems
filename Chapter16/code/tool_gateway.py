from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class Tool:
    name: str
    owner: str
    invoke: Callable[[dict[str, Any]], Any]
    requires_approval: bool = False


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        if name not in self._tools:
            raise KeyError(f"unknown tool: {name}")
        return self._tools[name]


class ToolPolicy:
    def validate_arguments(self, tool_name: str, arguments: dict, state: object) -> None:
        if not isinstance(arguments, dict):
            raise ValueError("tool arguments must be a dictionary")

    def validate_current_approval(self, tool_name: str, arguments: dict, state: object) -> None:
        if not getattr(state, "approval_current", False):
            raise PermissionError("current approval required")


class ToolGateway:
    def __init__(self, registry: ToolRegistry, policy: ToolPolicy):
        self.registry = registry
        self.policy = policy

    def call(self, caller: str, tool_name: str, arguments: dict, state: object):
        tool = self.registry.get(tool_name)
        if caller != tool.owner:
            raise PermissionError("caller is not tool owner")
        self.policy.validate_arguments(tool_name=tool_name, arguments=arguments, state=state)
        if tool.requires_approval:
            self.policy.validate_current_approval(tool_name=tool_name, arguments=arguments, state=state)
        return tool.invoke(arguments)
