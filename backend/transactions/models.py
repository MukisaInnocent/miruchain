"""
Models for transaction management.
"""
import uuid
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Transaction(models.Model):
    """
    Records all financial transactions in the system.
    """
    TRANSACTION_TYPES = (
        ('membership_payment', 'Membership Payment'),
        ('advertising_payment', 'Advertising Payment'),
        ('referral_commission', 'Referral Commission'),
        ('link_earning', 'Link Earning'),
        ('withdrawal', 'Withdrawal'),
        ('refund', 'Refund'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # User
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='transaction_history'
    )
    
    # Transaction details
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    description = models.TextField(blank=True)
    
    # Payment gateway details
    payment_method = models.CharField(max_length=50, blank=True)
    payment_id = models.CharField(max_length=255, blank=True, help_text='External payment ID')
    payment_metadata = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'transactions'
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['transaction_type']),
            models.Index(fields=['status']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['payment_id']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.transaction_type} - ${self.amount} ({self.status})"


class WithdrawalRequest(models.Model):
    """
    Tracks withdrawal requests from users.
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # User and transaction
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='withdrawal_requests'
    )
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        related_name='withdrawal_request',
        null=True,
        blank=True
    )
    
    # Withdrawal details
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    fee = models.DecimalField(
       max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    net_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    # Payment details
    payment_method = models.CharField(max_length=50)
    payment_details = models.JSONField(default=dict, help_text='Bank account, PayPal email, etc.')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(blank=True)
    
    # Admin handling
    approved_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_withdrawals'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'withdrawal_requests'
        verbose_name = 'Withdrawal Request'
        verbose_name_plural = 'Withdrawal Requests'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['status']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - ${self.amount} ({self.status})"
