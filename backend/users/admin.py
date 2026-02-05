"""
Django admin configuration for Users app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for custom User model."""
    
    list_display = (
        'email', 'full_name', 'is_active', 'is_verified', 
        'membership_paid', 'wallet_balance', 'joined_at'
    )
    list_filter = (
        'is_active', 'is_verified', 'membership_paid', 
        'is_admin', 'is_staff', 'is_superuser'
    )
    search_fields = ('email', 'full_name', 'referral_code')
    ordering = ('-joined_at',)
    
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal Info', {
            'fields': ('full_name', 'phone_number')
        }),
        ('Status', {
            'fields': ('is_active', 'is_verified', 'is_admin')
        }),
        ('Membership', {
            'fields': ('membership_paid', 'membership_expiry')
        }),
        ('Referral', {
            'fields': ('referral_code', 'referred_by')
        }),
        ('Wallet', {
            'fields': ('wallet_balance',)
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important Dates', {
            'fields': ('last_login', 'joined_at'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'full_name', 'password1', 'password2',
                'referred_by', 'is_active', 'is_verified'
            ),
        }),
    )
    
    readonly_fields = ('joined_at', 'last_login', 'referral_code')
    
    def get_readonly_fields(self, request, obj=None):
        """Make certain fields readonly after creation."""
        if obj:  # Editing existing object
            return self.readonly_fields + ('email',)
        return self.readonly_fields
