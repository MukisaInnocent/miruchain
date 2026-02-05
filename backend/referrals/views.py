"""
Views for referral management and statistics.
"""
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes

from .models import Referral
from .serializers import (
    ReferralSerializer,
    ReferralTreeNodeSerializer,
    ReferralChainSerializer,
    CommissionStatsSerializer
)
from .services import ReferralService


class ReferralListView(generics.ListAPIView):
    """
    List all referral commissions for current user.
    
    GET /api/v1/referrals
    """
    serializer_class = ReferralSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Referral.objects.filter(
            referrer=self.request.user
        ).select_related('referred')
    
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


class ReferralTreeView(APIView):
    """
    Get referral tree (downline) for current user.
    
    GET /api/v1/referrals/tree?depth=3
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        max_depth = int(request.query_params.get('depth', 3))
        max_depth = min(max_depth, 5)  # Limit to 5 levels max
        
        tree = ReferralService.get_referral_tree(request.user, max_depth=max_depth)
        
        return Response({
            'success': True,
            'data': {
                'user': {
                    'full_name': request.user.full_name,
                    'email': request.user.email,
                    'referral_code': request.user.referral_code
                },
                'referral_tree': tree,
                'max_depth': max_depth
            }
        })


class ReferralChainView(APIView):
    """
    Get referral chain (upline) for current user.
    
    GET /api/v1/referrals/chain
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        chain = ReferralService.get_referral_chain(request.user)
        serializer = ReferralChainSerializer(chain, many=True)
        
        return Response({
            'success': True,
            'data': {
                'chain': serializer.data,
                'chain_length': len(chain)
            }
        })


class CommissionStatsView(APIView):
    """
    Get commission statistics for current user.
    
    GET /api/v1/referrals/stats
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        stats = ReferralService.get_commission_stats(request.user)
        serializer = CommissionStatsSerializer(data=stats)
        serializer.is_valid(raise_exception=True)
        
        return Response({
            'success': True,
            'data': serializer.data
        })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_direct_referrals(request):
    """
    Get list of direct referrals (level 1 only).
    
    GET /api/v1/referrals/direct
    """
    direct_referrals = request.user.get_direct_referrals()
    
    referrals_data = []
    for referral in direct_referrals:
        # Get commission earned from this referral
        commission = Referral.objects.filter(
            referrer=request.user,
            referred=referral,
            level=1
        ).first()
        
        referrals_data.append({
            'id': str(referral.id),
            'full_name': referral.full_name,
            'email': referral.email,
            'joined_at': referral.joined_at,
            'is_active': referral.is_active,
            'commission_earned': float(commission.commission_earned) if commission else 0.00,
            'total_referrals': referral.get_referral_count()
        })
    
    return Response({
        'success': True,
        'data': {
            'total_count': len(referrals_data),
            'referrals': referrals_data
        }
    })
