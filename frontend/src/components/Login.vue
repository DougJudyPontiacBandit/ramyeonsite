<template>
  <div class="auth-container">
    <div class="auth-card">
      <!-- Logo with animation -->
      <div class="logo-container">
        <img :src="logoSrc" alt="Ramyeon Corner Logo" class="auth-logo" />
      </div>
      
      <h1 class="auth-title">Welcome Back! 🍜</h1>
      <p class="auth-subtitle">Don't have an account? <a href="#" @click.prevent="$emit('switchToSignUp')" class="create-link">Create now</a></p>
      
      <!-- Enhanced Messages -->
      <transition name="slide-fade">
        <div v-if="errorMessage" class="error-message">
          <span class="message-icon">⚠️</span>
          {{ errorMessage }}
        </div>
      </transition>
      
      <transition name="slide-fade">
        <div v-if="successMessage" class="success-message">
          <span class="message-icon">✅</span>
          {{ successMessage }}
        </div>
      </transition>
      
      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label for="email" class="form-label">
            <span class="label-icon">📧</span>
            E-mail
          </label>
          <div class="input-wrapper">
            <input
              type="email"
              id="email"
              v-model="formData.email"
              :class="['form-input', { error: errors.email, success: !errors.email && formData.email }]"
              placeholder="example@gmail.com"
              required
              @focus="activeField = 'email'"
              @blur="activeField = ''"
            />
            <span v-if="!errors.email && formData.email" class="input-check">✓</span>
          </div>
          <transition name="fade">
            <span v-if="errors.email" class="field-error">❌ {{ errors.email }}</span>
          </transition>
        </div>
        
        <div class="form-group">
          <label for="password" class="form-label">
            <span class="label-icon">🔒</span>
            Password
          </label>
          <div class="input-wrapper">
            <input
              :type="showPassword ? 'text' : 'password'"
              id="password"
              v-model="formData.password"
              :class="['form-input', { error: errors.password, success: !errors.password && formData.password }]"
              placeholder="Enter your password"
              required
              @focus="activeField = 'password'"
              @blur="activeField = ''"
            />
            <button
              type="button"
              class="password-toggle"
              @click="togglePassword"
              :aria-label="showPassword ? 'Hide password' : 'Show password'"
            >
              <span class="eye-icon">{{ showPassword ? '👁️' : '👁️‍🗨️' }}</span>
            </button>
          </div>
          <transition name="fade">
            <span v-if="errors.password" class="field-error">❌ {{ errors.password }}</span>
          </transition>
        </div>
        
        <div class="form-row">
          <div class="checkbox-group">
            <input type="checkbox" id="remember" v-model="formData.rememberMe" />
            <label for="remember">Remember me</label>
          </div>
          
          <div class="forgot-password">
            <a href="#" @click.prevent="handleForgotPassword">Forgot Password?</a>
          </div>
        </div>
        
        <button type="submit" class="auth-button" :disabled="isLoading">
          <span v-if="isLoading" class="loading-spinner"></span>
          <span v-else class="button-icon">🚀</span>
          {{ isLoading ? 'Signing In...' : 'Sign in' }}
        </button>
      </form>
      
      <div class="auth-divider">OR</div>
      
      <div class="social-login">
        <button class="social-btn google-btn" @click="socialLogin('google')" :disabled="isLoading">
          <span class="social-icon">🔴</span>
          <span>Continue with Google</span>
        </button>
        <button class="social-btn facebook-btn" @click="socialLogin('facebook')" :disabled="isLoading">
          <span class="social-icon">📘</span>
          <span>Continue with Facebook</span>
        </button>
      </div>
      
      <!-- Test Account Info -->
      <div class="test-account-info">
        <div class="test-header">🧪 <strong>Test Account</strong></div>
        <div class="test-credentials">
          <div class="credential-item">
            <span class="credential-label">Email:</span>
            <code>test@ramyeoncorner.com</code>
          </div>
          <div class="credential-item">
            <span class="credential-label">Password:</span>
            <code>Test123!</code>
          </div>
        </div>
      </div>

      <!-- Back to Home Button -->
      <button class="back-home-btn" @click="$emit('backToHome')">
        <span class="back-icon">←</span>
        Back to Home
      </button>
    </div>
    
    <!-- Right side promotional content -->
    <div class="promo-content">
      <div class="promo-badge">🔥 HOT DEAL</div>
      <div class="promo-image">
        <img src="../assets/food/ramyeon-hero.jpg" alt="Delicious Ramyeon" class="ramyeon-image" />
        <div class="image-overlay"></div>
      </div>
      <div class="promo-text">
        <div class="promo-timer">⏰ 24 HOURS ONLY</div>
        <h1 class="promo-title">FLASH SALE</h1>
        <div class="promo-code">
          <span class="code-label">USE CODE:</span>
          <span class="code-value">CORNER</span>
        </div>
        <h3 class="promo-discount">30% OFF</h3>
        <button class="order-btn">
          <span>Order Now</span>
          <span class="btn-arrow">→</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { authAPI } from '../services/api';

