"""
Serializers for Transaction data.
"""
from rest_framework import serializers
from .models import Transaction, WithdrawalRequest
from django.conf import settings


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model."""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = Transaction
        fields = (
            'id', 'user', 'user_email', 'user_name',
            'transaction_type', 'amount', 'status',
            'description', 'payment_method', 'payment_id',
            'created_at', 'updated_at', 'completed_at'
        )
        read_only_fields = (
            'id', 'user', 'status', 'payment_id',
            'created_at', 'updated_at', 'completed_at'
        )


class WithdrawalRequestSerializer(serializers.ModelSerializer):
    """Serializer for creating withdrawal requests."""
    
    class Meta:
        model = WithdrawalRequest
        fields = (
            'id', 'amount', 'payment_method', 'payment_details',
            'status', 'created_at'
        )
        read_only_fields = ('id', 'status', 'created_at')
    
    def validate_amount(self, value):
        """Validate withdrawal amount."""
        user = self.context['request'].user
        min_withdrawal = settings.MINIMUM_WITHDRAWAL
        
        if value < min_withdrawal:
            raise serializers.ValidationError(
                f'Minimum withdrawal amount is ${min_withdrawal}'
            )
        
        if value > user.wallet_balance:
            raise serializers.ValidationError(
                f'Insufficient balance. Available: ${user.wallet_balance}'
            )
        
        return value
    
    def validate_payment_details(self, value):
        """Validate payment details are provided."""
        if not value:
            raise serializers.ValidationError('Payment details are required')
        return value


class WithdrawalDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for withdrawal requests."""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.full_name', read_only=True, allow_null=True)
    
    class Meta:
        model = WithdrawalRequest
        fields = (
            'id', 'user', 'user_email', 'user_name',
            'amount', 'fee', 'net_amount',
            'payment_method', 'payment_details',
            'status', 'rejection_reason',
            'approved_by', 'approved_by_name',
            'created_at', 'updated_at', 'completed_at'
        )
        read_only_fields = fields


class PaymentIntentSerializer(serializers.Serializer):
    """Serializer for creating payment intents."""
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_type = serializers.ChoiceField(choices=['membership', 'advertising'])
    description = serializers.CharField(required=False, allow_blank=True)
