from utils import (
    calculate_distance_score,
    calculate_urgency_score,
    calculate_quantity_score,
    calculate_match_score
)


distance = 2
hours_left = 3
donation_quantity = 50
required_quantity = 40


distance_score = calculate_distance_score(distance)

urgency_score = calculate_urgency_score(hours_left)

quantity_score = calculate_quantity_score(
    donation_quantity,
    required_quantity
)

match_score = calculate_match_score(
    distance_score,
    urgency_score,
    quantity_score
)


print("Distance Score:", distance_score)
print("Urgency Score:", urgency_score)
print("Quantity Score:", quantity_score)
print("Match Score:", match_score)