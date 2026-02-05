"""
Custom User model for MIRUCHAIN platform.
"""
import uuid
import secrets
import string
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class UserManager(BaseUserManager):
    """Custom user manager."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('membership_paid', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model with UUID primary key and referral fields.
    """
    # Override username (we use email for authentication)
    username = None
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Authentication
    email = models.EmailField(unique=True, db_index=True)
    
    # Profile Information
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Status Flags
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    # Membership
    membership_paid = models.BooleanField(default=False)
    membership_expiry = models.DateTimeField(null=True, blank=True)
    
    # Referral System
    referral_code = models.CharField(max_length=20, unique=True, db_index=True)
    referred_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='referrals',
        db_index=True
    )
    
    # Wallet
    wallet_balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    # Timestamps
    joined_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    # Manager
    objects = UserManager()
    
    # Use email as username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-joined_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['referral_code']),
            models.Index(fields=['referred_by']),
            models.Index(fields=['membership_paid']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        """Generate referral code if not exists."""
        if not self.referral_code:
            self.referral_code = self.generate_referral_code()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_referral_code(length=10):
        """Generate a unique referral code."""
        characters = string.ascii_uppercase + string.digits
        while True:
            code = ''.join(secrets.choice(characters) for _ in range(length))
            if not User.objects.filter(referral_code=code).exists():
                return code
    
    def get_referral_chain(self):
        """Get the upline referral chain."""
        chain = []
        current = self.referred_by
        while current:
            chain.append(current)
            current = current.referred_by
        return chain
    
    def get_direct_referrals(self):
        """Get all direct referrals (people this user referred)."""
        return self.referrals.filter(is_active=True)
    
    def get_referral_count(self):
        """Get total count of direct referrals."""
        return self.referrals.filter(membership_paid=True).count()
    
    def get_total_earnings(self):
        """Get total earnings from all sources."""
        from transactions.models import Transaction
        from django.db.models import Sum
        
        earnings = Transaction.objects.filter(
            user=self,
            transaction_type__in=['referral_commission', 'link_earning'],
            status='completed'
        ).aggregate(total=Sum('amount'))
        
        return earnings['total'] or Decimal('0.00')
    
    @property
    def is_membership_active(self):
        """Check if membership is currently active."""
        if not self.membership_paid:
            return False
        if self.membership_expiry is None:
            return True  # Lifetime membership
        from django.utils import timezone
        return timezone.now() < self.membership_expiry
