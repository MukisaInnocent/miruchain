# MIRUCHAIN - API Documentation

REST API documentation for the MIRUCHAIN backend server.

**Base URL**: `https://api.miruchain.com/v1`  
**Authentication**: JWT Bearer Token  
**Content-Type**: `application/json`

---

## Table of Contents

1. [Authentication](#authentication)
2. [Users](#users)
3. [Referrals](#referrals)
4. [Business Links](#business-links)
5. [Transactions](#transactions)
6. [Admin](#admin)
7. [Configuration](#configuration)
8. [Error Handling](#error-handling)

---

## Authentication

### Register User

Create a new user account.

**Endpoint**: `POST /auth/register`  
**Auth Required**: No

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe",
  "phone_number": "+1234567890",
  "referral_code": "ABC123XYZ"
}
```

**Response**: `201 Created`
```json
{
  "success": true,
  "message": "Registration successful. Please complete payment to activate your account.",
  "data": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "referral_code": "DEF456UVW",
    "payment_required": true,
    "payment_amount": 100.00,
    "payment_url": "https://checkout.miruchain.com/pay/abc123"
  }
}
```

**Validation Errors**: `400 Bad Request`
```json
{
  "success": false,
  "errors": {
    "email": ["Email already registered"],
    "password": ["Password must be at least 8 characters"],
    "referral_code": ["Invalid referral code"]
  }
}
```

---

### Login

Authenticate user and receive JWT token.

**Endpoint**: `POST /auth/login`  
**Auth Required**: No

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "expires_in": 3600,
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "user@example.com",
      "full_name": "John Doe",
      "is_admin": false,
      "membership_paid": true
    }
  }
}
```

**Error**: `401 Unauthorized`
```json
{
  "success": false,
  "message": "Invalid email or password"
}
```

---

### Refresh Token

Get new access token using refresh token.

**Endpoint**: `POST /auth/refresh`  
**Auth Required**: No

**Request Body**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 3600
  }
}
```

---

### Verify Email

Verify user's email address.

**Endpoint**: `POST /auth/verify-email`  
**Auth Required**: No

**Request Body**:
```json
{
  "token": "verification_token_from_email"
}
```

**Response**: `200 OK`
```json
{
  "success": true,
  "message": "Email verified successfully"
}
```

---

### Password Reset Request

**Endpoint**: `POST /auth/forgot-password`  
**Auth Required**: No

**Request Body**:
```json
{
  "email": "user@example.com"
}
```

**Response**: `200 OK`
```json
{
  "success": true,
  "message": "Password reset link sent to your email"
}
```

---

### Password Reset Confirm

**Endpoint**: `POST /auth/reset-password`  
**Auth Required**: No

**Request Body**:
```json
{
  "token": "reset_token_from_email",
  "new_password": "NewSecurePass123!"
}
```

**Response**: `200 OK`
```json
{
  "success": true,
  "message": "Password reset successful"
}
```

---

## Users

All user endpoints require authentication unless stated otherwise.

### Get Current User Profile

**Endpoint**: `GET /users/me`  
**Auth Required**: Yes

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "phone_number": "+1234567890",
    "is_active": true,
    "is_verified": true,
    "membership_paid": true,
    "membership_expiry": "2025-12-31T23:59:59Z",
    "referral_code": "DEF456UVW",
    "wallet_balance": 1245.50,
    "joined_at": "2024-01-15T10:30:00Z",
    "referred_by": {
      "id": "440e8400-e29b-41d4-a716-446655440001",
      "full_name": "Jane Smith",
      "referral_code": "ABC123XYZ"
    }
  }
}
```

---

### Update User Profile

**Endpoint**: `PATCH /users/me`  
**Auth Required**: Yes

**Request Body**:
```json
{
  "full_name": "John Michael Doe",
  "phone_number": "+1234567891"
}
```

**Response**: `200 OK`
```json
{
  "success": true,
  "message": "Profile updated successfully",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "full_name": "John Michael Doe",
    "phone_number": "+1234567891"
  }
}
```

---

### Get User Dashboard Stats

**Endpoint**: `GET /users/me/dashboard`  
**Auth Required**: Yes

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "total_earnings": 12450.00,
    "wallet_balance": 4200.50,
    "total_referrals": 45,
    "active_referrals": 38,
    "total_links": 312,
    "approved_links": 298,
    "total_clicks": 15678,
    "total_conversions": 234,
    "earnings_breakdown": {
      "direct_referral_commissions": 8500.00,
      "upline_referral_commissions": 2450.00,
      "link_earnings": 1500.00
    },
    "recent_earnings": [
      {
        "date": "2024-01-20",
        "amount": 125.50
      },
      {
        "date": "2024-01-19",
        "amount": 87.25
      }
    ]
  }
}
```

---

## Referrals

### Get Referral Statistics

**Endpoint**: `GET /referrals/stats`  
**Auth Required**: Yes

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "total_referrals": 45,
    "active_referrals": 38,
    "total_commissions": 10950.00,
    "direct_commissions": 8500.00,
    "upline_commissions": 2450.00,
    "by_level": [
      {
        "level": 1,
        "count": 15,
        "total_earned": 8500.00
      },
      {
        "level": 2,
        "count": 20,
        "total_earned": 1800.00
      },
      {
        "level": 3,
        "count": 10,
        "total_earned": 650.00
      }
    ]
  }
}
```

---

### Get Referral Tree

**Endpoint**: `GET /referrals/tree`  
**Auth Required**: Yes

**Query Parameters**:
- `depth` (optional): Maximum depth to fetch (default: 3, max: 10)

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "full_name": "John Doe",
    "direct_referrals": [
      {
        "id": "661e8400-e29b-41d4-a716-446655440002",
        "full_name": "Alice Brown",
        "email": "alice@example.com",
        "joined_at": "2024-02-01T10:00:00Z",
        "is_active": true,
        "commission_earned": 25.00,
        "direct_referrals": [
          {
            "id": "771e8400-e29b-41d4-a716-446655440003",
            "full_name": "Bob Wilson",
            "commission_earned": 12.50,
            "direct_referrals": []
          }
        ]
      }
    ]
  }
}
```

---

### Get Referral Chain (Upline)

**Endpoint**: `GET /referrals/chain`  
**Auth Required**: Yes

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "chain": [
      {
        "level": 1,
        "user": {
          "id": "440e8400-e29b-41d4-a716-446655440001",
          "full_name": "Jane Smith",
          "referral_code": "ABC123XYZ"
        }
      },
      {
        "level": 2,
        "user": {
          "id": "330e8400-e29b-41d4-a716-446655440001",
          "full_name": "Mike Johnson",
          "referral_code": "XYZ789ABC"
        }
      }
    ]
  }
}
```

---

### Get Commission History

**Endpoint**: `GET /referrals/commissions`  
**Auth Required**: Yes

**Query Parameters**:
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 20, max: 100)
- `level` (optional): Filter by referral level

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "commissions": [
      {
        "id": "881e8400-e29b-41d4-a716-446655440004",
        "referred_user": {
          "id": "661e8400-e29b-41d4-a716-446655440002",
          "full_name": "Alice Brown"
        },
        "level": 1,
        "amount": 25.00,
        "created_at": "2024-02-01T10:05:00Z"
      }
    ],
    "pagination": {
      "current_page": 1,
      "per_page": 20,
      "total_pages": 3,
      "total_items": 45
    }
  }
}
```

---

## Business Links

### Get All Business Links

**Endpoint**: `GET /links`  
**Auth Required**: No (but shows share options if authenticated)

**Query Parameters**:
- `page` (optional): Page number
- `per_page` (optional): Items per page
- `category` (optional): Filter by category
- `search` (optional): Search query
- `sort` (optional): `popular`, `newest`, `clicks` (default: `popular`)

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "links": [
      {
        "id": "aa1e8400-e29b-41d4-a716-446655440005",
        "title": "Amazing Tech Product",
        "description": "Revolutionary product that changes everything...",
        "url": "https://example.com/product",
        "category": "Technology",
        "is_admin_link": false,
        "earning_rate": 0.00,
        "total_clicks": 1234,
        "total_conversions": 45,
        "created_at": "2024-01-10T08:00:00Z",
        "posted_by": {
          "id": "bb1e8400-e29b-41d4-a716-446655440006",
          "full_name": "Sarah Connor"
        }
      }
    ],
    "pagination": {
      "current_page": 1,
      "per_page": 20,
      "total_pages": 16,
      "total_items": 312
    }
  }
}
```

---

### Get Single Business Link

**Endpoint**: `GET /links/:link_id`  
**Auth Required**: No

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "id": "aa1e8400-e29b-41d4-a716-446655440005",
    "title": "Amazing Tech Product",
    "description": "Full description...",
    "url": "https://example.com/product",
    "category": "Technology",
    "is_admin_link": false,
    "earning_rate": 0.00,
    "total_clicks": 1234,
    "total_conversions": 45,
    "performance": {
      "conversion_rate": 3.65,
      "avg_earnings_per_share": 4.82
    }
  }
}
```

---

### Create Business Link

**Endpoint**: `POST /links`  
**Auth Required**: Yes

**Request Body**:
```json
{
  "title": "My Awesome Business",
  "description": "We provide excellent services...",
  "url": "https://mybusiness.com",
  "category": "Services"
}
```

**Response**: `201 Created`
```json
{
  "success": true,
  "message": "Business link created. Please complete payment to publish.",
  "data": {
    "link_id": "cc1e8400-e29b-41d4-a716-446655440007",
    "status": "pending_payment",
    "advertising_fee": 10.00,
    "payment_url": "https://checkout.miruchain.com/pay/xyz789"
  }
}
```

---

### Update Business Link

**Endpoint**: `PATCH /links/:link_id`  
**Auth Required**: Yes (must be owner or admin)

**Request Body**:
```json
{
  "title": "Updated Business Name",
  "description": "New description..."
}
```

**Response**: `200 OK`
```json
{
  "success": true,
  "message": "Link updated successfully",
  "data": {
    "id": "cc1e8400-e29b-41d4-a716-446655440007",
    "title": "Updated Business Name"
  }
}
```

---

### Generate Share Link

**Endpoint**: `POST /links/:link_id/share`  
**Auth Required**: Yes

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "share_id": "dd1e8400-e29b-41d4-a716-446655440008",
    "share_code": "SH-ABC123",
    "share_url": "https://miruchain.com/go/SH-ABC123",
    "potential_earning": 0.50
  }
}
```

---

### Track Link Click

**Endpoint**: `POST /links/track/:share_code`  
**Auth Required**: No

**Request Body**:
```json
{
  "referrer": "https://facebook.com",
  "user_agent": "Mozilla/5.0..."
}
```

**Response**: `200 OK`
```json
{
  "success": true,
  "redirect_url": "https://example.com/product"
}
```

---

### Get My Links

**Endpoint**: `GET /links/my-links`  
**Auth Required**: Yes

**Query Parameters**:
- `status` (optional): Filter by status (pending, approved, rejected, active)

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "links": [
      {
        "id": "cc1e8400-e29b-41d4-a716-446655440007",
        "title": "My Business",
        "status": "approved",
        "total_clicks": 245,
        "total_earnings": 122.50,
        "my_shares": {
          "share_url": "https://miruchain.com/go/SH-XYZ789",
          "clicks": 50,
          "earnings": 25.00
        }
      }
    ]
  }
}
```

---

## Transactions

### Get Transaction History

**Endpoint**: `GET /transactions`  
**Auth Required**: Yes

**Query Parameters**:
- `page`, `per_page`: Pagination
- `type` (optional): Filter by transaction type
- `status` (optional): Filter by status
- `start_date`, `end_date` (optional): Date range

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "transactions": [
      {
        "id": "ee1e8400-e29b-41d4-a716-446655440009",
        "type": "referral_commission",
        "amount": 25.00,
        "status": "completed",
        "description": "Direct referral commission from Alice Brown",
        "created_at": "2024-02-01T10:05:00Z",
        "processed_at": "2024-02-01T10:05:01Z"
      }
    ],
    "pagination": {
      "current_page": 1,
      "per_page": 20,
      "total_pages": 5,
      "total_items": 89
    }
  }
}
```

---

### Initiate Membership Payment

**Endpoint**: `POST /transactions/membership-payment`  
**Auth Required**: Yes (for existing users upgrading)

