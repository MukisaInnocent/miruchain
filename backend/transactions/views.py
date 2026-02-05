"""
Views for transaction and payment management.
"""
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.db import transaction as db_transaction
from django.conf import settings
from django.utils import timezone
from decimal import Decimal

from .models import Transaction, WithdrawalRequest
from .serializers import (
    TransactionSerializer,
    WithdrawalRequestSerializer,
    WithdrawalDetailSerializer,
    PaymentIntentSerializer
)


class TransactionListView(generics.ListAPIView):
    """
    List all transactions for current user.
    
    GET /api/v1/transactions
    """
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # Filter by type if provided
        transaction_type = request.query_params.get('type')
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        
        # Filter by status if provided
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'success': True,
                'data': serializer.data
            })
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })


class CreatePaymentIntentView(APIView):
    """
    Create a payment intent for Stripe.
    
    POST /api/v1/transactions/create-payment-intent
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = PaymentIntentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        amount = serializer.validated_data['amount']
        payment_type = serializer.validated_data['payment_type']
        description = serializer.validated_data.get('description', '')
        
        # Create transaction record
        transaction_type = 'membership_payment' if payment_type == 'membership' else 'advertising_payment'
        
        transaction_obj = Transaction.objects.create(
            user=request.user,
            transaction_type=transaction_type,
            amount=amount,
            status='pending',
            description=description or f'{payment_type.title()} payment',
            payment_method='stripe'
        )
        
        # TODO: Create Stripe payment intent
        # For now, return mock data
        # import stripe
        # stripe.api_key = settings.STRIPE_SECRET_KEY
        # intent = stripe.PaymentIntent.create(
        #     amount=int(amount * 100),  # Convert to cents
        #     currency='usd',
        #     metadata={'transaction_id': str(transaction_obj.id)}
        # )
        
        return Response({
            'success': True,
            'data': {
                'transaction_id': str(transaction_obj.id),
                'amount': float(amount),
                'client_secret': 'mock_client_secret_' + str(transaction_obj.id),
                'publishable_key': settings.STRIPE_PUBLIC_KEY
            }
        })


class ConfirmPaymentView(APIView):
    """
    Confirm a payment after Stripe processing.
    
    POST /api/v1/transactions/confirm-payment
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @db_transaction.atomic
    def post(self, request):
        transaction_id = request.data.get('transaction_id')
        payment_id = request.data.get('payment_id')
        
        if not transaction_id:
            return Response({
                'success': False,
                'message': 'Transaction ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            transaction_obj = Transaction.objects.get(
                id=transaction_id,
                user=request.user,
                status='pending'
            )
        except Transaction.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Transaction not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Update transaction
        transaction_obj.status = 'completed'
        transaction_obj.payment_id = payment_id
        transaction_obj.completed_at = timezone.now()
        transaction_obj.save()
        
        # Handle membership payment
        if transaction_obj.transaction_type == 'membership_payment':
            user = request.user
            user.membership_paid = True
            user.save(update_fields=['membership_paid'])
            
            # Distribute referral commissions
            from referrals.services import ReferralService
            ReferralService.distribute_commissions(user, transaction_obj.amount)
        
        return Response({
            'success': True,
            'message': 'Payment confirmed successfully',
            'data': TransactionSerializer(transaction_obj).data
        })


class WithdrawalRequestCreateView(generics.CreateAPIView):
    """
    Create a withdrawal request.
    
    POST /api/v1/transactions/withdrawal
    """
    serializer_class = WithdrawalRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @db_transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        amount = serializer.validated_data['amount']
        fee = Decimal(settings.WITHDRAWAL_FEE)
        net_amount = amount - fee
        
        # Create withdrawal request
        withdrawal = WithdrawalRequest.objects.create(
            user=request.user,
            amount=amount,
            fee=fee,
            net_amount=net_amount,
            payment_method=serializer.validated_data['payment_method'],
            payment_details=serializer.validated_data['payment_details'],
            status='pending'
        )
        
        # Create transaction record
        transaction_obj = Transaction.objects.create(
            user=request.user,
            transaction_type='withdrawal',
            amount=amount,
            status='pending',
            description=f'Withdrawal request - {withdrawal.payment_method}'
        )
        
        withdrawal.transaction = transaction_obj
        withdrawal.save(update_fields=['transaction'])
        
        # Deduct from wallet (pending)
        user = request.user
        user.wallet_balance -= amount
        user.save(update_fields=['wallet_balance'])
        
        return Response({
            'success': True,
            'message': 'Withdrawal request submitted successfully',
            'data': WithdrawalDetailSerializer(withdrawal).data
        }, status=status.HTTP_201_CREATED)


class WithdrawalRequestListView(generics.ListAPIView):
    """
    List withdrawal requests for current user.
    
    GET /api/v1/transactions/withdrawals
    """
    serializer_class = WithdrawalDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return WithdrawalRequest.objects.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'success': True,
                'data': serializer.data
            })
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_transaction_summary(request):
    """
    Get transaction summary for current user.
    
    GET /api/v1/transactions/summary
    """
    from django.db.models import Sum, Count
    
    user = request.user
    
    # Total earnings
    earnings = Transaction.objects.filter(
        user=user,
        transaction_type__in=['referral_commission', 'link_earning'],
        status='completed'
    ).aggregate(total=Sum('amount'))
    
    # Total spent
    spent = Transaction.objects.filter(
        user=user,
        transaction_type__in=['membership_payment', 'advertising_payment'],
        status='completed'
    ).aggregate(total=Sum('amount'))
    
    # Total withdrawn
    withdrawn = Transaction.objects.filter(
        user=user,
        transaction_type='withdrawal',
        status='completed'
    ).aggregate(total=Sum('amount'))
    
    # Pending withdrawals
    pending_withdrawals = WithdrawalRequest.objects.filter(
        user=user,
        status__in=['pending', 'approved', 'processing']
    ).aggregate(total=Sum('amount'))
    
    # Transaction counts by type
    counts = Transaction.objects.filter(
        user=user
    ).values('transaction_type').annotate(count=Count('id'))
    
    return Response({
        'success': True,
        'data': {
            'total_earnings': float(earnings['total'] or 0),
            'total_spent': float(spent['total'] or 0),
            'total_withdrawn': float(withdrawn['total'] or 0),
            'pending_withdrawals': float(pending_withdrawals['total'] or 0),
            'current_balance': float(user.wallet_balance),
            'transaction_counts': list(counts)
        }
    })
