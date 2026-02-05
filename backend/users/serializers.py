"""
Serializers for User model and authentication.
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    referral_code = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm', 'full_name', 'phone_number', 'referral_code')
    
    def validate(self, attrs):
        """Validate passwords match."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def validate_referral_code(self, value):
        """Validate referral code exists if provided."""
        if value:
            if not User.objects.filter(referral_code=value).exists():
                raise serializers.ValidationError("Invalid referral code.")
        return value
    
    def create(self, validated_data):
        """Create new user."""
        validated_data.pop('password_confirm')
        referral_code = validated_data.pop('referral_code', None)
        password = validated_data.pop('password')
        
        # Find referrer if code provided
        referred_by = None
        if referral_code:
            referred_by = User.objects.filter(referral_code=referral_code).first()
        
        user = User.objects.create_user(
            password=password,
            referred_by=referred_by,
            **validated_data
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile."""
    referrer = serializers.SerializerMethodField()
    direct_referrals_count = serializers.SerializerMethodField()
    total_earnings = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = (
            'id', 'email', 'full_name', 'phone_number', 'is_verified',
            'membership_paid', 'membership_expiry', 'referral_code',
            'wallet_balance', 'joined_at', 'referrer',
            'direct_referrals_count', 'total_earnings'
        )
        read_only_fields = (
            'id', 'email', 'is_verified', 'membership_paid', 'referral_code',
            'wallet_balance', 'joined_at'
        )
    
    def get_referrer(self, obj):
        """Get referrer information."""
        if obj.referred_by:
            return {
                'id': str(obj.referred_by.id),
                'full_name': obj.referred_by.full_name,
                'referral_code': obj.referred_by.referral_code
            }
        return None
    
    def get_direct_referrals_count(self, obj):
        """Get count of direct referrals."""
        return obj.get_referral_count()
    
    def get_total_earnings(self, obj):
        """Get total earnings."""
        return float(obj.get_total_earnings())


class UserDashboardSerializer(serializers.Serializer):
    """Serializer for dashboard statistics."""
    total_earnings = serializers.DecimalField(max_digits=10, decimal_places=2)
    wallet_balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_referrals = serializers.IntegerField()
    active_referrals = serializers.IntegerField()
    total_links = serializers.IntegerField()
    approved_links = serializers.IntegerField()
    total_clicks = serializers.IntegerField()
    total_conversions = serializers.IntegerField()
    earnings_breakdown = serializers.DictField()
    recent_earnings = serializers.ListField()


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change."""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        """Validate passwords match."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs
