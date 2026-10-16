/**
 * MIRUCHAIN API Integration Layer
 * Handles all API requests with JWT authentication
 */

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

class API {
  constructor() {
    this.baseURL = API_BASE_URL;
    this.accessToken = localStorage.getItem('access_token');
    this.refreshToken = localStorage.getItem('refresh_token');
  }

  /**
   * Get authorization headers
   */
  getHeaders(useAuth = true) {
    const headers = {
      'Content-Type': 'application/json',
    };

    if (useAuth && this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`;
    }

    return headers;
  }

  /**
   * Make API request with enhanced error handling
   */
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      ...options,
      headers: this.getHeaders(options.useAuth !== false),
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        // Token expired - try to refresh
        if (response.status === 401 && this.refreshToken) {
          const refreshed = await this.refreshAccessToken();
          if (refreshed) {
            // Retry the original request
            config.headers = this.getHeaders();
            const retryResponse = await fetch(url, config);
            const retryData = await retryResponse.json();

            if (!retryResponse.ok) {
              throw new Error(this.getUserFriendlyError(retryResponse.status, retryData));
            }
            return retryData;
          }
        }

        throw new Error(this.getUserFriendlyError(response.status, data));
      }

      return data;
    } catch (error) {
      console.error('API Error:', error);

      // Network errors
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        throw new Error('Unable to connect to the server. Please check your internet connection and try again.');
      }

      // JSON parsing errors
      if (error instanceof SyntaxError) {
        throw new Error('Received invalid response from server. Please try again.');
      }

      throw error;
    }
  }

  /**
   * Convert technical errors to user-friendly messages
   */
  getUserFriendlyError(status, data) {
    // Try to extract meaningful error message from response
    let message = data.message || data.error || data.detail;

    // Handle validation errors
    if (data.errors || data.non_field_errors) {
      const errors = data.errors || data.non_field_errors;
      if (Array.isArray(errors)) {
        message = errors.join('. ');
      } else if (typeof errors === 'object') {
        message = Object.entries(errors)
          .map(([field, msgs]) => `${field}: ${Array.isArray(msgs) ? msgs.join(', ') : msgs}`)
          .join('. ');
      }
    }

    // Provide user-friendly messages based on status code
    switch (status) {
      case 400:
        return message || 'Please check your input and try again.';
      case 401:
        return 'Your session has expired. Please log in again.';
      case 403:
        return 'You don\'t have permission to perform this action.';
      case 404:
        return 'The requested resource was not found.';
      case 409:
        return message || 'This action conflicts with existing data.';
      case 422:
        return message || 'Please check your input and try again.';
      case 429:
        return 'Too many requests. Please wait a moment and try again.';
      case 500:
        return 'Server error. Our team has been notified. Please try again later.';
      case 502:
      case 503:
      case 504:
        return 'Service temporarily unavailable. Please try again in a few moments.';
      default:
        return message || 'Something went wrong. Please try again.';
    }
  }

  /**
   * Refresh access token
   */
  async refreshAccessToken() {
    try {
      const response = await fetch(`${this.baseURL}/auth/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: this.refreshToken }),
      });

      const data = await response.json();

      if (response.ok && data.access) {
        this.accessToken = data.access;
        localStorage.setItem('access_token', data.access);
        return true;
      }

      // Refresh failed - logout
      this.logout();
      return false;
    } catch (error) {
      this.logout();
      return false;
    }
  }

  /**
   * Logout user
   */
  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    this.accessToken = null;
    this.refreshToken = null;
    window.location.href = '/login.html';
  }

  // ========== AUTHENTICATION ==========

  async register(data) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
      useAuth: false,
    });
  }

  async login(email, password) {
    const response = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
      useAuth: false,
    });

    if (response.success) {
      this.accessToken = response.data.access_token;
      this.refreshToken = response.data.refresh_token;
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('refresh_token', response.data.refresh_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }

    return response;
  }

  async verifyReferralCode(code) {
    return this.request('/auth/verify-referral-code', {
      method: 'POST',
      body: JSON.stringify({ referral_code: code }),
      useAuth: false,
    });
  }

  async forgotPassword(email) {
    return this.request('/auth/forgot-password', {
      method: 'POST',
      body: JSON.stringify({ email }),
      useAuth: false,
    });
  }

  // ========== USER ==========

  async getProfile() {
    return this.request('/users/me');
  }

  async updateProfile(data) {
    return this.request('/users/me', {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }

  async getDashboard() {
    return this.request('/users/me/dashboard');
  }

  async changePassword(oldPassword, newPassword) {
    return this.request('/users/me/change-password', {
      method: 'POST',
      body: JSON.stringify({
        old_password: oldPassword,
        new_password: newPassword,
      }),
    });
  }

  async getReferralLink() {
    return this.request('/users/me/referral-link');
  }

  // ========== REFERRALS ==========

  async getReferrals() {
    return this.request('/referrals');
  }

  async getReferralTree(depth = 3) {
    return this.request(`/referrals/tree?depth=${depth}`);
  }

  async getReferralChain() {
    return this.request('/referrals/chain');
  }

  async getReferralStats() {
    return this.request('/referrals/stats');
  }

  async getDirectReferrals() {
    return this.request('/referrals/direct');
  }

  // ========== TRANSACTIONS ==========

  async getTransactions(type = null, status = null) {
    let url = '/transactions';
    const params = [];
    if (type) params.push(`type=${type}`);
    if (status) params.push(`status=${status}`);
    if (params.length) url += `?${params.join('&')}`;

    return this.request(url);
  }

  async getTransactionSummary() {
    return this.request('/transactions/summary');
  }

  async createPaymentIntent(amount, paymentType, description = '') {
    return this.request('/transactions/create-payment-intent', {
      method: 'POST',
      body: JSON.stringify({ amount, payment_type: paymentType, description }),
    });
  }

  async confirmPayment(transactionId, paymentId) {
    return this.request('/transactions/confirm-payment', {
      method: 'POST',
      body: JSON.stringify({ transaction_id: transactionId, payment_id: paymentId }),
    });
  }

  async requestWithdrawal(amount, paymentMethod, paymentDetails) {
    return this.request('/transactions/withdrawal', {
      method: 'POST',
      body: JSON.stringify({ amount, payment_method: paymentMethod, payment_details: paymentDetails }),
    });
  }

  async getWithdrawals() {
    return this.request('/transactions/withdrawals');
  }

  // ========== LINKS ==========

  async getLinks(category = null, search = null) {
    let url = '/links';
    const params = [];
    if (category) params.push(`category=${category}`);
    if (search) params.push(`search=${search}`);
    if (params.length) url += `?${params.join('&')}`;

    return this.request(url, { useAuth: false });
  }

  async getMyLinks() {
    return this.request('/links/my-links');
  }

  async createLink(data) {
    return this.request('/links/create', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getLink(id) {
    return this.request(`/links/${id}`);
  }

  async updateLink(id, data) {
    return this.request(`/links/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteLink(id) {
    return this.request(`/links/${id}`, {
      method: 'DELETE',
    });
  }

  async shareLink(linkId) {
    return this.request(`/links/${linkId}/share`, {
      method: 'POST',
    });
  }

  async getMyShares() {
    return this.request('/links/my-shares');
  }

  async trackClick(shareCode) {
    return this.request(`/links/track/${shareCode}`, {
      method: 'POST',
      useAuth: false,
    });
  }

  async getLinkStats() {
    return this.request('/links/stats');
  }

  // ========== ADMIN ==========

  async getAdminDashboard() {
    return this.request('/admin/dashboard');
  }

  async getUsers(status = null, search = null) {
    let url = '/admin/users';
    const params = [];
    if (status) params.push(`status=${status}`);
    if (search) params.push(`search=${search}`);
    if (params.length) url += `?${params.join('&')}`;

    return this.request(url);
  }

  async getPendingLinks() {
    return this.request('/admin/links/pending');
  }

  async approveLink(linkId) {
    return this.request(`/admin/links/${linkId}/approve`, {
      method: 'POST',
    });
  }

  async rejectLink(linkId, reason) {
    return this.request(`/admin/links/${linkId}/reject`, {
      method: 'POST',
      body: JSON.stringify({ reason }),
    });
  }

  async getPendingWithdrawals() {
    return this.request('/admin/withdrawals/pending');
  }

  async approveWithdrawal(withdrawalId) {
    return this.request(`/admin/withdrawals/${withdrawalId}/approve`, {
      method: 'POST',
    });
  }

  async rejectWithdrawal(withdrawalId, reason) {
    return this.request(`/admin/withdrawals/${withdrawalId}/reject`, {
      method: 'POST',
      body: JSON.stringify({ reason }),
    });
  }
}

// Create global API instance
const api = new API();

// Helper functions
function isAuthenticated() {
  return !!localStorage.getItem('access_token');
}

function getCurrentUser() {
  const userStr = localStorage.getItem('user');
  return userStr ? JSON.parse(userStr) : null;
}

function requireAuth() {
  if (!isAuthenticated()) {
    window.location.href = '/login.html';
  }
}
