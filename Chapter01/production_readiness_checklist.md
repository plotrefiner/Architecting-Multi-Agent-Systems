# Production-Readiness Checklist

A production-ready agentic system isn't measured by demo polish. It is measured by reliable, safe, and quantifiable performance under real-world conditions.

Use this checklist to work through the key architectural questions before taking your agent from demo to production.

## Scope and value

- Is the user problem clearly defined?
- Is a multi-agent architecture actually needed?
- Would a simpler prompt, RAG pipeline, rules engine, or deterministic workflow be sufficient?
- What business or user value does the system create?
- What are the risks if the system gives a wrong answer or takes a wrong action?

## Agent responsibilities

- Does each agent have a clear role?
- Are responsibilities separated cleanly?
- Are input and output contracts defined?
- Are agents prohibited from making decisions outside their role?
- Is there a clear owner of the final output?
- Is there a clear owner of failure and escalation?

## Tool and action safety

- Which tools can each agent access?
- Are tool permissions based on least privilege?
- Are tool inputs validated before execution?
- Are tool outputs validated before use?
- Which actions are read-only, and which actions change external systems?
- Which actions require human approval?

## State, memory, and context

- What state is needed during a task?
- What memory is stored after the task?
- What information is shared across agents?
- What information should remain private?
- How is stale or incorrect memory handled?
- How is sensitive information protected?
- How is context selected for each model call?

## Reliability and failure handling

- What are the expected failure modes?
- Are retries bounded?
- Are loops detected and stopped?
- Are timeouts defined?
- Are fallback behaviors available?
- Can the system ask the user for clarification?
- Can the system escalate to a human?
- Can the system fail safely instead of hallucinating?

## Evaluation

- What does success mean for this system?
- Are there task-level metrics?
- Are there tool-call metrics?
- Are there safety and policy metrics?
- Are there latency and cost metrics?
- Are there golden test cases?
- Can the team run regression tests after prompt, model, or tool changes?

## Observability

- Are requests traced across agents?
- Are prompts and model versions logged?
- Are tool calls and results logged?
- Are intermediate outputs available for debugging?
- Are cost and latency tracked per request?
- Can failures be replayed?
- Are dashboards and alerts available?

## Human oversight and governance

- Which decisions require human review?
- How are human approvals captured?
- Can humans override or correct the system?
- Are audit logs available?
- Are data retention rules defined?
- Are compliance and responsible AI requirements addressed?
- Who is accountable for system behavior?

## Cost, latency, and scalability

- Is there a per-request cost budget?
- Are model choices appropriate for each task?
- Can independent steps run in parallel?
- Are expensive results cached?
- Are rate limits handled?
- Can the system handle production traffic?
- Is there a plan for load spikes and degraded service?

## Deployment and maintenance

- How are prompts versioned?
- How are tools versioned?
- How are model changes tested?
- How are rollback procedures handled?
- How are user feedback and production incidents incorporated?
- Who maintains the system after launch?
