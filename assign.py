from age_calculations import get_age, convert_to_date, is_number

def process_row(active_sheet, row_idx):
    """
    קורא שורה מגליון data2.xlsx לפי row_idx, ומחזיר:
      emp_id (מתעודת זהות בעמודה A אם קיימת, אחרת מספר שורה-1),
      birthdate, person_age, final_salary, full_name,
      start_date, leave_date, article14_date,
      article14_rate_cell, asset_value_cell, gender_cell
    """
    # מיפוי תאים לפי מיקום עמודות
    id_cell            = active_sheet.cell(row=row_idx, column=1)
    first_name_cell    = active_sheet.cell(row=row_idx, column=2)
    last_name_cell     = active_sheet.cell(row=row_idx, column=3)
    gender_cell        = active_sheet.cell(row=row_idx, column=4)
    birth_date_cell    = active_sheet.cell(row=row_idx, column=5)
    start_date_cell    = active_sheet.cell(row=row_idx, column=6)
    salary_cell        = active_sheet.cell(row=row_idx, column=7)
    article14_date_cell= active_sheet.cell(row=row_idx, column=8)
    article14_rate_cell= active_sheet.cell(row=row_idx, column=9)
    asset_value_cell   = active_sheet.cell(row=row_idx, column=10)
    leave_date_cell    = active_sheet.cell(row=row_idx, column=12)

    # יצירת emp_id מתעודת זהות או fallback לשורה-1
    if id_cell.value is not None and is_number(id_cell.value):
        emp_id = int(float(id_cell.value))
    else:
        emp_id = row_idx - 1

    # המרת תאריכים וערכים
    birthdate = convert_to_date(birth_date_cell.value)
    if birthdate is None:
        return None  # שורה תקולה

    person_age     = get_age(birthdate)
    final_salary   = float(salary_cell.value)
    full_name      = f"{first_name_cell.value} {last_name_cell.value}"
    start_date     = convert_to_date(start_date_cell.value)
    leave_date     = convert_to_date(leave_date_cell.value)
    article14_date = convert_to_date(article14_date_cell.value)

    return (
        emp_id, birthdate, person_age, final_salary, full_name,
        start_date, leave_date, article14_date,
        article14_rate_cell, asset_value_cell, gender_cell
    )

def assign_to_zero():
    # פונקציה זו אינה בשימוש בחלק 1 – ניתן להשאיר או להסיר
    total_sum = 0
    expected_return_assets = 0
    article14_rate = 0
    discount_value = 0
    discount_rate = 0
    gain_or_lose_asset = 0
    return article14_rate, discount_rate, discount_value, expected_return_assets, gain_or_lose_asset, total_sum
