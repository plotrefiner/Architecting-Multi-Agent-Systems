def should_alert(metric_name, value, thresholds):
    rule = thresholds.get(metric_name)
    if rule is None:
        return False
    operator = rule.get('operator')
    threshold = rule.get('threshold')
    if operator == '>':
        return value > threshold
    if operator == '>=':
        return value >= threshold
    if operator == '<':
        return value < threshold
    if operator == '<=':
        return value <= threshold
    if operator == '==':
        return value == threshold
    raise ValueError(f'unsupported operator: {operator}')

def build_alert(alert_id, metric, value, owner, first_debugging_steps):
    return {
        'alert_id': alert_id,
        'metric': metric,
        'observed_value': value,
        'suspected_owner': owner,
        'first_debugging_steps': list(first_debugging_steps),
    }
