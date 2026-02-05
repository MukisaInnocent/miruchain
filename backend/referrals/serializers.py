"""
Serializers for Referral data.
"""
from rest_framework import serializers
from .models import Referral


class ReferralSerializer(serializers.ModelSerializer):
    """Serializer for Referral model."""
    referrer_name = serializers.CharField(source='referrer.full_name', read_only=True)
    referrer_email = serializers.EmailField(source='referrer.email', read_only=True)
    referred_name = serializers.CharField(source='referred.full_name', read_only=True)
    referred_email = serializers.EmailField(source='referred.email', read_only=True)
    
    class Meta:
        model = Referral
        fields = (
            'id', 'referrer', 'referrer_name', 'referrer_email',
            'referred', 'referred_name', 'referred_email',
            'level', 'commission_earned', 'created_at'
        )
        read_only_fields = fields


class ReferralTreeNodeSerializer(serializers.Serializer):
    """Serializer for referral tree nodes."""
    id = serializers.UUIDField()
    full_name = serializers.CharField()
    email = serializers.EmailField()
    joined_at = serializers.DateTimeField()
    is_active = serializers.BooleanField()
    commission_earned = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)
    direct_referrals = serializers.ListField(child=serializers.DictField(), required=False)


class ReferralChainSerializer(serializers.Serializer):
    """Serializer for upline referral chain."""
    level = serializers.IntegerField()
    referral_code = serializers.CharField()
    full_name = serializers.CharField()
    email = serializers.EmailField()


class CommissionStatsSerializer(serializers.Serializer):
    """Serializer for commission statistics."""
    total_commissions = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_count = serializers.IntegerField()
    direct_commissions = serializers.DecimalField(max_digits=10, decimal_places=2)
    direct_count = serializers.IntegerField()
    upline_commissions = serializers.DecimalField(max_digits=10, decimal_places=2)
    upline_count = serializers.IntegerField()
    by_level = serializers.ListField()
