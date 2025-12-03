from typing import Dict, List
from datetime import datetime


def validate_account(acc: Dict) -> List[str]:
    errors = []
    if not acc.get('name'):
        errors.append('name is required')
    try:
        datetime.strptime(acc.get('renewal_date', ''), '%Y-%m-%d')
    except ValueError:
        errors.append('renewal_date must be YYYY-MM-DD')
    for field in ('health_score', 'engagement_score'):
        val = acc.get(field, -1)
        try:
            if not (0 <= float(val) <= 100):
                errors.append(f'{field} must be 0-100')
        except (TypeError, ValueError):
            errors.append(f'{field} must be numeric')
    return errors