**Request Body**:
```json
{
  "payment_method": "stripe",
  "return_url": "https://miruchain.com/dashboard"
}
```

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "transaction_id": "ff1e8400-e29b-41d4-a716-446655440010",
    "amount": 100.00,
    "payment_url": "https://checkout.stripe.com/...",
    "payment_reference": "pi_abc123xyz"
  }
}
```

---

### Request Withdrawal

**Endpoint**: `POST /transactions/withdrawal`  
**Auth Required**: Yes

**Request Body**:
```json
{
  "amount": 500.00,
  "payment_method": "bank_transfer",
  "account_details": {
    "account_number": "1234567890",
    "bank_name": "Example Bank",
    "account_holder": "John Doe"
  }
}
```

**Response**: `200 OK`
```json
{
  "success": true,
  "message": "Withdrawal request submitted for processing",
  "data": {
    "transaction_id": "gg1e8400-e29b-41d4-a716-446655440011",
    "amount": 500.00,
    "fee": 0.00,
    "net_amount": 500.00,
    "status": "pending",
    "estimated_processing_time": "2-5 business days"
  }
}
```

---

### Payment Webhook (Stripe Example)

**Endpoint**: `POST /webhooks/payment`  
**Auth Required**: No (verified by signature)

**Headers**:
```
Stripe-Signature: t=timestamp,v1=signature
```

**Request Body** (Stripe event):
```json
{
  "type": "payment_intent.succeeded",
  "data": {
    "object": {
      "id": "pi_abc123xyz",
      "amount": 10000,
      "metadata": {
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "transaction_type": "membership"
      }
    }
  }
}
```

**Response**: `200 OK`
```json
{
  "received": true
}
```

---

## Admin

All admin endpoints require admin authentication.

### Get Platform Analytics

**Endpoint**: `GET /admin/analytics`  
**Auth Required**: Yes (Admin only)

**Query Parameters**:
- `period` (optional): `today`, `week`, `month`, `year`, `all` (default: `month`)

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "overview": {
      "total_users": 12450,
      "active_members": 8900,
      "platform_revenue": 145200.00,
      "total_commissions_paid": 72600.00,
      "pending_withdrawals": 845.00
    },
    "user_growth": [
      { "date": "2024-01-01", "new_users": 45 },
      { "date": "2024-01-02", "new_users": 38 }
    ],
    "revenue_breakdown": {
      "membership_fees": 89000.00,
      "advertising_fees": 56200.00
    },
    "top_earners": [
      {
        "user_id": "...",
        "full_name": "Top User",
        "total_earnings": 8500.00
      }
    ]
  }
}
```

---

### Get All Users (Admin)

**Endpoint**: `GET /admin/users`  
**Auth Required**: Yes (Admin only)

**Query Parameters**:
- `page`, `per_page`: Pagination
- `search` (optional): Search by email/name
- `status` (optional): `active`, `inactive`, `unverified`
- `membership` (optional): `paid`, `unpaid`

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "users": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "user@example.com",
        "full_name": "John Doe",
        "is_active": true,
        "membership_paid": true,
        "wallet_balance": 1245.50,
        "total_referrals": 15,
        "joined_at": "2024-01-15T10:30:00Z"
      }
    ],
    "pagination": {...}
  }
}
```

---

### Update User Status (Admin)

**Endpoint**: `PATCH /admin/users/:user_id`  
**Auth Required**: Yes (Admin only)

**Request Body**:
```json
{
  "is_active": false,
  "is_admin": false
}
```

**Response**: `200 OK`
```json
{
  "success": true,
  "message": "User status updated",
  "data": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "is_active": false
  }
}
```

---

### Get Pending Links (Admin)

**Endpoint**: `GET /admin/links/pending`  
**Auth Required**: Yes (Admin only)

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "links": [
      {
        "id": "hh1e8400-e29b-41d4-a716-446655440012",
        "title": "New Business Link",
        "url": "https://example.com",
        "category": "Tech",
        "posted_by": {
          "id": "...",
          "full_name": "User Name"
        },
        "created_at": "2024-02-15T14:00:00Z"
      }
    ]
  }
}
```

---

### Approve/Reject Link (Admin)

**Endpoint**: `POST /admin/links/:link_id/moderate`  
**Auth Required**: Yes (Admin only)

**Request Body**:
```json
{
  "action": "approve",
  "reason": "Meets quality standards"
}
```

**Response**: `200 OK`
```json
{
  "success": true,
  "message": "Link approved successfully"
}
```

---

### Create Admin Promotional Link

**Endpoint**: `POST /admin/links/promotional`  
**Auth Required**: Yes (Admin only)

**Request Body**:
```json
{
  "title": "Official Promo: Earn $5 Per Share",
  "description": "Share and earn...",
  "url": "https://partner.com/offer",
  "category": "Finance",
  "earning_rate": 5.00
}
```

**Response**: `201 Created`
```json
{
  "success": true,
  "data": {
    "link_id": "ii1e8400-e29b-41d4-a716-446655440013",
    "is_admin_link": true,
    "earning_rate": 5.00
  }
}
```

---

## Configuration

### Get Public Configuration

