<template>
  <div class="auth-container login-page">
    <div class="auth-card" :class="{ 'slide-to-signup': isTransitioning }">
      <img :src="logoSrc" alt="Ramyeon Corner Logo" class="auth-logo" />
      
      <h1 class="auth-title">Sign In</h1>
      <p class="auth-subtitle">Don't have an account? <a href="#" @click.prevent="switchToSignUp" class="create-link">Create now</a></p>
      
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
      
      <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div>
      
      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label for="email" class="form-label">E-mail</label>
          <input
            type="email"
            id="email"
            v-model="formData.email"
            :class="['form-input', { error: errors.email, success: !errors.email && formData.email }]"
            placeholder="example@gmail.com"
            required
          />
          <span v-if="errors.email" class="field-error">{{ errors.email }}</span>
        </div>
        
        <div class="form-group">
          <label for="password" class="form-label">Password</label>
          <div style="position: relative;">
            <input
              :type="showPassword ? 'text' : 'password'"
              id="password"
              v-model="formData.password"
              :class="['form-input', { error: errors.password, success: !errors.password && formData.password }]"
              placeholder="@#*%"
              required
            />
            <button
              type="button"
              class="password-toggle"
              @click="togglePassword"
              :aria-label="showPassword ? 'Hide password' : 'Show password'"
            >
              {{ showPassword ? '👁️' : '👁️‍🗨️' }}
            </button>
          </div>
          <span v-if="errors.password" class="field-error">{{ errors.password }}</span>
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
          {{ isLoading ? 'Signing In...' : 'Sign in' }}
        </button>
      </form>
      
      <div class="auth-divider">OR</div>
      
      <div class="social-login">
        <button class="social-btn google" @click="socialLogin('google')" :disabled="isLoading">
          <img src="../assets/Nav Bar/fb.png" alt="Google" />
          <span>Continue with Google</span>
        </button>
        <button class="social-btn facebook" @click="socialLogin('facebook')" :disabled="isLoading">
          <img src="../assets/Nav Bar/fb.png" alt="Facebook" />
          <span>Continue with Facebook</span>
        </button>
      </div>
      
      <!-- Test Account Info -->
      <div class="test-account-info">
        <p><strong>Test Account:</strong></p>
        <p>Email: test@ramyeoncorner.com</p>
        <p>Password: Test123!</p>
      </div>

      <!-- Back to Home Button -->
      <button class="back-home-btn" @click="$emit('backToHome')">
        ← Back to Home
      </button>
    </div>
    
    <!-- Right side promotional content -->
    <div class="promo-content">
      <div class="promo-image">
        <img src="../assets/food/ramyeon-hero.jpg" alt="Delicious Ramyeon" class="ramyeon-image" />
      </div>
      <div class="promo-text">
        <h2>24 HOURS ONLY</h2>
        <h1>FLASH SALE</h1>
        <p>USE CODE: CORNER</p>
        <h3>30% OFF</h3>
        <button class="order-btn">Order Now</button>
      </div>
    </div>
  </div>
</template>

<script>
import { api } from '../api.js'

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
      isTransitioning: false,
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
        // Call backend API
        const response = await api.auth.login({
          email: this.formData.email,
          password: this.formData.password
        });

        const { user, access_token, token, refresh_token } = response.data;

        // Store auth token (support either field name)
        const accessToken = access_token || token;
        if (accessToken) {
          localStorage.setItem('auth_token', accessToken);
        }
        if (refresh_token) {
          localStorage.setItem('refresh_token', refresh_token);
        }

        // Store user session
        const userSession = {
          id: user.id || user._id,
          email: user.email,
          firstName: user.first_name || user.firstName || user.name?.split(' ')[0],
          lastName: user.last_name || user.lastName || (user.name?.split(' ').slice(1).join(' ') || ''),
          phone: user.phone,
          points: user.points || 3280,
          vouchers: user.vouchers || [
            {
              id: 1,
              title: 'Shin Ramyun',
              subtitle: 'Spicy Noodle',
              discount: '20% OFF',
              code: 'SHIN20',
              qrCode: 'SHIN20-QR-' + Date.now()
            },
            {
              id: 2,
              title: 'Fish Cake',
              subtitle: 'Side Dish',
              discount: '15% OFF',
              code: 'FISH15',
              qrCode: 'FISH15-QR-' + Date.now()
            }
          ],
          loginTime: new Date().toISOString()
        };

        localStorage.setItem('ramyeon_user_session', JSON.stringify(userSession));

        if (this.formData.rememberMe) {
          localStorage.setItem('ramyeon_remember_user', this.formData.email);
        }

        this.successMessage = 'Login successful! Redirecting...';

        setTimeout(() => {
          this.$emit('loginSuccess', userSession);
        }, 1000);

      } catch (error) {
        console.error('Login error:', error);

        if (error.response?.status === 401) {
          this.errorMessage = 'Invalid email or password. Please try again.';
        } else if (error.response?.status === 400) {
          this.errorMessage = error.response.data?.message || 'Invalid login credentials.';
        } else {
          this.errorMessage = 'An error occurred during login. Please try again.';
        }
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
    },
    
    switchToSignUp() {
      this.isTransitioning = true;
      setTimeout(() => {
        this.$emit('switchToSignUp');
        this.isTransitioning = false;
      }, 800);
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
