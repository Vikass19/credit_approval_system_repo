# app/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterCustomerAPIView.as_view(), name='register-customer'),
    path('check-eligibility/', CheckEligibilityView.as_view(), name='check-eligibility'),
    path('create-loan/', CreateLoanAPIView.as_view(), name='create-loan'),
    path('view-loan/<int:loan_id>/', ViewLoanAPIView.as_view(), name='view-loan'),
    path('view-loans/<int:customer_id>/', ViewCustomerLoansAPIView.as_view(), name='view-customer-loans'),
]