**Endpoint**: `GET /config/public`  
**Auth Required**: No

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "membership_fee": 100.00,
    "advertising_fee": 10.00,
    "minimum_withdrawal": 10.00,
    "categories": ["Technology", "Finance", "Services", "Creative", "Health"]
  }
}
```

---

### Update Configuration (Admin)

**Endpoint**: `PATCH /admin/config`  
**Auth Required**: Yes (Admin only)

**Request Body**:
```json
{
  "membership_fee": 150.00,
  "advertising_fee": 15.00
}
```

**Response**: `200 OK`
```json
{
  "success": true,
  "message": "Configuration updated successfully"
}
```

---

## Error Handling

All API errors follow this format:

```json
{
  "success": false,
  "message": "Error message",
  "errors": {
    "field_name": ["Validation error message"]
  },
  "code": "ERROR_CODE"
}
```

### Common HTTP Status Codes

- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `204 No Content`: Successful request with no response body
- `400 Bad Request`: Validation error or malformed request
- `401 Unauthorized`: Authentication required or failed
- `403 Forbidden`: Authenticated but not authorized
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource conflict (e.g., duplicate email)
- `422 Unprocessable Entity`: Semantic errors
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

### Error Codes

- `AUTH_REQUIRED`: Authentication required
- `AUTH_INVALID`: Invalid credentials
- `AUTH_EXPIRED`: Token expired
- `PERMISSION_DENIED`: Insufficient permissions
- `VALIDATION_ERROR`: Input validation failed
- `RESOURCE_NOT_FOUND`: Requested resource not found
- `DUPLICATE_RESOURCE`: Resource already exists
- `PAYMENT_FAILED`: Payment processing failed
- `INSUFFICIENT_BALANCE`: Wallet balance too low
- `RATE_LIMIT_EXCEEDED`: Too many requests

---

## Rate Limiting

**Limits**:
- Authenticated: 100 requests per minute
- Unauthenticated: 20 requests per minute
- Admin: 200 requests per minute

**Headers**:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1643723400
```

**Error Response** (`429 Too Many Requests`):
```json
{
  "success": false,
  "message": "Rate limit exceeded. Please try again later.",
  "retry_after": 60
}
```

---

## Pagination

All paginated endpoints return:

```json
{
  "pagination": {
    "current_page": 1,
    "per_page": 20,
    "total_pages": 10,
    "total_items": 200,
    "has_next": true,
    "has_prev": false
  }
}
```

**Query Parameters**:
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20, max: 100)

---

## Webhook Events

Webhooks are sent for:
- `user.registered`: New user registration
- `user.verified`: Email verified
- `membership.paid`: Membership payment completed
- `link.created`: Business link created
- `link.approved`: Link approved
- `commission.earned`: Referral commission earned
- `withdrawal.requested`: Withdrawal requested
- `withdrawal.completed`: Withdrawal processed

**Webhook Payload**:
```json
{
  "event": "commission.earned",
  "timestamp": "2024-02-01T10:05:00Z",
  "data": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "amount": 25.00,
    "level": 1
  }
}
```

---

## SDK Examples

### JavaScript/Node.js

```javascript
const MIRUCHAIN_API = 'https://api.miruchain.com/v1';

// Login
const login = async (email, password) => {
  const response = await fetch(`${MIRUCHAIN_API}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  const data = await response.json();
  localStorage.setItem('access_token', data.data.access_token);
  return data;
};

// Get dashboard
const getDashboard = async () => {
  const token = localStorage.getItem('access_token');
  const response = await fetch(`${MIRUCHAIN_API}/users/me/dashboard`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return await response.json();
};
```

### Python

```python
import requests

BASE_URL = 'https://api.miruchain.com/v1'

class MiruchainAPI:
    def __init__(self, access_token=None):
        self.access_token = access_token
    
    def login(self, email, password):
        response = requests.post(f'{BASE_URL}/auth/login', json={
            'email': email,
            'password': password
        })
        data = response.json()
        self.access_token = data['data']['access_token']
        return data
    
    def get_dashboard(self):
        response = requests.get(
            f'{BASE_URL}/users/me/dashboard',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        return response.json()
```

---

## Testing

**Test Base URL**: `https://api-test.miruchain.com/v1`

**Test Credentials**:
- Email: `test@miruchain.com`
- Password: `TestPass123!`

**Test Payment Cards** (Stripe):
- Success: `4242 4242 4242 4242`
- Decline: `4000 0000 0000 0002`
