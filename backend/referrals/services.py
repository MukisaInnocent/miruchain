"""
Service layer for referral commission calculations.
"""
from decimal import Decimal
from django.db import transaction
from django.conf import settings

from .models import Referral
from users.models import User
from transactions.models import Transaction


class ReferralService:
    """Service class for handling referral commission logic."""
    
    # Commission rates from settings
    DIRECT_COMMISSION_RATE = Decimal(settings.DIRECT_COMMISSION_RATE)
    UPLINE_POOL_RATE = Decimal(settings.UPLINE_POOL_RATE)
    UPLINE_SPLIT_RATE = Decimal(settings.UPLINE_SPLIT_RATE)
    MINIMUM_COMMISSION = Decimal('0.01')
    
    @classmethod
    @transaction.atomic
    def distribute_commissions(cls, new_user, membership_fee):
        """
        Distribute referral commissions for a new membership payment.
        
        Args:
            new_user: User instance of the new member
            membership_fee: Decimal amount of membership fee paid
        
        Returns:
            List of commission records created
        """
        commissions_created = []
        membership_fee = Decimal(str(membership_fee))
        
        # Step 1: Direct referral commission (25%)
        if new_user.referred_by:
            direct_commission = membership_fee * cls.DIRECT_COMMISSION_RATE
            
            # Credit direct referrer's wallet
            direct_referrer = new_user.referred_by
            direct_referrer.wallet_balance += direct_commission
            direct_referrer.save(update_fields=['wallet_balance'])
            
            # Create referral record
            referral = Referral.objects.create(
                referrer=direct_referrer,
                referred=new_user,
                level=1,
                commission_earned=direct_commission
            )
            
            # Create transaction record
            Transaction.objects.create(
                user=direct_referrer,
                transaction_type='referral_commission',
                amount=direct_commission,
                status='completed',
                description=f'Direct referral commission from {new_user.full_name}'
            )
            
            commissions_created.append({
                'user': direct_referrer,
                'amount': direct_commission,
                'level': 1
            })
            
            # Step 2: Upline commission distribution (additional 25%)
            remaining_pool = membership_fee * cls.UPLINE_POOL_RATE
            current_referrer = direct_referrer.referred_by
            level = 2
            
            while current_referrer and remaining_pool >= cls.MINIMUM_COMMISSION:
                # Calculate commission for this level (50% of remaining pool)
                commission = remaining_pool * cls.UPLINE_SPLIT_RATE
                
                # Credit referrer's wallet
                current_referrer.wallet_balance += commission
                current_referrer.save(update_fields=['wallet_balance'])
                
                # Create referral record
                Referral.objects.create(
                    referrer=current_referrer,
                    referred=new_user,
                    level=level,
                    commission_earned=commission
                )
                
                # Create transaction record
                Transaction.objects.create(
                    user=current_referrer,
                    transaction_type='referral_commission',
                    amount=commission,
                    status='completed',
                    description=f'Level {level} referral commission from {new_user.full_name}'
                )
                
                commissions_created.append({
                    'user': current_referrer,
                    'amount': commission,
                    'level': level
                })
                
                # Update for next iteration
                remaining_pool -= commission
                current_referrer = current_referrer.referred_by
                level += 1
        
        return commissions_created
    
    @staticmethod
    def get_referral_chain(user):
        """
        Get complete upline chain for a user.
        
        Args:
            user: User instance
        
        Returns:
            List of dict with user info and level
        """
        chain = []
        current = user.referred_by
        level = 1
        
        while current:
            chain.append({
                'level': level,
                'user': current,
                'referral_code': current.referral_code,
                'full_name': current.full_name,
                'email': current.email
            })
            current = current.referred_by
            level += 1
        
        return chain
    
    @staticmethod
    def get_referral_tree(user, max_depth=3):
        """
        Get referral tree (downline) for a user.
        
        Args:
            user: User instance
            max_depth: Maximum depth to fetch (default 3 levels)
        
        Returns:
            Nested dict representing referral tree
        """
        def build_tree(user_obj, current_depth):
            if current_depth > max_depth:
                return []
            
            direct_referrals = user_obj.referrals.filter(
                is_active=True,
                membership_paid=True
            ).select_related('referred_by')
            
            tree = []
            for referral in direct_referrals:
                tree.append({
                    'id': str(referral.id),
                    'full_name': referral.full_name,
                    'email': referral.email,
                    'joined_at': referral.joined_at,
                    'is_active': referral.is_active,
                   'commission_earned': Referral.objects.filter(
                        referrer=user_obj,
                        referred=referral,
                        level=1
                    ).first().commission_earned if current_depth == 1 else None,
                    'direct_referrals': build_tree(referral, current_depth + 1)
                })
            
            return tree
        
        return build_tree(user, 1)
    
    @staticmethod
    def get_commission_stats(user):
        """
        Get commission statistics for a user.
        
        Args:
            user: User instance
        
        Returns:
            Dict with commission stats
        """
        from django.db.models import Sum, Count
        
        # Total commissions earned
        total_commissions = Referral.objects.filter(
            referrer=user
        ).aggregate(
            total=Sum('commission_earned'),
            count=Count('id')
        )
        
        # Commission by level
        by_level = Referral.objects.filter(
            referrer=user
        ).values('level').annotate(
            count=Count('id'),
            total_earned=Sum('commission_earned')
        ).order_by('level')
        
        # Direct commissions (level 1)
        direct = Referral.objects.filter(
            referrer=user,
            level=1
        ).aggregate(
            total=Sum('commission_earned'),
            count=Count('id')
        )
        
        # Upline commissions (level 2+)
        upline = Referral.objects.filter(
            referrer=user,
            level__gt=1
        ).aggregate(
            total=Sum('commission_earned'),
            count=Count('id')
        )
        
        return {
            'total_commissions': total_commissions['total'] or Decimal('0.00'),
            'total_count': total_commissions['count'] or 0,
            'direct_commissions': direct['total'] or Decimal('0.00'),
            'direct_count': direct['count'] or 0,
            'upline_commissions': upline['total'] or Decimal('0.00'),
            'upline_count': upline['count'] or 0,
            'by_level': list(by_level)
        }
