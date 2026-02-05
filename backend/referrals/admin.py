"""
Django admin configuration for Referrals app.
"""
from django.contrib import admin
from .models import Referral


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    """Admin configuration for Referral model."""
    
    list_display = (
        'referrer', 'referred', 'level', 
        'commission_earned', 'created_at'
    )
    list_filter = ('level', 'created_at')
    search_fields = (
        'referrer__email', 'referrer__full_name',
        'referred__email', 'referred__full_name'
    )
    readonly_fields = ('id', 'created_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {
            'fields': ('id', 'referrer', 'referred')
        }),
        ('Commission Details', {
            'fields': ('level', 'commission_earned')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )
