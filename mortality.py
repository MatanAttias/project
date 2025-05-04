
def mortality_rate(gender_type, current_age, mortality_map):
    """
    מחזיר את שיעור התמותה (q_x) עבור גיל ומין, מתוך מיפוי שהוטען מראש.
    gender_type: 0 = גברים, 1 = נשים
    current_age: int
    mortality_map: dict[int, dict[int, float]] – { gender: { age: rate, … }, … }
    """
    age_map = mortality_map.get(gender_type, {})
    if not age_map:
        return 0.0
    # אם נמצא בדיוק
    if current_age in age_map:
        return age_map[current_age]
    # מצא את הגיל הקרוב ביותר
    closest_age = min(age_map.keys(), key=lambda age: abs(age - current_age))
    return age_map[closest_age]


def calculate_resignation_rate(person_age, turnover_map=None):
    """
    מחזיר (dismiss_rate, resign_rate) עבור גיל, מתוך מיפוי או חוק קשיח.
    אם turnover_map=None, נעזר בקוד המוטבע (אופציה זמנית).
    """
    if turnover_map:
        if not turnover_map:
            return 0.0, 0.0
        if person_age in turnover_map:
            return turnover_map[person_age]
        closest = min(turnover_map.keys(), key=lambda age: abs(age - person_age))
        return turnover_map[closest]

    # fallback: חוק קשיח כפי שהייתה בפונקציה המקורית
    if 18 <= person_age <= 29:
        return 0.07, 0.20
    if 30 <= person_age <= 39:
        return 0.05, 0.13
    if 40 <= person_age <= 49:
        return 0.04, 0.10
    if 50 <= person_age <= 59:
        return 0.03, 0.07
    if 60 <= person_age <= 67:
        return 0.02, 0.03
    return 0.0, 0.0
