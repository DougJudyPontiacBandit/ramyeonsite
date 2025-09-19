<template>
  <div class="auth-container">
    <div class="auth-card">
      <img :src="logoSrc" alt="Ramyeon Corner Logo" class="auth-logo" />

      <h1 class="auth-title">Join Us!</h1>
      <p class="auth-subtitle">Already have an account? <a href="#" @click.prevent="$emit('switchToLogin')" class="create-link">Sign in here</a></p>

      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div>

      <form @submit.prevent="handleSignUp" class="auth-form">
        <div class="form-row">
          <div class="form-group half-width">
            <label for="firstName" class="form-label">First Name</label>
            <input
              type="text"
              id="firstName"
              v-model="formData.firstName"
              :class="['form-input', { error: errors.firstName, success: !errors.firstName && formData.firstName }]"
              placeholder="John"
              required
            />
            <span v-if="errors.firstName" class="field-error">{{ errors.firstName }}</span>
          </div>

          <div class="form-group half-width">
            <label for="lastName" class="form-label">Last Name</label>
            <input
              type="text"
              id="lastName"
              v-model="formData.lastName"
              :class="['form-input', { error: errors.lastName, success: !errors.lastName && formData.lastName }]"
              placeholder="Doe"
              required
            />
            <span v-if="errors.lastName" class="field-error">{{ errors.lastName }}</span>
          </div>
        </div>

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
          <label for="phone" class="form-label">Phone Number</label>
          <input
            type="tel"
            id="phone"
            v-model="formData.phone"
            :class="['form-input', { error: errors.phone, success: !errors.phone && formData.phone }]"
            placeholder="+63 912 345 6789"
            required
          />
          <span v-if="errors.phone" class="field-error">{{ errors.phone }}</span>
        </div>

        <div class="form-group">
          <label for="password" class="form-label">Password</label>
          <div style="position: relative;">
            <input
              :type="showPassword ? 'text' : 'password'"
              id="password"
              v-model="formData.password"
              :class="['form-input', { error: errors.password, success: !errors.password && formData.password }]"
              placeholder="Create a strong password"
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

        <div class="form-group">
          <label for="confirmPassword" class="form-label">Confirm Password</label>
          <div style="position: relative;">
            <input
              :type="showConfirmPassword ? 'text' : 'password'"
              id="confirmPassword"
              v-model="formData.confirmPassword"
              :class="['form-input', { error: errors.confirmPassword, success: !errors.confirmPassword && formData.confirmPassword }]"
              placeholder="Confirm your password"
              required
            />
            <button
              type="button"
              class="password-toggle"
              @click="toggleConfirmPassword"
              :aria-label="showConfirmPassword ? 'Hide password' : 'Show password'"
            >
              {{ showConfirmPassword ? '👁️' : '👁️‍🗨️' }}
            </button>
          </div>
          <span v-if="errors.confirmPassword" class="field-error">{{ errors.confirmPassword }}</span>
        </div>

        <div class="checkbox-group">
          <input type="checkbox" id="terms" v-model="formData.agreeToTerms" required />
          <label for="terms">
            I agree to the <a href="#" @click.prevent="showTerms">Terms of Service</a>
            and <a href="#" @click.prevent="showPrivacy">Privacy Policy</a>
          </label>
        </div>

        <div class="checkbox-group">
          <input type="checkbox" id="newsletter" v-model="formData.subscribeNewsletter" />
          <label for="newsletter">Subscribe to our newsletter for exclusive deals</label>
        </div>

        <button type="submit" class="auth-button" :disabled="isLoading">
          <span v-if="isLoading" class="loading-spinner"></span>
          {{ isLoading ? 'Creating Account...' : 'Create Account' }}
        </button>
      </form>

      <div class="auth-divider">OR</div>

      <div class="social-login">
        <button class="social-btn google-btn" @click="socialSignUp('google')" :disabled="isLoading">
          <img src="../assets/Nav Bar/git.png" alt="Google" />
          <span>Continue with Google</span>
        </button>
        <button class="social-btn facebook-btn" @click="socialSignUp('facebook')" :disabled="isLoading">
          <img src="../assets/Nav Bar/fb.png" alt="Facebook" />
          <span>Continue with Facebook</span>
        </button>
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
        <h2>ENJOY RAMYEON YOUR WAY!</h2>
        <h1>WELCOME BONUS</h1>
        <p>GET STARTED WITH</p>
        <h3>25% OFF</h3>
        <p class="bonus-text">Plus earn points with every order!</p>
        <button class="order-btn">Join Now</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SignUp',
  emits: ['switchToLogin', 'signUpSuccess', 'backToHome'],
  data() {
    return {
      formData: {
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        password: '',
        confirmPassword: '',
        agreeToTerms: false,
        subscribeNewsletter: false
      },
      errors: {},
      errorMessage: '',
      successMessage: '',
      isLoading: false,
      showPassword: false,
      showConfirmPassword: false,
      logoSrc: require('../assets/Nav Bar/Logo.png')
    }
  },
  methods: {
    validateForm() {
      this.errors = {};

      // First name validation
      if (!this.formData.firstName.trim()) {
        this.errors.firstName = 'First name is required';
      } else if (this.formData.firstName.trim().length < 2) {
        this.errors.firstName = 'First name must be at least 2 characters';
      }

      // Last name validation
      if (!this.formData.lastName.trim()) {
        this.errors.lastName = 'Last name is required';
      } else if (this.formData.lastName.trim().length < 2) {
        this.errors.lastName = 'Last name must be at least 2 characters';
      }

      // Email validation
      if (!this.formData.email) {
        this.errors.email = 'Email is required';
      } else if (!this.isValidEmail(this.formData.email)) {
        this.errors.email = 'Please enter a valid email address';
      }

      // Phone validation
      if (!this.formData.phone) {
        this.errors.phone = 'Phone number is required';
      } else if (!this.isValidPhone(this.formData.phone)) {
        this.errors.phone = 'Please enter a valid phone number';
      }

      // Password validation
      if (!this.formData.password) {
        this.errors.password = 'Password is required';
      } else if (this.formData.password.length < 8) {
        this.errors.password = 'Password must be at least 8 characters';
      } else if (!this.isStrongPassword(this.formData.password)) {
        this.errors.password = 'Password must contain at least one uppercase letter, one lowercase letter, and one number';
      }

      // Confirm password validation
      if (!this.formData.confirmPassword) {
        this.errors.confirmPassword = 'Please confirm your password';
      } else if (this.formData.password !== this.formData.confirmPassword) {
        this.errors.confirmPassword = 'Passwords do not match';
      }

      return Object.keys(this.errors).length === 0;
    },

    isValidEmail(email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(email);
    },

    isValidPhone(phone) {
      const phoneRegex = /^[+]?[1-9][\d]{0,15}$/;
      return phoneRegex.test(phone.replace(/[\s\-()]/g, ''));
    },

    isStrongPassword(password) {
      const strongRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/;
      return strongRegex.test(password);
    },

    async handleSignUp() {
      this.errorMessage = '';
      this.successMessage = '';

      if (!this.validateForm()) {
        return;
      }

      if (!this.formData.agreeToTerms) {
        this.errorMessage = 'Please agree to the Terms of Service and Privacy Policy';
        return;
      }

      this.isLoading = true;

      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Check if user already exists
        const users = JSON.parse(localStorage.getItem('ramyeon_users') || '[]');
        const existingUser = users.find(u => u.email === this.formData.email);

        if (existingUser) {
          this.errorMessage = 'An account with this email already exists. Please sign in instead.';
          return;
        }

        // Create new user
        const newUser = {
          id: Date.now(),
          firstName: this.formData.firstName.trim(),
          lastName: this.formData.lastName.trim(),
          email: this.formData.email.toLowerCase(),
          phone: this.formData.phone,
          password: this.formData.password, // In real app, this would be hashed
          points: 0, // New users start with 0 points
          vouchers: [
            // Welcome voucher for new users
            {
              id: 1,
              title: 'Welcome Bonus',
              subtitle: 'New Member Special',
              discount: '25% OFF',
              code: 'WELCOME25',
              qrCode: 'WELCOME25-QR-' + Date.now()
            }
          ],
          subscribeNewsletter: this.formData.subscribeNewsletter,
          createdAt: new Date().toISOString()
        };

        // Save user to localStorage
        users.push(newUser);
        localStorage.setItem('ramyeon_users', JSON.stringify(users));

        // Create user session
        const userSession = {
          id: newUser.id,
          email: newUser.email,
          firstName: newUser.firstName,
          lastName: newUser.lastName,
          phone: newUser.phone,
          points: newUser.points,
          vouchers: newUser.vouchers,
          loginTime: new Date().toISOString()
        };

        localStorage.setItem('ramyeon_user_session', JSON.stringify(userSession));

        this.successMessage = 'Account created successfully! Welcome to Ramyeon Corner!';

        setTimeout(() => {
          this.$emit('signUpSuccess', userSession);
        }, 1500);

      } catch (error) {
        this.errorMessage = 'An error occurred during registration. Please try again.';
        console.error('SignUp error:', error);
      } finally {
        this.isLoading = false;
      }
    },

    togglePassword() {
      this.showPassword = !this.showPassword;
    },

    toggleConfirmPassword() {
      this.showConfirmPassword = !this.showConfirmPassword;
    },

    showTerms() {
      alert('Terms of Service will be displayed here in a modal.');
    },

    showPrivacy() {
      alert('Privacy Policy will be displayed here in a modal.');
    },

    socialSignUp(provider) {
      if (this.isLoading) return;

      this.isLoading = true;

      // Simulate social signup
      setTimeout(() => {
        const mockUser = {
          id: Date.now(),
          email: `user@${provider}.com`,
          firstName: 'Social',
          lastName: 'User',
          phone: '+1234567890',
          points: 100, // Bonus points for social signup
          vouchers: [
            {
              id: 1,
              title: 'Social Signup Bonus',
              subtitle: 'Thank you for joining!',
              discount: '30% OFF',
              code: 'SOCIAL30',
              qrCode: 'SOCIAL30-QR-' + Date.now()
            }
          ],
          loginTime: new Date().toISOString()
        };

        localStorage.setItem('ramyeon_user_session', JSON.stringify(mockUser));
        this.successMessage = `${provider} signup successful! Welcome to Ramyeon Corner!`;

        setTimeout(() => {
          this.$emit('signUpSuccess', mockUser);
        }, 1000);

        this.isLoading = false;
      }, 1500);
    }
  }
}
</script>

<style src="./AuthStyles.css"></style>
