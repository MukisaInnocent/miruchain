# MIRUCHAIN - Referral Commission Logic Documentation

## Overview

MIRUCHAIN implements a sophisticated multi-level referral commission system where members earn money by referring new members. This document details the exact calculation logic, examples, and edge cases.

## Commission Structure

### Base Rules

1. **Direct Referral Commission**: 25% of the membership fee
2. **Upline Commission Pool**: Additional 25% of the membership fee
3. **Upline Distribution**: The pool is distributed recursively up the referral chain
   - Each level receives 50% of the remaining pool
   - Distribution continues until the pool is exhausted or no more referrers exist

### Mathematical Formula

For a membership fee `F`:

- **Direct Referrer (Level 1)**: `0.25 × F`
- **Level 2 Referrer**: `0.25 × F × 0.5 = 0.125 × F`
- **Level 3 Referrer**: `0.25 × F × 0.5² = 0.0625 × F`
- **Level n Referrer**: `0.25 × F × 0.5^(n-1)`

The series converges to a maximum total commission of:
- Direct: 25%
- Upline total: 25% × (0.5 + 0.25 + 0.125 + ... ) = 25% × 1 = 25%
- **Grand total: 50% of membership fee**

## Implementation Algorithm

### Pseudocode

```python
def calculate_referral_commissions(new_user, membership_fee):
    """
    Calculate and distribute referral commissions when a new user pays membership.
    
    Args:
        new_user: The newly registered user who paid
        membership_fee: Amount paid for membership
    
    Returns:
        List of commission records created
    """
    commissions = []
    
    # Direct referral commission (25%)
    direct_commission = membership_fee * 0.25
    direct_referrer = new_user.referred_by
    
    if direct_referrer:
        commissions.append({
            'user': direct_referrer,
            'amount': direct_commission,
            'level': 1,
            'type': 'direct_referral'
        })
    
    # Upline commission pool (25%)
    remaining_pool = membership_fee * 0.25
    current_referrer = direct_referrer.referred_by if direct_referrer else None
    level = 2
    
    # Distribute upline commissions
    while current_referrer and remaining_pool > 0.01:  # Stop if pool < 1 cent
        commission = remaining_pool * 0.5
        
        commissions.append({
            'user': current_referrer,
            'amount': commission,
            'level': level,
            'type': 'upline_referral'
        })
        
        remaining_pool -= commission
        current_referrer = current_referrer.referred_by
        level += 1
    
    return commissions
```

### Python/Django Implementation

```python
# backend/referrals/services.py

from decimal import Decimal
from django.db import transaction
from users.models import User
from transactions.models import Transaction
from .models import Referral

class ReferralService:
    
    DIRECT_COMMISSION_RATE = Decimal('0.25')  # 25%
    UPLINE_POOL_RATE = Decimal('0.25')         # 25%
    UPLINE_SPLIT_RATE = Decimal('0.50')        # 50%
    MINIMUM_COMMISSION = Decimal('0.01')       # 1 cent minimum
    
    @classmethod
    @transaction.atomic
    def distribute_commissions(cls, new_user, membership_fee):
        """
        Distribute referral commissions for a new membership payment.
        """
        commissions_created = []
        membership_fee = Decimal(str(membership_fee))
        
        # Step 1: Direct referral commission
        if new_user.referred_by:
            direct_commission = membership_fee * cls.DIRECT_COMMISSION_RATE
            
            # Credit direct referrer's wallet
            direct_referrer = new_user.referred_by
            direct_referrer.wallet_balance += direct_commission
            direct_referrer.save()
            
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
            
            # Step 2: Upline commission distribution
            remaining_pool = membership_fee * cls.UPLINE_POOL_RATE
            current_referrer = direct_referrer.referred_by
            level = 2
            
            while current_referrer and remaining_pool >= cls.MINIMUM_COMMISSION:
                # Calculate commission for this level
                commission = remaining_pool * cls.UPLINE_SPLIT_RATE
                
                # Credit referrer's wallet
                current_referrer.wallet_balance += commission
                current_referrer.save()
                
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
```

## Examples

### Example 1: Membership Fee = $100

**Scenario**: Alice → Bob → Charlie → David → Eve

Eve pays $100 membership fee.

**Commission Distribution**:

| Referrer | Level | Calculation | Commission | Running Total |
|----------|-------|-------------|-----------|---------------|
| David (direct) | 1 | $100 × 0.25 | **$25.00** | $25.00 |
| Charlie | 2 | $25 × 0.5 | **$12.50** | $37.50 |
| Bob | 3 | $12.50 × 0.5 | **$6.25** | $43.75 |
| Alice | 4 | $6.25 × 0.5 | **$3.13** | $46.88 |

**Remaining pool after Alice**: $3.13 × 0.5 = $1.57 (would go to Alice's referrer if exists)

**Platform keeps**: $100 - $46.88 = $53.12 (if chain ends at Alice)

### Example 2: Membership Fee = $50

**Scenario**: John → Mary → Peter

Peter pays $50 membership fee.

**Commission Distribution**:

| Referrer | Level | Calculation | Commission |
|----------|-------|-------------|-----------|
| Mary (direct) | 1 | $50 × 0.25 | **$12.50** |
| John | 2 | $12.50 × 0.5 | **$6.25** |

**Total distributed**: $18.75  
**Platform keeps**: $50 - $18.75 = $31.25

### Example 3: Membership Fee = $200, Deep Chain (10 levels)

**Commission Distribution**:

| Level | Commission | Cumulative |
|-------|-----------|-----------|
| 1 | $50.00 | $50.00 |
| 2 | $25.00 | $75.00 |
| 3 | $12.50 | $87.50 |
| 4 | $6.25 | $93.75 |
| 5 | $3.13 | $96.88 |
| 6 | $1.56 | $98.44 |
| 7 | $0.78 | $99.22 |
| 8 | $0.39 | $99.61 |
| 9 | $0.20 | $99.81 |
| 10 | $0.10 | $99.91 |

**Total distributed**: $99.91 (~50% of $200)  
**Platform keeps**: $100.09

## Edge Cases

### Case 1: User Has No Referrer

```python
# New user registers without referral code
user = User(email='test@example.com', referred_by=None)

# Result: No commissions distributed
# Platform keeps entire membership fee
```

### Case 2: Only One Level of Referral

```python
# A refers B, B pays membership
# A has no referrer

# Result:
# - A gets: 25% direct commission
# - Upline pool: No one to distribute to
# - Platform keeps: 75% of membership fee
```

### Case 3: Minimum Commission Threshold

```python
# When remaining pool < $0.01, stop distribution
# Prevents micro-transactions and database bloat

if remaining_pool < Decimal('0.01'):
    break  # Stop distributing
```

### Case 4: Circular Referral Prevention

```python
# Database constraint prevents circular referrals
# User cannot refer themselves or someone in their upline

def validate_referral(user, referral_code):
    referrer = User.objects.get(referral_code=referral_code)
    
    # Check if referrer is in user's downline
    current = referrer
    while current:
        if current == user:
            raise ValidationError("Circular referral detected")
        current = current.referred_by
    
    return referrer
```

## Database Tracking

### Referrals Table

Each commission generates a record:

```sql
INSERT INTO referrals (id, referrer_id, referred_id, level, commission_earned, created_at)
VALUES (
    uuid_generate_v4(),
    'referrer-uuid',
    'new-user-uuid',
    2,  -- level in chain
    12.50,
    NOW()
);
```

### Transactions Table

Each commission creates a transaction:

```sql
INSERT INTO transactions (id, user_id, transaction_type, amount, status, description, created_at)
VALUES (
    uuid_generate_v4(),
    'referrer-uuid',
    'referral_commission',
    12.50,
    'completed',
    'Level 2 referral commission from New User',
    NOW()
);
```

## Audit & Reporting

### Getting Total Commissions for a User

```python
def get_user_commission_stats(user):
    """Get commission earnings breakdown for a user."""
    
    direct_commissions = Referral.objects.filter(
        referrer=user,
        level=1
    ).aggregate(total=Sum('commission_earned'))
    
    upline_commissions = Referral.objects.filter(
        referrer=user,
        level__gt=1
    ).aggregate(total=Sum('commission_earned'))
    
    return {
        'direct': direct_commissions['total'] or 0,
        'upline': upline_commissions['total'] or 0,
        'total': (direct_commissions['total'] or 0) + (upline_commissions['total'] or 0)
    }
```

### Getting Referral Chain

```python
def get_referral_chain(user):
    """Get complete upline chain for a user."""
    
    chain = []
    current = user.referred_by
    level = 1
    
    while current:
        chain.append({
            'user': current,
            'level': level,
            'referral_code': current.referral_code
        })
        current = current.referred_by
        level += 1
    
    return chain
```

## Testing Checklist

- [ ] Test commission calculation with $100 membership fee
- [ ] Test commission calculation with $50 membership fee  
- [ ] Test 2-level referral chain
- [ ] Test 5-level referral chain
- [ ] Test 10+ level referral chain
- [ ] Test user with no referrer
- [ ] Test minimum commission threshold stopping condition
- [ ] Verify total commissions = ~50% of membership fee
- [ ] Test wallet balance updates correctly
- [ ] Test transaction records created correctly
- [ ] Test referral records created correctly
- [ ] Test with decimal membership fees ($99.99)
- [ ] Verify no circular referrals possible
- [ ] Test concurrent membership payments (race conditions)

## Performance Considerations

1. **Database Transactions**: Wrap commission distribution in atomic transaction
2. **Indexing**: Index `referred_by` field for efficient chain traversal
3. **Caching**: Cache referral chains for active users
4. **Async Processing**: Consider processing commissions asynchronously for high-volume scenarios

## Security Considerations

1. **Validation**: Validate membership payment before distributing commissions
2. **Idempotency**: Ensure commissions only distributed once per payment
3. **Audit Trail**: Keep immutable transaction records
4. **Fraud Prevention**: Monitor for suspicious referral patterns
5. **Rate Limiting**: Limit new member registrations per IP/device
