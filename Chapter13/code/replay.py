PROHIBITED_REPLAY_EFFECTS = {
    'execute_external_action',
    'send_customer_message',
    'create_new_approval',
    'modify_customer_record',
}

def authorize_replay(replay_type, requested_effects, policy):
    allowed_types = set(policy.get('allowed_replay_types', []))
    if replay_type not in allowed_types:
        return {'authorized': False, 'reason': 'replay_type_not_allowed'}
    blocked = sorted(PROHIBITED_REPLAY_EFFECTS & set(requested_effects))
    if blocked:
        return {'authorized': False, 'reason': 'prohibited_effect_requested', 'blocked_effects': blocked}
    return {'authorized': True, 'reason': None}
