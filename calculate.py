# calculate.py

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
      - final_salary: שכר שנתי נוכחי
      - person_age, person_gender: גיל ומין העובד
      - calculation_date: תאריך חיתוך (31.12.2024)
      - discount_map: dict[int, float] – מפה של שנות ותק לשיעורי היוון
      - mortality_map: dict[int, dict[int, float]] – מפה של {gender: {age: rate}}
    מחזיר:
      total_calc (float) – סכום PV של פיטורין ומוות.
    """
    # 1. חשב ותק ותק ללא סעיף 14
    tenure, non14 = calculate_tenure(start_date, leave_date, article14_date, calculation_date)

    total_calc = 0.0
    # 2. עבור כל שנה בתקופת החיוב non14
    for year in range(int(non14)):
        # 2.1 שיעור היוון מתוך המפה
        discount_rate = rate_of_discount(year, discount_map)
        # 2.2 שיעורי פיטורין ועזיבה (יחזיר dismiss_rate, resign_rate)
        dismiss_rate, resign_rate = calculate_resignation_rate(person_age + year)
        # 2.3 שיעור תמותה מתוך המפה
        death_rate = mortality_rate(person_gender, person_age + year, mortality_map)

        # 2.4 גובה תשלום שנתי
        annual_benefit = final_salary * ((1 + salary_growth) ** year)

        # 2.5 חישוב PV לפיטורין ולמוות
        pv_dismiss = annual_benefit * dismiss_rate / ((1 + discount_rate) ** year)
        pv_death = annual_benefit * death_rate / ((1 + discount_rate) ** year)

        total_calc += pv_dismiss + pv_death

    return total_calc
