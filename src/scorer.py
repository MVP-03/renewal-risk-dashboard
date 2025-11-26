import json
from datetime import datetime, date


def days_until_renewal(renewal_date_str, reference_date=None):
    renewal = datetime.strptime(renewal_date_str, '%Y-%m-%d').date()
    ref = reference_date or date.today()
    return (renewal - ref).days


def risk_tier(days_until, health_score, engagement_score):
    if days_until < 0:
        return 'expired'
    composite = health_score * 0.6 + engagement_score * 0.4
    if days_until <= 30 and composite < 50:
        return 'critical'
    if days_until <= 60 and composite < 60:
        return 'at-risk'
    if composite < 70:
        return 'watch'
    return 'healthy'


def score_renewals(accounts, reference_date=None):
    results = []
    for acct in accounts:
        days = days_until_renewal(acct['renewal_date'], reference_date)
        tier = risk_tier(days, acct['health_score'], acct['engagement_score'])
        results.append({
            'account': acct['name'],
            'arr': acct['arr_usd'],
            'days_until_renewal': days,
            'health_score': acct['health_score'],
            'engagement_score': acct['engagement_score'],
            'risk_tier': tier,
        })
    tier_order = {'expired': 0, 'critical': 1, 'at-risk': 2, 'watch': 3, 'healthy': 4}
    results.sort(key=lambda r: (tier_order.get(r['risk_tier'], 5), -r['arr']))
    return results


def arr_at_risk(scored):
    return sum(r['arr'] for r in scored if r['risk_tier'] in {'expired', 'critical', 'at-risk'})


def summary(scored):
    by_tier = {}
    for r in scored:
        tier = r['risk_tier']
        by_tier.setdefault(tier, {'count': 0, 'arr': 0})
        by_tier[tier]['count'] += 1
        by_tier[tier]['arr'] += r['arr']
    return by_tier


def load_and_score(path, reference_date=None):
    with open(path) as f:
        data = json.load(f)
    return score_renewals(data['accounts'], reference_date)
