import pytest
from datetime import date


@pytest.fixture
def healthy_account():
    return {'name': 'Healthy Corp', 'arr_usd': 50000, 'renewal_date': '2026-09-01',
            'health_score': 85.0, 'engagement_score': 80.0,
            'logins_last_30d': 25, 'logins_prev_30d': 22, 'open_tickets': 0,
            'nps_score': 9, 'seat_utilisation': 0.90, 'exec_last_contact_days': 15}


@pytest.fixture
def critical_account():
    return {'name': 'At Risk LLC', 'arr_usd': 120000, 'renewal_date': '2026-07-15',
            'health_score': 35.0, 'engagement_score': 30.0,
            'logins_last_30d': 1, 'logins_prev_30d': 18, 'open_tickets': 5,
            'nps_score': 2, 'seat_utilisation': 0.15, 'exec_last_contact_days': 100}


@pytest.fixture
def reference_date():
    return date(2026, 6, 29)
