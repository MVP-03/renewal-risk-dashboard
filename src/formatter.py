from typing import List, Dict


def format_risk_table(scored: List[Dict]) -> str:
    lines = [
        f"{'Account':<22} {'ARR':>10}  {'Days':>5}  {'Tier':<10}  Signals",
        '-' * 65,
    ]
    for r in scored:
        signals = ', '.join(r.get('warning_signals', [])) or '—'
        lines.append(
            f"{r['account']:<22} ${r['arr']:>9,.0f}  {r['days_until_renewal']:>5}  "
            f"{r['risk_tier']:<10}  {signals}"
        )
    return '\n'.join(lines)


def format_arr_at_risk(total_arr: float) -> str:
    return f'ARR at risk: ${total_arr:,.0f}'


def tier_badge(tier: str) -> str:
    badges = {
        'critical': '🔴 CRITICAL',
        'at-risk':  '🟠 AT-RISK',
        'watch':    '🟡 WATCH',
        'healthy':  '🟢 HEALTHY',
        'expired':  '⚫ EXPIRED',
    }
    return badges.get(tier, tier.upper())
