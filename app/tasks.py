import pandas as pd
from .models import Customer, Loan
from celery import shared_task
from datetime import datetime

@shared_task
def import_customer_and_loan_data():
    # Load customer data
    customer_df = pd.read_excel('customer_data.xlsx')
    for _, row in customer_df.iterrows():
        Customer.objects.update_or_create(
            phone_number=row['phone_number'],
            defaults={
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'monthly_salary': row['monthly_salary'],
                'approved_limit': row['approved_limit'],
                'current_debt': row['current_debt'],
                'age': 30  # Placeholder; adjust if 'age' is available
            }
        )

    # Load loan data
    loan_df = pd.read_excel('loan_data.xlsx')
    for _, row in loan_df.iterrows():
        try:
            customer = Customer.objects.get(customer_id=row['customer_id'])
            Loan.objects.update_or_create(
                loan_id=row['loan_id'],
                defaults={
                    'customer': customer,
                    'loan_amount': row['loan_amount'],
                    'tenure': row['tenure'],
                    'interest_rate': row['interest_rate'],
                    'monthly_installment': row['monthly_repayment'],
                    'emis_paid_on_time': row['EMIs paid on time'],
                    'start_date': pd.to_datetime(row['start_date']),
                    'end_date': pd.to_datetime(row['end_date']),
                }
            )
        except Customer.DoesNotExist:
            continue
