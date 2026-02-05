"""
URL configuration for Referrals app.
"""
from django.urls import path
from . import views

app_name = 'referrals'

urlpatterns = [
    path('', views.ReferralListView.as_view(), name='list'),
    path('tree', views.ReferralTreeView.as_view(), name='tree'),
    path('chain', views.ReferralChainView.as_view(), name='chain'),
    path('stats', views.CommissionStatsView.as_view(), name='stats'),
    path('direct', views.get_direct_referrals, name='direct'),
]
