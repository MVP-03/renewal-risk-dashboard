import pytest
from datetime import date
from src.scorer import days_until_renewal, risk_tier, score_renewals, arr_at_risk, summary


def test_days_until_renewal_future():
    ref = date(2025, 12, 1)
    days = days_until_renewal('2025-12-31', reference_date=ref)
    assert days == 30


def test_days_until_renewal_past():
    ref = date(2025, 12, 1)
    days = days_until_renewal('2025-11-15', reference_date=ref)
    assert days < 0


def test_risk_tier_critical():
    assert risk_tier(20, 40, 35) == 'critical'


def test_risk_tier_at_risk():
    assert risk_tier(45, 55, 50) == 'at-risk'


def test_risk_tier_watch():
    assert risk_tier(90, 62, 60) == 'watch'


def test_risk_tier_healthy():
    assert risk_tier(90, 85, 90) == 'healthy'


def test_risk_tier_expired():
    assert risk_tier(-5, 80, 80) == 'expired'


def test_score_renewals_sorted_critical_first():
    ref = date(2025, 12, 1)
    accounts = [
        {'name': 'Healthy Co', 'arr_usd': 200000, 'renewal_date': '2026-03-01', 'health_score': 85, 'engagement_score': 80},
        {'name': 'Risky Co', 'arr_usd': 90000, 'renewal_date': '2025-12-15', 'health_score': 30, 'engagement_score': 25},
    ]
    results = score_renewals(accounts, reference_date=ref)
    assert results[0]['account'] == 'Risky Co'
    assert results[0]['risk_tier'] == 'critical'


def test_score_renewals_same_tier_sorted_by_arr_desc():
    ref = date(2025, 12, 1)
    accounts = [
        {'name': 'Small Co', 'arr_usd': 30000, 'renewal_date': '2026-03-01', 'health_score': 85, 'engagement_score': 80},
        {'name': 'Big Co', 'arr_usd': 200000, 'renewal_date': '2026-03-01', 'health_score': 85, 'engagement_score': 80},
    ]
    results = score_renewals(accounts, reference_date=ref)
    assert results[0]['account'] == 'Big Co'


def test_arr_at_risk_sums_critical_and_at_risk():
    scored = [
        {'account': 'A', 'arr': 100000, 'risk_tier': 'critical', 'days_until_renewal': 20, 'health_score': 30, 'engagement_score': 30},
        {'account': 'B', 'arr': 50000, 'risk_tier': 'at-risk', 'days_until_renewal': 45, 'health_score': 55, 'engagement_score': 50},
        {'account': 'C', 'arr': 200000, 'risk_tier': 'healthy', 'days_until_renewal': 90, 'health_score': 90, 'engagement_score': 85},
    ]
    assert arr_at_risk(scored) == 150000


def test_arr_at_risk_all_healthy():
    scored = [
        {'account': 'A', 'arr': 100000, 'risk_tier': 'healthy', 'days_until_renewal': 90, 'health_score': 80, 'engagement_score': 80},
    ]
    assert arr_at_risk(scored) == 0


def test_summary_counts_by_tier():
    scored = [
        {'account': 'A', 'arr': 100000, 'risk_tier': 'critical', 'days_until_renewal': 20, 'health_score': 30, 'engagement_score': 30},
        {'account': 'B', 'arr': 50000, 'risk_tier': 'critical', 'days_until_renewal': 25, 'health_score': 40, 'engagement_score': 35},
        {'account': 'C', 'arr': 200000, 'risk_tier': 'healthy', 'days_until_renewal': 90, 'health_score': 90, 'engagement_score': 85},
    ]
    s = summary(scored)
    assert s['critical']['count'] == 2
    assert s['critical']['arr'] == 150000
    assert s['healthy']['count'] == 1


def test_score_renewals_empty_list():
    assert score_renewals([]) == []
