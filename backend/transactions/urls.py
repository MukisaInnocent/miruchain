"""
URL configuration for Transactions app.
"""
from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    # Transaction history
    path('', views.TransactionListView.as_view(), name='list'),
    path('summary', views.get_transaction_summary, name='summary'),
    
    # Payments
    path('create-payment-intent', views.CreatePaymentIntentView.as_view(), name='create_payment'),
    path('confirm-payment', views.ConfirmPaymentView.as_view(), name='confirm_payment'),
    
    # Withdrawals
    path('withdrawal', views.WithdrawalRequestCreateView.as_view(), name='create_withdrawal'),
    path('withdrawals', views.WithdrawalRequestListView.as_view(), name='list_withdrawals'),
]
