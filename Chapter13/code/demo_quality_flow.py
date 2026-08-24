from evaluators import evaluate_trajectory, evaluate_tool_call
from replay import authorize_replay

if __name__ == '__main__':
    expected = ['classify_intent', 'retrieve_policy', 'await_human_authority']
    actual = ['classify_intent', 'retrieve_policy', 'await_human_authority']
    print(evaluate_trajectory(expected, actual, prohibited_nodes=['execute_approved_action']))
    print(evaluate_tool_call({'allowed': True, 'input_contract_valid': True, 'output_contract_valid': True}))
    policy = {'allowed_replay_types': ['trace_replay', 'artifact_replay']}
    print(authorize_replay('trace_replay', [], policy))
