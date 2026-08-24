from dataclasses import dataclass, asdict
from typing import Optional, Sequence

@dataclass(frozen=True)
class TraceSpan:
    trace_id: str
    span_id: str
    workflow_id: str
    component: str
    operation: str
    input_refs: Sequence[str]
    output_refs: Sequence[str]
    state_version: int
    status: str
    latency_ms: int
    cost_usd: float
    parent_span_id: Optional[str] = None
    model_version: Optional[str] = None
    prompt_version: Optional[str] = None
    tool_version: Optional[str] = None
    error_type: Optional[str] = None

    def to_dict(self):
        return asdict(self)

def validate_trace_span(span: dict) -> bool:
    required = {'trace_id','span_id','workflow_id','component','operation','input_refs','output_refs','state_version','status','latency_ms','cost_usd'}
    missing = required - set(span)
    if missing:
        raise ValueError(f'missing trace fields: {sorted(missing)}')
    if span['status'] not in {'success','failed','rejected','pending'}:
        raise ValueError('invalid trace status')
    return True
