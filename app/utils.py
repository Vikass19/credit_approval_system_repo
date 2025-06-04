# app/utils.py
from datetime import date

def calculate_emi(principal, annual_rate, tenure_months):
    monthly_rate = annual_rate / 100 / 12
    if monthly_rate == 0:
        return round(principal / tenure_months, 2)
    emi = principal * monthly_rate * (1 + monthly_rate) ** tenure_months / ((1 + monthly_rate) ** tenure_months - 1)
    return round(emi, 2)


def get_repayments_left(start_date, end_date, emis_paid_on_time):
    total_days = (end_date - start_date).days
    total_emis = total_days // 30
    remaining = max(0, total_emis - emis_paid_on_time)
    return remaining
