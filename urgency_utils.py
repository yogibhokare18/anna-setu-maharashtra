from datetime import datetime


def calculate_urgency(safe_until):

    now = datetime.utcnow()

    remaining_time = safe_until - now

    remaining_hours = remaining_time.total_seconds() / 3600

    if remaining_hours <= 2:
        return "Critical"

    elif remaining_hours <= 6:
        return "High"

    elif remaining_hours <= 12:
        return "Medium"

    else:
        return "Low"