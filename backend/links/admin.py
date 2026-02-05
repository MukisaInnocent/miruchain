"""
Django admin configuration for Links app.
"""
from django.contrib import admin
from .models import BusinessLink, LinkShare, LinkClick


@admin.register(BusinessLink)
class BusinessLinkAdmin(admin.ModelAdmin):
    """Admin configuration for BusinessLink model."""
    
    list_display = (
        'title', 'user', 'category', 'link_type',
        'status', 'total_clicks', 'created_at'
    )
    list_filter = ('status', 'link_type', 'category', 'created_at')
    search_fields = ('title', 'description', 'user__email', 'user__full_name')
    readonly_fields = (
        'id', 'total_shares', 'total_clicks', 'total_conversions',
        'created_at', 'updated_at'
    )
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {
            'fields': ('id', 'user', 'link_type')
        }),
        ('Link Details', {
            'fields': ('title', 'description', 'url', 'image_url', 'category')
        }),
        ('Status', {
            'fields': ('status', 'rejection_reason', 'moderated_by', 'expires_at')
        }),
        ('Earnings (Admin Links)', {
            'fields': ('earning_per_click', 'earning_per_conversion')
        }),
        ('Statistics', {
            'fields': ('total_shares', 'total_clicks', 'total_conversions')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['approve_links', 'reject_links']
    
    def approve_links(self, request, queryset):
        """Approve selected links."""
        count = queryset.filter(status='pending').update(
            status='approved',
            moderated_by=request.user
        )
        self.message_user(request, f'{count} link(s) approved.')
    approve_links.short_description = 'Approve selected links'
    
    def reject_links(self, request, queryset):
        """Reject selected links."""
        count = queryset.filter(status='pending').update(
            status='rejected',
            moderated_by=request.user
        )
        self.message_user(request, f'{count} link(s) rejected.')
    reject_links.short_description = 'Reject selected links'


@admin.register(LinkShare)
class LinkShareAdmin(admin.ModelAdmin):
    """Admin configuration for LinkShare model."""
    
    list_display = (
        'business_link', 'shared_by', 'share_code',
        'clicks', 'conversions', 'total_earned', 'created_at'
    )
    list_filter = ('created_at',)
    search_fields = (
        'business_link__title', 'shared_by__email',
        'shared_by__full_name', 'share_code'
    )
    readonly_fields = (
        'id', 'share_code', 'clicks', 'conversions',
        'total_earned', 'created_at', 'last_clicked_at'
    )
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {
            'fields': ('id', 'business_link', 'shared_by')
        }),
        ('Tracking', {
            'fields': ('share_code',)
        }),
        ('Statistics', {
            'fields': ('clicks', 'conversions', 'total_earned')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'last_clicked_at')
        }),
    )


@admin.register(LinkClick)
class LinkClickAdmin(admin.ModelAdmin):
    """Admin configuration for LinkClick model."""
    
    list_display = (
        'link_share', 'ip_address', 'is_conversion', 
        'clicked_at'
    )
    list_filter = ('is_conversion', 'clicked_at')
    search_fields = ('link_share__share_code', 'ip_address')
    readonly_fields = fields = (
        'id', 'link_share', 'ip_address', 'user_agent', 'referrer',
        'is_conversion', 'conversion_value', 'clicked_at', 'converted_at'
    )
    ordering = ('-clicked_at',)
