"""
Views for business link management.
"""
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.db import transaction as db_transaction
from django.utils import timezone
from django.db.models import Sum, Count
import secrets
import string
from decimal import Decimal

from .models import BusinessLink, LinkShare, LinkClick
from .serializers import (
    BusinessLinkSerializer,
    BusinessLinkCreateSerializer,
    LinkShareSerializer,
    LinkClickSerializer,
    LinkStatsSerializer
)


class BusinessLinkListView(generics.ListAPIView):
    """
    List all approved business links (public directory).
    
    GET /api/v1/links
    """
    serializer_class = BusinessLinkSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = BusinessLink.objects.filter(status='approved')
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Search by title or description
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) | 
                models.Q(description__icontains=search)
            )
        
        return queryset
    
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


class MyBusinessLinksView(generics.ListAPIView):
    """
    List current user's business links.
    
    GET /api/v1/links/my-links
    """
    serializer_class = BusinessLinkSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return BusinessLink.objects.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })


class BusinessLinkCreateView(generics.CreateAPIView):
    """
    Create a new business link.
    
    POST /api/v1/links
    """
    serializer_class = BusinessLinkCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        # Check if user has paid membership
        if not request.user.membership_paid:
            return Response({
                'success': False,
                'message': 'Membership payment required to post links'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create link
        link = BusinessLink.objects.create(
            user=request.user,
            **serializer.validated_data
        )
        
        return Response({
            'success': True,
            'message': 'Business link submitted for review',
            'data': BusinessLinkSerializer(link).data
        }, status=status.HTTP_201_CREATED)


class BusinessLinkDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, update, or delete a business link.
    
    GET/PUT/DELETE /api/v1/links/{id}
    """
    serializer_class = BusinessLinkSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return BusinessLink.objects.filter(user=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Can only update pending links
        if instance.status != 'pending':
            return Response({
                'success': False,
                'message': 'Can only update pending links'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return super().update(request, *args, **kwargs)


class ShareLinkView(APIView):
    """
    Create a share for a business link.
    
    POST /api/v1/links/{link_id}/share
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @db_transaction.atomic
    def post(self, request, link_id):
        try:
            business_link = BusinessLink.objects.get(
                id=link_id,
                status='approved'
            )
        except BusinessLink.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Link not found or not approved'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check if already shared
        existing_share = LinkShare.objects.filter(
            business_link=business_link,
            shared_by=request.user
        ).first()
        
        if existing_share:
            return Response({
                'success': True,
                'message': 'You have already shared this link',
                'data': LinkShareSerializer(existing_share).data
            })
        
        # Generate unique share code
        share_code = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
        
        # Create share
        link_share = LinkShare.objects.create(
            business_link=business_link,
            shared_by=request.user,
            share_code=share_code
        )
        
        # Update link stats
        business_link.total_shares += 1
        business_link.save(update_fields=['total_shares'])
        
        return Response({
            'success': True,
            'message': 'Link shared successfully',
            'data': LinkShareSerializer(link_share).data
        }, status=status.HTTP_201_CREATED)


class MySharedLinksView(generics.ListAPIView):
    """
    List all links shared by current user.
    
    GET /api/v1/links/my-shares
    """
    serializer_class = LinkShareSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return LinkShare.objects.filter(shared_by=self.request.user).select_related('business_link')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def track_click(request, share_code):
    """
    Track a click on a shared link.
    
    POST /api/v1/links/track/{share_code}
    """
    try:
        link_share = LinkShare.objects.select_related('business_link', 'shared_by').get(
            share_code=share_code
        )
    except LinkShare.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Invalid share code'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Get IP and user agent
    ip_address = request.META.get('REMOTE_ADDR')
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    referrer = request.META.get('HTTP_REFERER', '')
    
    # Create click record
    link_click = LinkClick.objects.create(
        link_share=link_share,
        ip_address=ip_address,
        user_agent=user_agent,
        referrer=referrer
    )
    
    # Update statistics
    link_share.clicks += 1
    link_share.last_clicked_at = timezone.now()
    link_share.save(update_fields=['clicks', 'last_clicked_at'])
    
    link_share.business_link.total_clicks += 1
    link_share.business_link.save(update_fields=['total_clicks'])
    
    # Calculate earnings if applicable
    earning = link_share.business_link.earning_per_click
    if earning > 0:
        # Credit user wallet
        link_share.shared_by.wallet_balance += earning
        link_share.shared_by.save(update_fields=['wallet_balance'])
        
        # Update share earnings
        link_share.total_earned += earning
        link_share.save(update_fields=['total_earned'])
        
        # Create transaction
        from transactions.models import Transaction
        Transaction.objects.create(
            user=link_share.shared_by,
            transaction_type='link_earning',
            amount=earning,
            status='completed',
            description=f'Click earning from {link_share.business_link.title}'
        )
    
    return Response({
        'success': True,
        'data': {
            'redirect_url': link_share.business_link.url,
            'earning': float(earning)
        }
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_link_stats(request):
    """
    Get link statistics for current user.
    
    GET /api/v1/links/stats
    """
    user = request.user
    
    # My posted links
    my_links = BusinessLink.objects.filter(user=user)
    total_links = my_links.count()
    approved_links = my_links.filter(status='approved').count()
    pending_links = my_links.filter(status='pending').count()
    
    # My shared links
    my_shares = LinkShare.objects.filter(shared_by=user)
    total_shares = my_shares.count()
    
    # Aggregated stats
    share_stats = my_shares.aggregate(
        total_clicks=Sum('clicks'),
        total_conversions=Sum('conversions'),
        total_earned=Sum('total_earned')
    )
    
    stats_data = {
        'total_links': total_links,
        'approved_links': approved_links,
        'pending_links': pending_links,
        'total_shares': total_shares,
        'total_clicks': share_stats['total_clicks'] or 0,
        'total_conversions': share_stats['total_conversions'] or 0,
        'total_earned': share_stats['total_earned'] or Decimal('0.00')
    }
    
    serializer = LinkStatsSerializer(data=stats_data)
    serializer.is_valid(raise_exception=True)
    
    return Response({
        'success': True,
        'data': serializer.data
    })
