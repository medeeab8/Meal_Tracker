
def calculate_tdee(height, weight, activity_level):
    # Placeholder TDEE calculation
    base_tdee = (height * 6.25) + (weight * 9.99) - (5 * 30) + 5  
    activity_multiplier = {
        1: 1.2,
        2: 1.375,
        3: 1.55,
        4: 1.725,
        5: 1.9
    }
    return int(base_tdee * activity_multiplier.get(activity_level, 1.2))