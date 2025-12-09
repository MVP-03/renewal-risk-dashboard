import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from signals import triggered_signals, signal_count, annotate_signals

HEALTHY = {
    'account_id': 'a1', 'logins_last_30d': 20, 'logins_prev_30d': 18,
    'open_tickets': 1, 'nps_score': 8, 'seat_utilisation': 0.80,
    'exec_last_contact_days': 30,
}
AT_RISK = {
    'account_id': 'a2', 'logins_last_30d': 2, 'logins_prev_30d': 20,
    'open_tickets': 4, 'nps_score': 3, 'seat_utilisation': 0.25,
    'exec_last_contact_days': 120,
}


def test_no_signals_healthy():
    assert triggered_signals(HEALTHY) == []


def test_multiple_signals_at_risk():
    signals = triggered_signals(AT_RISK)
    assert 'login_drop' in signals
    assert 'low_nps' in signals
    assert 'seat_underuse' in signals


def test_signal_count():
    assert signal_count(HEALTHY) == 0
    assert signal_count(AT_RISK) >= 3


def test_annotate_escalate():
    result = annotate_signals([HEALTHY, AT_RISK])
    risky = next(r for r in result if r['account_id'] == 'a2')
    assert risky['escalate'] is True
    safe = next(r for r in result if r['account_id'] == 'a1')
    assert safe['escalate'] is False
