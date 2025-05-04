from discount import rate_of_discount
from mortality import calculate_resignation_rate, mortality_rate

def get_non_article14_term(non_article14_years, tenure):
    return non_article14_years if non_article14_years > 0 else tenure


def calculate_tenure(start_date, leave_date, article14_date, calculation_date):
    tenure = (calculation_date - start_date).days / 365.0
    if not article14_date or article14_date == "-":
        non_article14_years = tenure
    else:
        non_article14_years = (article14_date - start_date).days / 365.0
    return tenure, non_article14_years


def determine_retirement_age(person_gender, person_age):
    if person_gender == 1:
        return 64, 64 - person_age
    return 67, 67 - person_age


def perform_calculation(
    start_date,
    leave_date,
    article14_date,
    salary_growth,
    final_salary,
    person_age,
    person_gender,
    calculation_date,
    discount_map,
    mortality_map
):
    """
    מחשב את ערך ה-PV של התחייבות פיצויי פיטורין לפי IAS19 (כולל מוות).
    פרמטרים:
      - start_date, leave_date, article14_date: תאריכים
      - salary_growth: שיעור צמיחת שכר (למשל 0.04)
      - final_salary: שכר חודשי נוכחי (כפול 12 לחישוב שנתי)
      - person_age, person_gender: גיל ומין העובד
      - calculation_date: תאריך חיתוך (31.12.2024)
      - discount_map: dict[int, float] – מפה של שנות ותק לשיעורי היוון
      - mortality_map: dict[int, dict[int, float]] – מפה של {gender: {age: rate}}
    מחזיר:
      total_calc (float) – סכום PV של פיטורין ומוות, מעוגל לשקלים
    """
    # 1. Annualize salary
    annual_salary = final_salary * 12

    # 2. חשב ותק ותק ללא סעיף 14
    tenure, non14 = calculate_tenure(start_date, leave_date, article14_date, calculation_date)

    total_calc = 0.0
    # 3. עבור כל שנה בתקופת החיוב non14
    for year in range(int(non14)):
        n = year + 1
        # 3.1 שיעור היוון לשנה n
        discount_rate = rate_of_discount(n, discount_map)
        # 3.2 שיעורי פיטורין ועזיבה לגיל המתאים
        dismiss_rate, resign_rate = calculate_resignation_rate(person_age + year)
        # 3.3 שיעור תמותה לגיל המתאים
        death_rate = mortality_rate(person_gender, person_age + year, mortality_map)

        # 3.4 גובה תשלום שנתי עם צמיחת שכר לשנה n
        annual = annual_salary * ((1 + salary_growth) ** n)

        # 3.5 חישוב PV לפיטורין ולמוות בשנת n
        total_calc += annual * dismiss_rate / ((1 + discount_rate) ** n)
        total_calc += annual * death_rate   / ((1 + discount_rate) ** n)

    # 4. עיגול לשקלים
    return round(total_calc, 0)
