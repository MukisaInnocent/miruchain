"""
URL configuration for Admin Panel app.
"""
from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    # Dashboard
    path('dashboard', views.DashboardStatsView.as_view(), name='dashboard'),
    
    # User management
    path('users', views.UserManagementView.as_view(), name='users'),
    
    # Link moderation
    path('links/pending', views.ModerateLinksView.as_view(), name='pending_links'),
    path('links/<uuid:link_id>/approve', views.ApproveLinkView.as_view(), name='approve_link'),
    path('links/<uuid:link_id>/reject', views.RejectLinkView.as_view(), name='reject_link'),
    
    # Withdrawal management
    path('withdrawals/pending', views.PendingWithdrawalsView.as_view(), name='pending_withdrawals'),
    path('withdrawals/<uuid:withdrawal_id>/approve', views.ApproveWithdrawalView.as_view(), name='approve_withdrawal'),
    path('withdrawals/<uuid:withdrawal_id>/reject', views.RejectWithdrawalView.as_view(), name='reject_withdrawal'),
]
