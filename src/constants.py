RISK_TIER_THRESHOLDS = {
    'critical': {'max_days': 30,  'max_composite': 50},
    'at_risk':  {'max_days': 60,  'max_composite': 60},
    'watch':    {'max_composite': 70},
}

COMPOSITE_WEIGHTS = {
    'health_score':     0.6,
    'engagement_score': 0.4,
}

ARR_ALERT_FLOOR_USD = 10_000

SIGNAL_ESCALATION_THRESHOLD = 2