export default {
  name: 'Login',
  emits: ['switchToSignUp', 'loginSuccess', 'backToHome'],
  data() {
    return {
      formData: {
        email: '',
        password: '',
        rememberMe: false
      },
      errors: {},
      errorMessage: '',
      successMessage: '',
      isLoading: false,
      showPassword: false,
      activeField: '',
      logoSrc: require('../assets/Nav Bar/Logo.png')
    }
  },
  methods: {
    validateForm() {
      this.errors = {};
      
      // Email validation
      if (!this.formData.email) {
        this.errors.email = 'Email is required';
      } else if (!this.isValidEmail(this.formData.email)) {
        this.errors.email = 'Please enter a valid email address';
      }
      
      // Password validation
      if (!this.formData.password) {
        this.errors.password = 'Password is required';
      } else if (this.formData.password.length < 6) {
        this.errors.password = 'Password must be at least 6 characters';
      }
      
      return Object.keys(this.errors).length === 0;
    },
    
    isValidEmail(email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(email);
    },
    
    async handleLogin() {
      this.errorMessage = '';
      this.successMessage = '';
      
      if (!this.validateForm()) {
        return;
      }
      
      this.isLoading = true;
      
      try {
        // IMPORTANT: Clear old session data first to prevent showing wrong user
        localStorage.removeItem('ramyeon_user_session');
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        
        // Call backend API to login
        const response = await authAPI.login(
          this.formData.email.toLowerCase().trim(),
          this.formData.password
        );
        
        console.log('🔍 DEBUG: Login response:', response);
        
        // Check if token was set (authAPI.login sets it in localStorage)
        const token = localStorage.getItem('access_token');
        console.log('🔍 DEBUG: Token in localStorage after login:', !!token);
        
        // If no token, check if response has token data
        if (!token) {
          // Check if token is in response but wasn't set (different structure)
          const responseToken = response?.access_token || response?.token || response?.data?.access_token;
          if (responseToken) {
            console.log('🔍 DEBUG: Found token in response, setting manually');
            localStorage.setItem('access_token', responseToken);
          } else {
            // Log warning but don't fail - maybe token is set via cookies or different mechanism
            console.warn('⚠️ No token found in response or localStorage, but login succeeded');
            console.warn('⚠️ Response structure:', Object.keys(response || {}));
            // Don't throw error - let it proceed and see if profile fetch works
            // The profile component will handle the missing token case
          }
        }
        
        console.log('✅ Login successful, token set:', !!localStorage.getItem('access_token'));
        
        // Create user session from API response
        // Backend returns: { access_token, user, ... } or legacy { customer }
        const customer = response.customer || response.user || {};
        const userSession = {
          id: customer._id || customer.id,
          email: customer.email,
          username: customer.username,
          fullName: customer.full_name,
          firstName: customer.full_name ? customer.full_name.split(' ')[0] : '',
          lastName: customer.full_name ? customer.full_name.split(' ').slice(1).join(' ') : '',
          phone: customer.phone || '',
          points: customer.loyalty_points || 0,
          deliveryAddress: customer.delivery_address || {},
          loginTime: new Date().toISOString()
        };
        
        // Save session to localStorage
        localStorage.setItem('ramyeon_user_session', JSON.stringify(userSession));
        
        if (this.formData.rememberMe) {
          localStorage.setItem('ramyeon_remember_user', this.formData.email);
        }
        
        this.successMessage = response.message || 'Login successful! Welcome back!';
        
        // Emit login success immediately (no delay needed)
        this.$emit('loginSuccess', userSession);
        
      } catch (error) {
        console.error('Login error:', error);
        console.error('Login error details:', JSON.stringify(error, null, 2));
        
        // Handle specific error messages from backend
        let errorMsg = 'Invalid email or password. Please try again.';
        
        if (typeof error === 'string') {
          errorMsg = error;
        } else if (error.error) {
          errorMsg = error.error;
        } else if (error.detail) {
          errorMsg = error.detail;
        } else if (error.message) {
          errorMsg = error.message;
        } else if (error.non_field_errors && Array.isArray(error.non_field_errors)) {
          errorMsg = error.non_field_errors[0];
        } else if (error.non_field_errors) {
          errorMsg = error.non_field_errors;
        }
        
        this.errorMessage = errorMsg;
      } finally {
        this.isLoading = false;
      }
    },
    
    togglePassword() {
      this.showPassword = !this.showPassword;
    },
    
    handleForgotPassword() {
      alert('Forgot password functionality will be implemented soon!');
    },
    
    socialLogin(provider) {
      if (this.isLoading) return;
      
      this.isLoading = true;
      
      // Simulate social login
      setTimeout(() => {
        const mockUser = {
          id: Date.now(),
          email: `user@${provider}.com`,
          firstName: 'Social',
          lastName: 'User',
          phone: '+1234567890',
          points: 3280,
          vouchers: [
            {
              id: 1,
              title: 'Shin Ramyun',
              subtitle: 'Spicy Noodle',
              discount: '20% OFF',
              code: 'SHIN20',
              qrCode: 'SHIN20-QR-' + Date.now()
            }
          ],
          loginTime: new Date().toISOString()
        };
        
        localStorage.setItem('ramyeon_user_session', JSON.stringify(mockUser));
        this.successMessage = `${provider} login successful! Redirecting...`;
        
        setTimeout(() => {
          this.$emit('loginSuccess', mockUser);
        }, 1000);
        
        this.isLoading = false;
      }, 1500);
    }
  },
  
  mounted() {
    // Check if user should be remembered
    const rememberedEmail = localStorage.getItem('ramyeon_remember_user');
    if (rememberedEmail) {
      this.formData.email = rememberedEmail;
      this.formData.rememberMe = true;
    }
  }
}
</script>

<style scoped src="./AuthStyles.css"></style>
