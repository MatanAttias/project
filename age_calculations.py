from datetime import date, datetime

def get_age(birthdate, reference_date=None):
    """
    מחשב גיל מלא בהתבסס על תאריך לידה ותאריך חיתוך.
    reference_date: date – ברירת מחדל היא 31.12.2024
    """
    if reference_date is None:
        reference_date = date(2024, 12, 31)
    years = reference_date.year - birthdate.year - (
        (reference_date.month, reference_date.day) < (birthdate.month, birthdate.day)
    )
    return years

def convert_to_date(value, fmt=None):
    """
    ממיר ערך ל־date.
    אם value הוא datetime, מחזיר date.
    אם value הוא מחרוזת, מנסה פורמט ISO (%Y-%m-%d) או fmt מסופק.
    """
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        for pattern in ([fmt] if fmt else ["%Y-%m-%d", "%d/%m/%Y"]):
            try:
                return datetime.strptime(value, pattern).date()
            except Exception:
                continue
    return None

def is_number(value):
    """
    בודק אם ניתן להמיר ל־float.
    """
    if value is None:
        return False
    try:
        float(value)
        return True
    except Exception:
        return False

def determine_gender(gender_value):
    """
    ממיר ערך מין ('M'/'F' או 0/1) לאינדקס 0=גברים, 1=נשים.
    """
    if isinstance(gender_value, str):
        val = gender_value.strip().upper()
        if val == "M":
            return 0
        if val == "F":
            return 1
    if isinstance(gender_value, (int, float)):
        return int(gender_value)  # הנחה: 0 או 1
    # ברירת מחדל
    return 0
