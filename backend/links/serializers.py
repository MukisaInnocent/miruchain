"""
Serializers for Link data.
"""
from rest_framework import serializers
from .models import BusinessLink, LinkShare, LinkClick


class BusinessLinkSerializer(serializers.ModelSerializer):
    """Serializer for BusinessLink model."""
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = BusinessLink
        fields = (
            'id', 'user', 'user_name', 'user_email',
            'title', 'description', 'url', 'image_url', 'category',
            'link_type', 'status',
            'earning_per_click', 'earning_per_conversion',
            'total_shares', 'total_clicks', 'total_conversions',
            'created_at', 'updated_at', 'expires_at'
        )
        read_only_fields = (
            'id', 'user', 'link_type', 'status',
            'total_shares', 'total_clicks', 'total_conversions',
            'created_at', 'updated_at'
        )


class BusinessLinkCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating business links."""
    
    class Meta:
        model = BusinessLink
        fields = ('title', 'description', 'url', 'image_url', 'category')
    
    def validate_url(self, value):
        """Validate URL format."""
        if not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError('URL must start with http:// or https://')
        return value


class LinkShareSerializer(serializers.ModelSerializer):
    """Serializer for LinkShare model."""
    business_link_title = serializers.CharField(source='business_link.title', read_only=True)
    business_link_url = serializers.URLField(source='business_link.url', read_only=True)
    shared_by_name = serializers.CharField(source='shared_by.full_name', read_only=True)
    share_url = serializers.SerializerMethodField()
    
    class Meta:
        model = LinkShare
        fields = (
            'id', 'business_link', 'business_link_title', 'business_link_url',
            'shared_by', 'shared_by_name',
            'share_code', 'share_url',
            'clicks', 'conversions', 'total_earned',
            'created_at', 'last_clicked_at'
        )
        read_only_fields = fields
    
    def get_share_url(self, obj):
        """Generate shareable URL."""
        from django.conf import settings
        return f"{settings.FRONTEND_URL}/link/{obj.share_code}"


class LinkClickSerializer(serializers.ModelSerializer):
    """Serializer for LinkClick model."""
    
    class Meta:
        model = LinkClick
        fields = (
            'id', 'link_share', 'ip_address', 'user_agent', 'referrer',
            'is_conversion', 'conversion_value',
            'clicked_at', 'converted_at'
        )
        read_only_fields = fields


class LinkStatsSerializer(serializers.Serializer):
    """Serializer for link statistics."""
    total_links = serializers.IntegerField()
    approved_links = serializers.IntegerField()
    pending_links = serializers.IntegerField()
    total_shares = serializers.IntegerField()
    total_clicks = serializers.IntegerField()
    total_conversions = serializers.IntegerField()
    total_earned = serializers.DecimalField(max_digits=10, decimal_places=2)
