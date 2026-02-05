"""
Models for referral tracking and commissions.
"""
import uuid
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Referral(models.Model):
    """
    Tracks referral relationships and commissions earned.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Referral relationship
    referrer = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='commissions_earned',
        help_text='User who earned this commission'
    )
    referred = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='commissions_generated',
        help_text='New user who generated this commission'
    )
    
    # Commission details
    level = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text='Level in referral chain (1=direct, 2+=upline)'
    )
    commission_earned = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'referrals'
        verbose_name = 'Referral Commission'
        verbose_name_plural = 'Referral Commissions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['referrer']),
            models.Index(fields=['referred']),
            models.Index(fields=['level']),
            models.Index(fields=['-created_at']),
        ]
        # Ensure unique referral commission per referrer-referred-level combination
        unique_together = [['referrer', 'referred', 'level']]
    
    def __str__(self):
        return f"{self.referrer.email} earned ${self.commission_earned} (Level {self.level})"
