
def rate_of_discount(work_years, discount_map):
    """
    מחזיר את שיעור ההיוון התואם מעץ מיפוי שמועבר כפרמטר.
    discount_map: dict[int, float] – מפה של שנות ותק לשיעורי היוון.
    """
    # בחר את המפתח הקרוב ביותר לשנות העבודה
    year_key = min(discount_map.keys(), key=lambda y: abs(y - work_years))
    return discount_map[year_key]
