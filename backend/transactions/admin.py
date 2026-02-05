"""
Django admin configuration for Transactions app.
"""
from django.contrib import admin
from .models import Transaction, WithdrawalRequest


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin configuration for Transaction model."""
    
    list_display = (
        'user', 'transaction_type', 'amount', 
        'status', 'payment_method', 'created_at'
    )
    list_filter = ('transaction_type', 'status', 'payment_method', 'created_at')
    search_fields = ('user__email', 'user__full_name', 'payment_id', 'description')
    readonly_fields = ('id', 'created_at', 'updated_at', 'completed_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {
            'fields': ('id', 'user')
        }),
        ('Transaction Details', {
            'fields': ('transaction_type', 'amount', 'status', 'description')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'payment_id', 'payment_metadata')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at')
        }),
    )


@admin.register(WithdrawalRequest)
class WithdrawalRequestAdmin(admin.ModelAdmin):
    """Admin configuration for WithdrawalRequest model."""
    
    list_display = (
        'user', 'amount', 'net_amount', 
        'status', 'payment_method', 'created_at'
    )
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('user__email', 'user__full_name')
    readonly_fields = ('id', 'created_at', 'updated_at', 'completed_at', 'net_amount')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {
            'fields': ('id', 'user', 'transaction')
        }),
        ('Withdrawal Details', {
            'fields': ('amount', 'fee', 'net_amount', 'status')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'payment_details')
        }),
        ('Admin Actions', {
            'fields': ('approved_by', 'rejection_reason')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at')
        }),
    )
    
    actions = ['approve_withdrawals', 'reject_withdrawals']
    
    def approve_withdrawals(self, request, queryset):
        """Approve selected withdrawal requests."""
        count = queryset.filter(status='pending').update(
            status='approved',
            approved_by=request.user
        )
        self.message_user(request, f'{count} withdrawal(s) approved.')
    approve_withdrawals.short_description = 'Approve selected withdrawals'
    
    def reject_withdrawals(self, request, queryset):
        """Reject selected withdrawal requests."""
        count = queryset.filter(status='pending').update(status='rejected')
        self.message_user(request, f'{count} withdrawal(s) rejected.')
    reject_withdrawals.short_description = 'Reject selected withdrawals'
