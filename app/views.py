# app/views.py

# ───────────────────────────────
#  Standard Library
from datetime import datetime, date, timedelta

#  Django & DRF
from django.db import models
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

#  App-specific imports
from .models import Customer, Loan
from .serializers import (
    RegisterCustomerSerializer,
    CheckEligibilitySerializer,
    CreateLoanSerializer,
    ViewLoanSerializer,
    LoanListSerializer
)
from .utils import calculate_emi


# ───────────────────────────────
#  Helper Function
def get_customer_by_id(customer_id):
    try:
        return Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return None


# ───────────────────────────────
#  Customer Registration API
class RegisterCustomerAPIView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = RegisterCustomerSerializer


# ───────────────────────────────
#  Check Eligibility API
class CheckEligibilityView(APIView):
    def post(self, request):
        serializer = CheckEligibilitySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        customer = get_customer_by_id(data['customer_id'])
        if not customer:
            return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

        loans = Loan.objects.filter(customer=customer)
        total_emis = loans.aggregate(total=models.Sum('tenure'))['total'] or 0
        paid_emis = loans.aggregate(paid=models.Sum('emis_paid_on_time'))['paid'] or 0
        paid_ratio = paid_emis / total_emis if total_emis else 1
        num_loans = loans.count()
        current_year_loans = loans.filter(start_date__year=datetime.now().year).count()
        total_loan_volume = loans.aggregate(total=models.Sum('loan_amount'))['total'] or 0

        active_loans = loans.filter(end_date__gte=date.today())
        current_loan_sum = active_loans.aggregate(total=models.Sum('loan_amount'))['total'] or 0
        current_emis_sum = active_loans.aggregate(total=models.Sum('monthly_repayment'))['total'] or 0

        credit_score = (
            paid_ratio * 40 +
            max(0, 20 - num_loans * 2) +
            min(current_year_loans * 5, 15) +
            min(total_loan_volume / 100000, 25)
        )

        if current_loan_sum > customer.approved_limit or current_emis_sum > 0.5 * customer.monthly_income:
            credit_score = 0

        interest_rate = data['interest_rate']
        corrected_rate = interest_rate
        approved = False

        if credit_score > 50:
            approved = True
        elif 30 < credit_score <= 50:
            approved = True if interest_rate > 12 else False
            corrected_rate = max(interest_rate, 16)
        elif 10 < credit_score <= 30:
            approved = True if interest_rate > 16 else False
            corrected_rate = max(interest_rate, 20)

        if approved and interest_rate < corrected_rate:
            interest_rate = corrected_rate

        monthly_installment = calculate_emi(data['loan_amount'], interest_rate, data['tenure']) if approved else 0

        return Response({
            "customer_id": customer.customer_id,
            "approval": approved,
            "interest_rate": interest_rate,
            "corrected_interest_rate": corrected_rate,
            "tenure": data['tenure'],
            "monthly_installment": round(monthly_installment, 2),
        })


# ───────────────────────────────
#  Create Loan API
class CreateLoanAPIView(APIView):
    def post(self, request):
        serializer = CreateLoanSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        customer = get_customer_by_id(data['customer_id'])
        if not customer:
            return Response({'message': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        if data['loan_amount'] > customer.approved_limit - customer.current_debt:
            return Response({
                "loan_id": None,
                "customer_id": customer.customer_id,
                "loan_approved": False,
                "message": "Loan amount exceeds your eligible limit",
                "monthly_installment": 0.0
            }, status=status.HTTP_400_BAD_REQUEST)

        monthly_installment = calculate_emi(data['loan_amount'], data['interest_rate'], data['tenure'])

        loan = Loan.objects.create(
            customer=customer,
            loan_amount=data['loan_amount'],
            interest_rate=data['interest_rate'],
            tenure=data['tenure'],
            monthly_repayment=monthly_installment,
            emis_paid_on_time=0,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=data['tenure'] * 30),
        )

        customer.current_debt += data['loan_amount']
        customer.save()

        return Response({
            "loan_id": loan.loan_id,
            "customer_id": customer.customer_id,
            "loan_approved": True,
            "message": "Loan approved successfully",
            "monthly_installment": round(monthly_installment, 2)
        }, status=status.HTTP_201_CREATED)


# ───────────────────────────────
# View Single Loan
class ViewLoanAPIView(APIView):
    def get(self, request, loan_id):
        try:
            loan = Loan.objects.select_related("customer").get(loan_id=loan_id)
        except Loan.DoesNotExist:
            return Response({"error": "Loan not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ViewLoanSerializer(loan)
        return Response(serializer.data)


# ───────────────────────────────
#  View All Active Loans by Customer ID
class ViewCustomerLoansAPIView(APIView):
    def get(self, request, customer_id):
        customer = get_customer_by_id(customer_id)
        if not customer:
            return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

        loans = Loan.objects.filter(customer=customer, end_date__gte=date.today())
        serializer = LoanListSerializer(loans, many=True)
        return Response(serializer.data)
