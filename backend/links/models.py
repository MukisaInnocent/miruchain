"""
Models for business link management.
"""
import uuid
from django.db import models
from django.core.validators import MinValueValidator, URLValidator
from decimal import Decimal


class BusinessLink(models.Model):
    """
    Business links posted by users for advertising.
    """
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    )
    
    LINK_TYPE_CHOICES = (
        ('user_posted', 'User Posted'),
        ('admin_posted', 'Admin Posted'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Owner
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='business_links'
    )
    
    # Link details
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField(validators=[URLValidator()])
    image_url = models.URLField(blank=True, validators=[URLValidator()])
    category = models.CharField(max_length=100, blank=True)
    
    # Type and status
    link_type = models.CharField(
        max_length=20,
        choices=LINK_TYPE_CHOICES,
        default='user_posted'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # Earning settings (for admin links)
    earning_per_click = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    earning_per_conversion = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    # Statistics
    total_shares = models.IntegerField(default=0)
    total_clicks = models.IntegerField(default=0)
    total_conversions = models.IntegerField(default=0)
    
    # Moderation
    rejection_reason = models.TextField(blank=True)
    moderated_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='moderated_links'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'business_links'
        verbose_name = 'Business Link'
        verbose_name_plural = 'Business Links'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['status']),
            models.Index(fields=['link_type']),
            models.Index(fields=['category']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} by {self.user.full_name}"


class LinkShare(models.Model):
    """
    Tracks individual shares of business links.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Relationship
    business_link = models.ForeignKey(
        BusinessLink,
        on_delete=models.CASCADE,
        related_name='shares'
    )
    shared_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='shared_links'
    )
    
    # Unique share code for tracking
    share_code = models.CharField(max_length=50, unique=True, db_index=True)
    
    # Statistics
    clicks = models.IntegerField(default=0)
    conversions = models.IntegerField(default=0)
    total_earned = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    last_clicked_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'link_shares'
        verbose_name = 'Link Share'
        verbose_name_plural = 'Link Shares'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['business_link']),
            models.Index(fields=['shared_by']),
            models.Index(fields=['share_code']),
            models.Index(fields=['-created_at']),
        ]
        unique_together = [['business_link', 'shared_by']]
    
    def __str__(self):
        return f"{self.business_link.title} shared by {self.shared_by.full_name}"


class LinkClick(models.Model):
    """
    Tracks individual clicks on shared links.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Relationship
    link_share = models.ForeignKey(
        LinkShare,
        on_delete=models.CASCADE,
        related_name='click_records'
    )
    
    # Click metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True)
    
    # Conversion tracking
    is_conversion = models.BooleanField(default=False)
    conversion_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    # Timestamp
    clicked_at = models.DateTimeField(auto_now_add=True)
    converted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'link_clicks'
        verbose_name = 'Link Click'
        verbose_name_plural = 'Link Clicks'
        ordering = ['-clicked_at']
        indexes = [
            models.Index(fields=['link_share']),
            models.Index(fields=['is_conversion']),
            models.Index(fields=['-clicked_at']),
        ]
    
    def __str__(self):
        return f"Click on {self.link_share.business_link.title} at {self.clicked_at}"
