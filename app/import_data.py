import pandas as pd
from app.models import Customer, Loan


def import_customers_from_excel(file_path="customer_data.xlsx"):
    try:
        df = pd.read_excel(file_path)
        df.rename(columns={
            'Customer ID': 'customer_id',
            'First Name': 'first_name',
            'Last Name': 'last_name',
            'Age': 'age',
            'Phone Number': 'phone_number',
            'Monthly Salary': 'monthly_income',
            'Approved Limit': 'approved_limit'
        }, inplace=True)

        for _, row in df.iterrows():
            Customer.objects.update_or_create(
                customer_id=row['customer_id'],
                defaults={
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'age': row['age'],
                    'phone_number': str(row['phone_number']),
                    'monthly_income': row['monthly_income'],
                    'approved_limit': row['approved_limit'],
                }
            )
        print("Customers imported successfully.")
    except Exception as e:
        print(f" Error importing customers: {e}")


def import_loans_from_excel(file_path="loan_data.xlsx"):
    try:
        df = pd.read_excel(file_path)
        df.rename(columns={
            'Loan ID': 'loan_id',
            'Customer ID': 'customer_id',
            'Loan Amount': 'loan_amount',
            'Tenure': 'tenure',
            'Interest Rate': 'interest_rate',
            'EMIs paid on Time': 'emis_paid_on_time',
            'Date of Approval': 'start_date',
            'End Date': 'end_date'
        }, inplace=True)

        for _, row in df.iterrows():
            customer = Customer.objects.get(customer_id=row['customer_id'])
            Loan.objects.update_or_create(
                loan_id=row['loan_id'],
                defaults={
                    'customer': customer,
                    'loan_amount': row['loan_amount'],
                    'tenure': row['tenure'],
                    'interest_rate': row['interest_rate'],
                    'monthly_repayment': 0,  # You can calculate if needed
                    'emis_paid_on_time': row['emis_paid_on_time'],
                    'start_date': pd.to_datetime(row['start_date']),
                    'end_date': pd.to_datetime(row['end_date']),
                }
            )
        print("Loans imported successfully.")
    except Exception as e:
        print(f" Error importing loans: {e}")
