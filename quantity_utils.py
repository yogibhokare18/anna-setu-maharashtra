def calculate_quantity_match(serves_people):

    if serves_people >= 50:
        return "High"

    elif serves_people >= 20:
        return "Medium"

    else:
        return "Low"