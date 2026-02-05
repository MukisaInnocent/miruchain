"""
Signal handlers for Users app.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    """
    Handle post-save actions for User model.
    """
    if created:
        # User created - could send welcome email here
        print(f"New user created: {instance.email}")
        
        # TODO: Send welcome email
        # TODO: Send email verification
        
        # Log referral if exists
        if instance.referred_by:
            print(f"User {instance.email} was referred by {instance.referred_by.email}")
