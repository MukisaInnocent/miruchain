"""
Admin panel views for platform management.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Sum, Count, Q
from django.db import transaction as db_transaction
from django.utils import timezone
from decimal import Decimal

from .permissions import IsAdminUser
from users.models import User
from referrals.models import Referral
from links.models import BusinessLink, LinkShare
from transactions.models import Transaction, WithdrawalRequest


class DashboardStatsView(APIView):
    """
    Get overall platform statistics for admin dashboard.
    
    GET /api/v1/admin/dashboard
    """
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        # User statistics
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        paid_members = User.objects.filter(membership_paid=True).count()
        new_users_today = User.objects.filter(
            joined_at__date=timezone.now().date()
        ).count()
        
        # Transaction statistics
        total_revenue = Transaction.objects.filter(
            transaction_type__in=['membership_payment', 'advertising_payment'],
            status='completed'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        total_paid_out = Transaction.objects.filter(
            transaction_type__in=['referral_commission', 'link_earning'],
            status='completed'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        # Link statistics
        total_links = BusinessLink.objects.count()
        approved_links = BusinessLink.objects.filter(status='approved').count()
        pending_links = BusinessLink.objects.filter(status='pending').count()
        
        # Withdrawal statistics
        pending_withdrawals = WithdrawalRequest.objects.filter(
            status='pending'
        ).count()
        pending_withdrawal_amount = WithdrawalRequest.objects.filter(
            status='pending'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        return Response({
            'success': True,
            'data': {
                'users': {
                    'total': total_users,
                    'active': active_users,
                    'paid_members': paid_members,
                    'new_today': new_users_today
                },
                'revenue': {
                    'total_revenue': float(total_revenue),
                    'total_paid_out': float(total_paid_out),
                    'net_revenue': float(total_revenue - total_paid_out)
                },
                'links': {
                    'total': total_links,
                    'approved': approved_links,
                    'pending': pending_links
                },
                'withdrawals': {
                    'pending_count': pending_withdrawals,
                    'pending_amount': float(pending_withdrawal_amount)
                }
            }
        })


class UserManagementView(APIView):
    """
    Get list of users with filtering.
    
    GET /api/v1/admin/users
    """
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        users = User.objects.all()
        
        # Filter by status
        status_filter = request.query_params.get('status')
        if status_filter == 'active':
            users = users.filter(is_active=True)
        elif status_filter == 'inactive':
            users = users.filter(is_active=False)
        elif status_filter == 'paid':
            users = users.filter(membership_paid=True)
        
        # Search
        search = request.query_params.get('search')
        if search:
            users = users.filter(
                Q(email__icontains=search) |
                Q(full_name__icontains=search)
            )
        
        # Serialize
        users_data = []
        for user in users[:100]:  # Limit to 100 for performance
            users_data.append({
                'id': str(user.id),
                'email': user.email,
                'full_name': user.full_name,
                'is_active': user.is_active,
                'is_verified': user.is_verified,
                'membership_paid': user.membership_paid,
                'wallet_balance': float(user.wallet_balance),
                'referral_code': user.referral_code,
                'total_referrals': user.get_referral_count(),
                'joined_at': user.joined_at
            })
        
        return Response({
            'success': True,
            'data': users_data,
            'total': users.count()
        })


class ModerateLinksView(APIView):
    """
    Get pending links for moderation.
    
    GET /api/v1/admin/links/pending
    """
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        pending_links = BusinessLink.objects.filter(
            status='pending'
        ).select_related('user')
        
        links_data = []
        for link in pending_links:
            links_data.append({
                'id': str(link.id),
                'title': link.title,
                'description': link.description,
                'url': link.url,
                'image_url': link.image_url,
                'category': link.category,
                'user': {
                    'id': str(link.user.id),
                    'email': link.user.email,
                    'full_name': link.user.full_name
                },
                'created_at': link.created_at
            })
        
        return Response({
            'success': True,
            'data': links_data
        })


class ApproveLinkView(APIView):
    """
    Approve a business link.
    
    POST /api/v1/admin/links/{link_id}/approve
    """
    permission_classes = [IsAdminUser]
    
    def post(self, request, link_id):
        try:
            link = BusinessLink.objects.get(id=link_id, status='pending')
        except BusinessLink.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Link not found or already moderated'
            }, status=status.HTTP_404_NOT_FOUND)
        
        link.status = 'approved'
        link.moderated_by = request.user
        link.save(update_fields=['status', 'moderated_by'])
        
        return Response({
            'success': True,
            'message': 'Link approved successfully'
        })


class RejectLinkView(APIView):
    """
    Reject a business link.
    
    POST /api/v1/admin/links/{link_id}/reject
    """
    permission_classes = [IsAdminUser]
    
    def post(self, request, link_id):
        try:
            link = BusinessLink.objects.get(id=link_id, status='pending')
        except BusinessLink.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Link not found or already moderated'
            }, status=status.HTTP_404_NOT_FOUND)
        
        reason = request.data.get('reason', '')
        
        link.status = 'rejected'
        link.rejection_reason = reason
        link.moderated_by = request.user
        link.save(update_fields=['status', 'rejection_reason', 'moderated_by'])
        
        return Response({
            'success': True,
            'message': 'Link rejected successfully'
        })


class PendingWithdrawalsView(APIView):
    """
    Get pending withdrawal requests.
    
    GET /api/v1/admin/withdrawals/pending
    """
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        withdrawals = WithdrawalRequest.objects.filter(
            status='pending'
        ).select_related('user')
        
        withdrawals_data = []
        for withdrawal in withdrawals:
            withdrawals_data.append({
                'id': str(withdrawal.id),
                'user': {
                    'id': str(withdrawal.user.id),
                    'email': withdrawal.user.email,
                    'full_name': withdrawal.user.full_name
                },
                'amount': float(withdrawal.amount),
                'fee': float(withdrawal.fee),
                'net_amount': float(withdrawal.net_amount),
                'payment_method': withdrawal.payment_method,
                'payment_details': withdrawal.payment_details,
                'created_at': withdrawal.created_at
            })
        
        return Response({
            'success': True,
            'data': withdrawals_data
        })


class ApproveWithdrawalView(APIView):
    """
    Approve a withdrawal request.
    
    POST /api/v1/admin/withdrawals/{withdrawal_id}/approve
    """
    permission_classes = [IsAdminUser]
    
    @db_transaction.atomic
    def post(self, request, withdrawal_id):
        try:
            withdrawal = WithdrawalRequest.objects.get(
                id=withdrawal_id,
                status='pending'
            )
        except WithdrawalRequest.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Withdrawal not found or already processed'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Update withdrawal status
        withdrawal.status = 'approved'
        withdrawal.approved_by = request.user
        withdrawal.save(update_fields=['status', 'approved_by'])
        
        # Update transaction
        if withdrawal.transaction:
            withdrawal.transaction.status = 'completed'
            withdrawal.transaction.completed_at = timezone.now()
            withdrawal.transaction.save(update_fields=['status', 'completed_at'])
        
        return Response({
            'success': True,
            'message': 'Withdrawal approved successfully'
        })


class RejectWithdrawalView(APIView):
    """
    Reject a withdrawal request.
    
    POST /api/v1/admin/withdrawals/{withdrawal_id}/reject
    """
    permission_classes = [IsAdminUser]
    
    @db_transaction.atomic
    def post(self, request, withdrawal_id):
        try:
            withdrawal = WithdrawalRequest.objects.get(
                id=withdrawal_id,
                status='pending'
            )
        except WithdrawalRequest.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Withdrawal not found or already processed'
            }, status=status.HTTP_404_NOT_FOUND)
        
        reason = request.data.get('reason', '')
        
        # Refund amount to user wallet
        user = withdrawal.user
        user.wallet_balance += withdrawal.amount
        user.save(update_fields=['wallet_balance'])
        
        # Update withdrawal status
        withdrawal.status = 'rejected'
        withdrawal.rejection_reason = reason
        withdrawal.save(update_fields=['status', 'rejection_reason'])
        
        # Update transaction
        if withdrawal.transaction:
            withdrawal.transaction.status = 'cancelled'
            withdrawal.transaction.save(update_fields=['status'])
        
        return Response({
            'success': True,
            'message': 'Withdrawal rejected and amount refunded to user wallet'
        })
