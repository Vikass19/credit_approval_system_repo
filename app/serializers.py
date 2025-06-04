from rest_framework import serializers
from .models import Customer, Loan
from .utils import get_repayments_left


# ------------------------------
# Customer Serializers
# ------------------------------

class RegisterCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'customer_id', 'first_name', 'last_name',
            'age', 'monthly_income', 'phone_number', 'approved_limit'
        ]
        read_only_fields = ['customer_id', 'approved_limit']

    def create(self, validated_data):
        monthly_income = validated_data.get('monthly_income')
        approved_limit = round(36 * monthly_income / 100000) * 100000
        validated_data['approved_limit'] = approved_limit
        return super().create(validated_data)


# ------------------------------
# Loan Application Serializers
# ------------------------------

class CheckEligibilitySerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.FloatField()
    interest_rate = serializers.FloatField()
    tenure = serializers.IntegerField()


class CreateLoanSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.FloatField(min_value=0)
    interest_rate = serializers.FloatField(min_value=0)
    tenure = serializers.IntegerField(min_value=1)


# ------------------------------
# Loan Response Serializers
# ------------------------------

class ViewLoanSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    monthly_installment = serializers.FloatField(source='monthly_repayment')

    class Meta:
        model = Loan
        fields = [
            'loan_id', 'customer',
            'loan_amount', 'interest_rate',
            'monthly_installment', 'tenure'
        ]

    def get_customer(self, obj):
        customer = obj.customer
        return {
            "id": customer.customer_id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "phone_number": customer.phone_number,
            "age": customer.age,
        }


class LoanListSerializer(serializers.ModelSerializer):
    monthly_installment = serializers.FloatField(source='monthly_repayment')
    repayments_left = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = [
            'loan_id', 'loan_amount',
            'interest_rate', 'monthly_installment',
            'repayments_left'
        ]

    def get_repayments_left(self, obj):
        return get_repayments_left(obj.start_date, obj.end_date, obj.emis_paid_on_time)
