def calculate_distance_score(distance_km):
    """
    Distance कमी असेल तर score जास्त.
    0 km = 100
    10 km किंवा त्यापेक्षा जास्त = 0
    """

    if distance_km is None:
        return 0

    score = 100 - (distance_km * 10)

    return max(0, min(100, score))


def calculate_urgency_score(hours_left):
    """
    Food expiry जवळ असेल तर urgency score जास्त.
    """

    if hours_left is None:
        return 0

    if hours_left <= 1:
        return 100
    elif hours_left <= 3:
        return 90
    elif hours_left <= 6:
        return 75
    elif hours_left <= 12:
        return 60
    elif hours_left <= 24:
        return 40
    else:
        return 20


def calculate_quantity_score(donation_quantity, required_quantity):
    """
    Donation quantity आणि required quantity match.
    """

    if not donation_quantity or not required_quantity:
        return 0

    difference = abs(donation_quantity - required_quantity)

    score = 100 - ((difference / required_quantity) * 100)

    return max(0, min(100, score))


def calculate_match_score(
    distance_score,
    urgency_score,
    quantity_score
):
    """
    Final Matching Score.
    """

    score = (
        (distance_score * 0.40)
        + (urgency_score * 0.30)
        + (quantity_score * 0.30)
    )

    return round(score, 2)