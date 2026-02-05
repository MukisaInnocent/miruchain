"""
Views for User authentication and management.
"""
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from django.db.models import Sum, Count, Q
from decimal import Decimal
from datetime import datetime, timedelta

from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
    UserDashboardSerializer,
    ChangePasswordSerializer
)


class UserRegistrationView(generics.CreateAPIView):
    """
    Register a new user.
    
    POST /api/v1/auth/register
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Get membership fee from settings
        from django.conf import settings
        membership_fee = settings.MEMBERSHIP_FEE
        
        # Generate payment URL (placeholder - will be implemented in transactions app)
        payment_url = f"{settings.FRONTEND_URL}/payment/{user.id}"
        
        return Response({
            'success': True,
            'message': 'Registration successful. Please complete payment to activate your account.',
            'data': {
                'user_id': str(user.id),
                'email': user.email,
                'full_name': user.full_name,
                'referral_code': user.referral_code,
                'payment_required': True,
                'payment_amount': float(membership_fee),
                'payment_url': payment_url
            }
        }, status=status.HTTP_201_CREATED)


class UserLoginView(TokenObtainPairView):
    """
    Login user and return JWT tokens.
    
    POST /api/v1/auth/login
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({
                'success': False,
                'message': 'Email and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, username=email, password=password)
        
        if user is None:
            return Response({
                'success': False,
                'message': 'Invalid email or password'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_active:
            return Response({
                'success': False,
                'message': 'Account is deactivated. Please contact support.'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        # Update last login
        user.last_login = datetime.now()
        user.save(update_fields=['last_login'])
        
        return Response({
            'success': True,
            'data': {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'token_type': 'Bearer',
                'expires_in': 3600,  # 1 hour
                'user': {
                    'id': str(user.id),
                    'email': user.email,
                    'full_name': user.full_name,
                    'is_admin': user.is_admin,
                    'membership_paid': user.membership_paid
                }
            }
        }, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Get or update current user's profile.
    
    GET /api/v1/users/me
    PATCH /api/v1/users/me
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'success': True,
            'message': 'Profile updated successfully',
            'data': serializer.data
        })


class UserDashboardView(APIView):
    """
    Get dashboard statistics for current user.
    
    GET /api/v1/users/me/dashboard
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Import models here to avoid circular imports
        from referrals.models import Referral
        from links.models import BusinessLink, LinkShare
        from transactions.models import Transaction
        
        # Get referral counts
        total_referrals = user.referrals.filter(membership_paid=True).count()
        active_referrals = user.referrals.filter(
            membership_paid=True,
            is_active=True
        ).count()
        
        # Get link counts
        total_links = BusinessLink.objects.filter(user=user).count()
        approved_links = BusinessLink.objects.filter(
            user=user,
            status='approved'
        ).count()
        
        # Get link statistics
        user_shares = LinkShare.objects.filter(shared_by=user)
        total_clicks = user_shares.aggregate(total=Sum('clicks'))['total'] or 0
        total_conversions = user_shares.aggregate(total=Sum('conversions'))['total'] or 0
        
        # Get earnings breakdown
        transactions = Transaction.objects.filter(
            user=user,
            status='completed'
        )
        
        referral_commissions = transactions.filter(
            transaction_type='referral_commission'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        link_earnings = transactions.filter(
            transaction_type='link_earning'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        total_earnings = referral_commissions + link_earnings
        
        # Get recent earnings (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_earnings_data = transactions.filter(
            transaction_type__in=['referral_commission', 'link_earning'],
            created_at__gte=thirty_days_ago
        ).extra(
            select={'date': 'DATE(created_at)'}
        ).values('date').annotate(
            amount=Sum('amount')
        ).order_by('date')
        
        recent_earnings = [
            {
                'date': item['date'].strftime('%Y-%m-%d'),
                'amount': float(item['amount'])
            }
            for item in recent_earnings_data
        ]
        
        # Prepare dashboard data
        dashboard_data = {
            'total_earnings': total_earnings,
            'wallet_balance': user.wallet_balance,
            'total_referrals': total_referrals,
            'active_referrals': active_referrals,
            'total_links': total_links,
            'approved_links': approved_links,
            'total_clicks': total_clicks,
            'total_conversions': total_conversions,
            'earnings_breakdown': {
                'direct_referral_commissions': float(referral_commissions),
                'upline_referral_commissions': 0,  # TODO: Implement in referrals app
                'link_earnings': float(link_earnings)
            },
            'recent_earnings': recent_earnings
        }
        
        serializer = UserDashboardSerializer(data=dashboard_data)
        serializer.is_valid(raise_exception=True)
        
        return Response({
            'success': True,
            'data': serializer.data
        })


class ChangePasswordView(APIView):
    """
    Change user password.
    
    POST /api/v1/users/me/change-password
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        
        # Check old password
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({
                'success': False,
                'message': 'Old password is incorrect'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Set new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'success': True,
            'message': 'Password changed successfully'
        })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def verify_referral_code(request):
    """
    Verify if a referral code is valid.
    
    POST /api/v1/auth/verify-referral-code
    """
    referral_code = request.data.get('referral_code')
    
    if not referral_code:
        return Response({
            'success': False,
            'message': 'Referral code is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(referral_code=referral_code)
        return Response({
            'success': True,
            'data': {
                'valid': True,
                'referrer': {
                    'full_name': user.full_name,
                    'referral_code': user.referral_code
                }
            }
        })
    except User.DoesNotExist:
        return Response({
            'success': False,
            'data': {
                'valid': False
            }
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def request_password_reset(request):
    """
    Request password reset email.
    
    POST /api/v1/auth/forgot-password
    """
    email = request.data.get('email')
    
    if not email:
        return Response({
            'success': False,
            'message': 'Email is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
        # TODO: Implement password reset email sending
        # For now, just return success
        return Response({
            'success': True,
            'message': 'Password reset link sent to your email'
        })
    except User.DoesNotExist:
        # Don't reveal if email exists or not (security)
        return Response({
            'success': True,
            'message': 'Password reset link sent to your email'
        })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_referral_link(request):
    """
    Get user's unique referral link.
    
    GET /api/v1/users/me/referral-link
    """
    user = request.user
    from django.conf import settings
    
    referral_url = f"{settings.FRONTEND_URL}/register?ref={user.referral_code}"
    
    return Response({
        'success': True,
        'data': {
            'referral_code': user.referral_code,
            'referral_url': referral_url,
            'total_referrals': user.get_referral_count()
        }
    })
