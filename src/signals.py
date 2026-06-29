from typing import List, Dict


EARLY_WARNING_RULES = [
    ('login_drop',       lambda a: a.get('logins_last_30d', 1) < a.get('logins_prev_30d', 1) * 0.5),
    ('support_surge',    lambda a: a.get('open_tickets', 0) >= 3),
    ('low_nps',          lambda a: a.get('nps_score', 10) <= 5),
    ('seat_underuse',    lambda a: a.get('seat_utilisation', 1.0) < 0.40),
    ('exec_disengaged',  lambda a: a.get('exec_last_contact_days', 0) > 90),
]


def triggered_signals(account: Dict) -> List[str]:
    return [name for name, rule in EARLY_WARNING_RULES if rule(account)]


def signal_count(account: Dict) -> int:
    return len(triggered_signals(account))


def annotate_signals(accounts: List[Dict]) -> List[Dict]:
    result = []
    for acc in accounts:
        signals = triggered_signals(acc)
        result.append({
            **acc,
            'warning_signals': signals,
            'signal_count':    len(signals),
            'escalate':        len(signals) >= 2,
        })
    return sorted(result, key=lambda x: x['signal_count'], reverse=True)
