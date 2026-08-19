def run_single_agent(user_request, agent, tools, max_steps=5):
    state = {
        "user_request": user_request,
        "observations": [],
        "steps": [],
        "status": "in_progress"
    }

    for step_number in range(max_steps):
        action = agent.choose_action(state)

        if action["type"] == "ask_clarifying_question":
            state["status"] = "needs_user_input"
            state["question"] = action["question"]
            return state

        if action["type"] == "call_tool":
            tool_name = action["tool_name"]
            tool_result = tools[tool_name](**action["tool_args"])
            state["observations"].append(tool_result)
            state["steps"].append(action)
            continue

        if action["type"] == "final_answer":
            state["status"] = "completed"
            state["answer"] = action["answer"]
            return state

        if action["type"] == "escalate":
            state["status"] = "needs_human_review"
            state["reason"] = action["reason"]
            return state

    state["status"] = "max_steps_exceeded"
    return state
