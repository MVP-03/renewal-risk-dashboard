# renewal-risk-dashboard

CLI tool that scores upcoming B2B SaaS renewals by risk tier — critical, at-risk, watch, or healthy — based on health score, engagement score, and days to renewal. Helps CS and sales prioritise outreach before the renewal crunch.

## Usage

```bash
python -c "from src.scorer import load_and_score, summary; s = load_and_score('data/renewals.json'); print(summary(s))"
pytest tests/
```

## Risk tiers

| Tier | Criteria |
|---|---|
| critical | ≤30 days to renewal AND composite score < 50 |
| at-risk | ≤60 days to renewal AND composite score < 60 |
| watch | composite score < 70 |
| healthy | composite score ≥ 70 |

Composite = `health_score × 0.6 + engagement_score × 0.4`

Results are sorted: critical first, then at-risk, watch, healthy. Within each tier, higher ARR accounts appear first.

## Input format

```json
{
  "accounts": [
    {
      "name": "Acme Corp",
      "arr_usd": 120000,
      "renewal_date": "2026-01-15",
      "health_score": 42,
      "engagement_score": 38
    }
  ]
}
```

## Motivation

Going into Q4 2025 renewal season we had no systematic way to triage which accounts CS should touch first. We were prioritising by gut feel and ARR alone — missing accounts that were small but churning fast. This script gives a ranked list so CS can work the list top-to-bottom.
