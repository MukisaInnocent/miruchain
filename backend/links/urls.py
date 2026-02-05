"""
URL configuration for Links app.
"""
from django.urls import path
from . import views

app_name = 'links'

urlpatterns = [
    # Business links
    path('', views.BusinessLinkListView.as_view(), name='list'),
    path('create', views.BusinessLinkCreateView.as_view(), name='create'),
    path('my-links', views.MyBusinessLinksView.as_view(), name='my_links'),
    path('<uuid:pk>', views.BusinessLinkDetailView.as_view(), name='detail'),
    
    # Sharing
    path('<uuid:link_id>/share', views.ShareLinkView.as_view(), name='share'),
    path('my-shares', views.MySharedLinksView.as_view(), name='my_shares'),
    
    # Tracking
    path('track/<str:share_code>', views.track_click, name='track_click'),
    
    # Statistics
    path('stats', views.get_link_stats, name='stats'),
]
