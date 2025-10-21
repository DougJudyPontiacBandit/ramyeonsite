<template>
  <div class="settings-wrapper" :class="{ 'dark-mode': isDarkMode }">
    <div class="settings-container">
      <!-- Header Section -->
      <div class="settings-header">
        <button class="back-button" @click="$emit('setCurrentPage', 'Profile')">
          <span>←</span> Back to Profile
        </button>
        <h1 class="header-title">Profile Settings</h1>
        <p class="header-subtitle">Manage your personal information and preferences</p>
      </div>

      <!-- Messages -->
      <transition name="slide-down">
        <div v-if="successMessage" class="alert alert-success">
          <span class="alert-icon">✓</span>
          <span class="alert-text">{{ successMessage }}</span>
        </div>
      </transition>

      <transition name="slide-down">
        <div v-if="errorMessage" class="alert alert-error">
          <span class="alert-icon">✕</span>
          <span class="alert-text">{{ errorMessage }}</span>
        </div>
      </transition>

      <!-- Profile Picture Card -->
      <div class="settings-card">
        <div class="card-header">
          <h2 class="card-title">
            <span class="title-icon">📸</span>
            Profile Picture
          </h2>
        </div>
        <div class="card-body center">
          <div class="avatar-section">
            <div class="avatar-wrapper" @click="triggerFileUpload">
              <div class="avatar-container">
                <img v-if="profileData.profilePicture" :src="profileData.profilePicture" alt="Profile" class="avatar-image" />
                <div v-else class="avatar-placeholder">
                  <span class="avatar-initials">{{ getInitials() }}</span>
                </div>
                <div class="avatar-overlay">
                  <span class="camera-icon">📷</span>
                  <span class="upload-text">Change Photo</span>
                </div>
              </div>
              <div class="avatar-badge">✏️</div>
            </div>
            <input 
              type="file" 
              ref="fileInput" 
              @change="handleFileUpload" 
              accept="image/*" 
              style="display: none;"
            />
            <p class="avatar-hint">Click to upload a new profile picture (Max 2MB)</p>
          </div>
        </div>
      </div>

      <!-- Personal Information Card -->
      <div class="settings-card">
        <div class="card-header">
          <h2 class="card-title">
            <span class="title-icon">👤</span>
            Personal Information
          </h2>
        </div>
        <div class="card-body">
          <form @submit.prevent="updateProfile">
            <div class="form-grid">
              <div class="form-group">
                <label class="form-label">
                  First Name <span class="required">*</span>
                </label>
                <div class="input-wrapper">
                  <input
                    type="text"
                    v-model="profileData.firstName"
                    :class="['form-input', { 'has-error': validationErrors.firstName }]"
                    placeholder="Enter first name"
                    required
                    @blur="validateField('firstName')"
                  />
                  <span class="input-icon">👤</span>
                </div>
                <transition name="fade">
                  <span v-if="validationErrors.firstName" class="error-text">
                    {{ validationErrors.firstName }}
                  </span>
                </transition>
              </div>

              <div class="form-group">
                <label class="form-label">
                  Last Name <span class="required">*</span>
                </label>
                <div class="input-wrapper">
                  <input
                    type="text"
                    v-model="profileData.lastName"
                    :class="['form-input', { 'has-error': validationErrors.lastName }]"
                    placeholder="Enter last name"
                    required
                    @blur="validateField('lastName')"
                  />
                  <span class="input-icon">👤</span>
                </div>
                <transition name="fade">
                  <span v-if="validationErrors.lastName" class="error-text">
                    {{ validationErrors.lastName }}
                  </span>
                </transition>
              </div>

              <div class="form-group">
                <label class="form-label">
                  Email Address <span class="required">*</span>
                </label>
                <div class="input-wrapper">
                  <input
                    type="email"
                    v-model="profileData.email"
                    :class="['form-input', { 'has-error': validationErrors.email }]"
                    placeholder="your.email@example.com"
                    required
                    @blur="validateField('email')"
                  />
                  <span class="input-icon">📧</span>
                </div>
                <transition name="fade">
                  <span v-if="validationErrors.email" class="error-text">
                    {{ validationErrors.email }}
                  </span>
                </transition>
              </div>

              <div class="form-group">
                <label class="form-label">
                  Phone Number <span class="required">*</span>
                </label>
                <div class="input-wrapper">
                  <input
                    type="tel"
                    v-model="profileData.phone"
                    :class="['form-input', { 'has-error': validationErrors.phone }]"
                    placeholder="+63 XXX XXX XXXX"
                    required
                    @blur="validateField('phone')"
                  />
                  <span class="input-icon">📱</span>
                </div>
                <transition name="fade">
                  <span v-if="validationErrors.phone" class="error-text">
                    {{ validationErrors.phone }}
                  </span>
                </transition>
              </div>

              <div class="form-group full-width">
                <label class="form-label">Delivery Address</label>
                <div class="input-wrapper">
                  <textarea
                    v-model="profileData.address"
                    class="form-input form-textarea"
                    rows="3"
                    placeholder="Enter your complete delivery address"
                  ></textarea>
                  <span class="input-icon">📍</span>
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">Date of Birth</label>
                <div class="input-wrapper">
                  <input
                    type="date"
                    v-model="profileData.birthdate"
                    class="form-input"
                    :max="maxBirthdate"
                  />
                  <span class="input-icon">🎂</span>
                </div>
              </div>
            </div>

            <div class="form-actions">
              <button 
                type="submit" 
                class="btn-save"
                :disabled="isLoading || hasValidationErrors"
              >
                <span v-if="isLoading" class="spinner"></span>
                <span v-else>💾</span>
                {{ isLoading ? 'Saving Changes...' : 'Save Changes' }}
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Security & Password Card -->
      <div class="settings-card">
        <div class="card-header">
          <h2 class="card-title">
            <span class="title-icon">🔐</span>
            Security & Password
          </h2>
        </div>
        <div class="card-body">
          <form @submit.prevent="changePassword">
            <div class="form-grid">
              <div class="form-group full-width">
                <label class="form-label">
                  Current Password <span class="required">*</span>
                </label>
                <div class="input-wrapper">
                  <input
                    :type="showCurrentPassword ? 'text' : 'password'"
                    v-model="passwordData.currentPassword"
                    class="form-input"
                    placeholder="Enter current password"
                    required
                  />
                  <button
                    type="button"
                    class="password-toggle"
                    @click="showCurrentPassword = !showCurrentPassword"
                    tabindex="-1"
                  >
                    {{ showCurrentPassword ? '👁️' : '👁️‍🗨️' }}
                  </button>
                </div>
              </div>

              <div class="form-group full-width">
                <label class="form-label">
                  New Password <span class="required">*</span>
                </label>
                <div class="input-wrapper">
                  <input
                    :type="showNewPassword ? 'text' : 'password'"
                    v-model="passwordData.newPassword"
                    :class="['form-input', { 'has-error': passwordData.newPassword && !isPasswordStrong }]"
                    placeholder="Enter new password"
                    required
                    minlength="8"
                    @input="checkPasswordStrength"
                  />
                  <button
                    type="button"
                    class="password-toggle"
                    @click="showNewPassword = !showNewPassword"
                    tabindex="-1"
                  >
                    {{ showNewPassword ? '👁️' : '👁️‍🗨️' }}
                  </button>
                </div>
                <transition name="fade">
                  <div v-if="passwordData.newPassword" class="password-strength">
                    <div class="strength-bars">
                      <div 
                        v-for="i in 4" 
                        :key="i"
                        class="strength-bar"
                        :class="{ 
                          'active': i <= passwordStrength.level,
                          [passwordStrength.class]: i <= passwordStrength.level
                        }"
                      ></div>
                    </div>
                    <span class="strength-label" :class="passwordStrength.class">
                      {{ passwordStrength.text }}
                    </span>
                  </div>
                </transition>
              </div>

              <div class="form-group full-width">
                <label class="form-label">
                  Confirm New Password <span class="required">*</span>
                </label>
                <div class="input-wrapper">
                  <input
                    :type="showConfirmPassword ? 'text' : 'password'"
                    v-model="passwordData.confirmPassword"
                    :class="['form-input', { 'has-error': passwordData.confirmPassword && passwordData.newPassword !== passwordData.confirmPassword }]"
                    placeholder="Confirm new password"
                    required
                  />
                  <button
                    type="button"
                    class="password-toggle"
                    @click="showConfirmPassword = !showConfirmPassword"
                    tabindex="-1"
                  >
                    {{ showConfirmPassword ? '👁️' : '👁️‍🗨️' }}
                  </button>
                </div>
                <transition name="fade">
                  <span 
                    v-if="passwordData.confirmPassword && passwordData.newPassword !== passwordData.confirmPassword" 
                    class="error-text"
                  >
                    Passwords do not match
                  </span>
                </transition>
              </div>
            </div>

            <div class="form-actions">
              <button 
                type="submit" 
                class="btn-secondary"
                :disabled="isPasswordLoading || !isPasswordValid"
              >
                <span v-if="isPasswordLoading" class="spinner"></span>
                <span v-else>🔑</span>
                {{ isPasswordLoading ? 'Changing Password...' : 'Update Password' }}
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Notification Preferences Card -->
      <div class="settings-card">
        <div class="card-header">
          <h2 class="card-title">
            <span class="title-icon">🔔</span>
            Notification Preferences
          </h2>
        </div>
        <div class="card-body">
          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-icon">📧</span>
              <div class="setting-text">
                <div class="setting-label">Email Notifications</div>
                <div class="setting-desc">Receive promotional emails and order updates</div>
              </div>
            </div>
            <label class="toggle">
              <input type="checkbox" v-model="profileData.emailNotifications" @change="togglePreference('emailNotifications')">
              <span class="toggle-slider"></span>
            </label>
          </div>

          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-icon">💬</span>
              <div class="setting-text">
                <div class="setting-label">SMS Notifications</div>
                <div class="setting-desc">Get text messages for order status updates</div>
              </div>
            </div>
            <label class="toggle">
              <input type="checkbox" v-model="profileData.smsNotifications" @change="togglePreference('smsNotifications')">
              <span class="toggle-slider"></span>
            </label>
          </div>

          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-icon">🎁</span>
              <div class="setting-text">
                <div class="setting-label">Marketing Communications</div>
                <div class="setting-desc">Receive special offers and promotions</div>
              </div>
            </div>
            <label class="toggle">
              <input type="checkbox" v-model="profileData.marketingEmails" @change="togglePreference('marketingEmails')">
              <span class="toggle-slider"></span>
            </label>
          </div>

          <div class="form-actions">
            <button class="btn-primary" @click="savePreferences" :disabled="isSavingPreferences">
              <span v-if="isSavingPreferences" class="spinner"></span>
              <span v-else>💾</span>
              {{ isSavingPreferences ? 'Saving Preferences...' : 'Save Preferences' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Danger Zone Card -->
      <div class="settings-card danger-card">
        <div class="card-header">
          <h2 class="card-title">
            <span class="title-icon">⚠️</span>
            Danger Zone
          </h2>
        </div>
        <div class="card-body">
          <div class="danger-actions">
            <button class="danger-btn outline" @click="exportData">
              <span class="btn-icon">📥</span>
              <div class="btn-text">
                <div class="btn-label">Export My Data</div>
                <div class="btn-desc">Download your profile information</div>
              </div>
            </button>

            <button class="danger-btn solid" @click="confirmDeleteAccount">
              <span class="btn-icon">🗑️</span>
              <div class="btn-text">
                <div class="btn-label">Delete Account</div>
                <div class="btn-desc">Permanently remove your account</div>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Account Modal -->
    <transition name="modal">
      <div v-if="showDeleteModal" class="modal-overlay" @click="showDeleteModal = false">
        <div class="modal" @click.stop>
          <div class="modal-header danger">
            <h3>⚠️ Delete Account</h3>
            <button class="modal-close" @click="showDeleteModal = false">✕</button>
          </div>
          <div class="modal-body">
            <div class="warning-box">
              <p><strong>This action cannot be undone.</strong></p>
              <p>This will permanently delete your account and remove all your data from our servers.</p>
            </div>
            <div class="deletion-list">
              <h4>What will be deleted:</h4>
              <ul>
                <li>All your profile information</li>
                <li>Order history</li>
                <li>Loyalty points and rewards</li>
                <li>Saved addresses and payment methods</li>
              </ul>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn-secondary" @click="showDeleteModal = false">Cancel</button>
            <button class="btn-danger" @click="deleteAccount">Delete Account</button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: 'ProfileSettings',
  emits: ['setCurrentPage'],
  data() {
    return {
      profileData: {
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        address: '',
        birthdate: '',
        profilePicture: '',
        emailNotifications: true,
        smsNotifications: true,
        marketingEmails: false
      },
      passwordData: {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      },
      validationErrors: {},
      showCurrentPassword: false,
      showNewPassword: false,
      showConfirmPassword: false,
      isLoading: false,
      isPasswordLoading: false,
      isSavingPreferences: false,
      successMessage: '',
      errorMessage: '',
      showDeleteModal: false,
      isDarkMode: false,
      passwordStrength: {
        text: '',
        class: '',
        level: 0
      }
    }
  },
  computed: {
    maxBirthdate() {
      const today = new Date();
      const minAge = new Date(today.getFullYear() - 13, today.getMonth(), today.getDate());
      return minAge.toISOString().split('T')[0];
    },
    hasValidationErrors() {
      return Object.keys(this.validationErrors).length > 0;
    },
    isPasswordValid() {
      return (
        this.passwordData.currentPassword &&
        this.passwordData.newPassword &&
        this.passwordData.confirmPassword &&
        this.passwordData.newPassword === this.passwordData.confirmPassword &&
        this.passwordData.newPassword.length >= 8
      );
    },
    isPasswordStrong() {
      const password = this.passwordData.newPassword;
      const hasUpper = /[A-Z]/.test(password);
      const hasLower = /[a-z]/.test(password);
      const hasNumber = /[0-9]/.test(password);
      const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);
      const isLongEnough = password.length >= 8;
      
      return hasUpper && hasLower && hasNumber && hasSpecial && isLongEnough;
    }
  },
  mounted() {
    this.loadUserData();
    this.loadDarkModePreference();
    this.fetchCurrentUser();
  },
  methods: {
    async loadUserData() {
      const userSession = localStorage.getItem('ramyeon_user_session');
      if (userSession) {
        try {
          const userData = JSON.parse(userSession);
          this.profileData = {
            firstName: userData.firstName || userData.first_name || '',
            lastName: userData.lastName || userData.last_name || '',
            email: userData.email || '',
            phone: userData.phone || '',
            address: userData.address || (userData.delivery_address?.street || ''),
            birthdate: userData.birthdate || '',
            profilePicture: userData.profilePicture || userData.profile_picture || '',
            emailNotifications: userData.emailNotifications !== false,
            smsNotifications: userData.smsNotifications !== false,
            marketingEmails: userData.marketingEmails || false
          };
        } catch (error) {
          console.error('Error loading user data:', error);
        }
      }
    },

    async fetchCurrentUser() {
      try {
        const { authAPI } = await import('../services/api.js')
        const response = await authAPI.getProfile()
        const customer = response.customer || response
        
        const fullName = customer.full_name || `${customer.first_name || ''} ${customer.last_name || ''}`.trim()
        const names = fullName.split(' ')
        
        this.profileData = {
          ...this.profileData,
          firstName: names[0] || this.profileData.firstName,
          lastName: names.slice(1).join(' ') || this.profileData.lastName,
          email: customer.email || this.profileData.email,
          phone: customer.phone || this.profileData.phone,
          address: customer.delivery_address?.street || this.profileData.address,
          birthdate: customer.birthdate || this.profileData.birthdate,
          profilePicture: customer.profile_picture || this.profileData.profilePicture,
        }
      } catch (error) {
        console.log('Not logged in or error fetching profile:', error)
      }
    },

    loadDarkModePreference() {
      const darkMode = localStorage.getItem('ramyeon_dark_mode');
      this.isDarkMode = darkMode === 'true';
    },

    validateField(fieldName) {
      this.validationErrors = { ...this.validationErrors };
      delete this.validationErrors[fieldName];

      const value = this.profileData[fieldName];

      if (!value || value.trim() === '') {
        this.validationErrors[fieldName] = 'This field is required';
        return false;
      }

      if (fieldName === 'email') {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
          this.validationErrors[fieldName] = 'Please enter a valid email address';
          return false;
        }
      }

      if (fieldName === 'phone') {
        const phoneRegex = /^[+]?[(]?[0-9]{1,4}[)]?[\s.-]?[(]?[0-9]{1,4}[)]?[\s.-]?[0-9]{1,9}$/;
        if (!phoneRegex.test(value.replace(/\s/g, ''))) {
          this.validationErrors[fieldName] = 'Please enter a valid phone number';
          return false;
        }
      }

      if ((fieldName === 'firstName' || fieldName === 'lastName') && value.length < 2) {
        this.validationErrors[fieldName] = 'Name must be at least 2 characters';
        return false;
      }

      return true;
    },

    checkPasswordStrength() {
      const password = this.passwordData.newPassword;
      let strength = 0;
      
      if (password.length >= 8) strength++;
      if (password.length >= 12) strength++;
      if (/[a-z]/.test(password)) strength++;
      if (/[A-Z]/.test(password)) strength++;
      if (/[0-9]/.test(password)) strength++;
      if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) strength++;

      if (strength <= 2) {
        this.passwordStrength = { text: 'Weak', class: 'weak', level: 1 };
      } else if (strength <= 4) {
        this.passwordStrength = { text: 'Medium', class: 'medium', level: 2 };
      } else if (strength <= 5) {
        this.passwordStrength = { text: 'Strong', class: 'strong', level: 3 };
      } else {
        this.passwordStrength = { text: 'Very Strong', class: 'very-strong', level: 4 };
      }
    },

    async updateProfile() {
      const fieldsToValidate = ['firstName', 'lastName', 'email', 'phone'];
      let isValid = true;
      
      fieldsToValidate.forEach(field => {
        if (!this.validateField(field)) {
          isValid = false;
        }
      });

      if (!isValid) {
        this.showErrorMessage('Please fix the validation errors before submitting');
        return;
      }

      this.isLoading = true;

      try {
        const { authAPI } = await import('../services/api.js')
        
        const updateData = {
          full_name: `${this.profileData.firstName} ${this.profileData.lastName}`.trim(),
          email: this.profileData.email,
          phone: this.profileData.phone,
          delivery_address: {
            street: this.profileData.address
          },
          birthdate: this.profileData.birthdate,
          profile_picture: this.profileData.profilePicture
        };

        const response = await authAPI.updateProfile(updateData);
        
        const userSession = JSON.parse(localStorage.getItem('ramyeon_user_session') || '{}');
        const updatedUser = {
          ...userSession,
          firstName: this.profileData.firstName,
          lastName: this.profileData.lastName,
          email: this.profileData.email,
          phone: this.profileData.phone,
          address: this.profileData.address,
          birthdate: this.profileData.birthdate,
          profilePicture: this.profileData.profilePicture,
          updatedAt: new Date().toISOString()
        };
        localStorage.setItem('ramyeon_user_session', JSON.stringify(updatedUser));

        this.showSuccessMessage(response.message || 'Profile updated successfully!');

      } catch (error) {
        console.error('Profile update error:', error);
        this.showErrorMessage(error.error || error.message || 'Failed to update profile. Please try again.');
      } finally {
        this.isLoading = false;
      }
    },

    async changePassword() {
      if (!this.isPasswordValid) {
        this.showErrorMessage('Please check your password entries');
        return;
      }

      this.isPasswordLoading = true;

      try {
        const { authAPI } = await import('../services/api.js')
        
        const response = await authAPI.changePassword(
          this.passwordData.currentPassword,
          this.passwordData.newPassword
        );

        this.passwordData = {
          currentPassword: '',
          newPassword: '',
          confirmPassword: ''
        };
        this.passwordStrength = { text: '', class: '', level: 0 };

        this.showSuccessMessage(response.message || 'Password changed successfully!');

      } catch (error) {
        console.error('Password change error:', error);
        this.showErrorMessage(error.error || error.message || 'Failed to change password.');
      } finally {
        this.isPasswordLoading = false;
      }
    },

    togglePreference(preference) {
      // Preference already toggled by v-model, but we can log which one
      console.log(`Preference ${preference} toggled`);
    },

    async savePreferences() {
      this.isSavingPreferences = true;
      
      try {
        const { authAPI } = await import('../services/api.js')
        
        const preferences = {
          emailNotifications: this.profileData.emailNotifications,
          smsNotifications: this.profileData.smsNotifications,
          marketingEmails: this.profileData.marketingEmails
        };

        await authAPI.updateProfile({ preferences });

        const userSession = JSON.parse(localStorage.getItem('ramyeon_user_session') || '{}');
        localStorage.setItem('ramyeon_user_session', JSON.stringify({ ...userSession, ...preferences }));

        this.showSuccessMessage('Preferences saved successfully!');
      } catch (error) {
        const userSession = JSON.parse(localStorage.getItem('ramyeon_user_session') || '{}');
        localStorage.setItem('ramyeon_user_session', JSON.stringify({
          ...userSession,
          emailNotifications: this.profileData.emailNotifications,
          smsNotifications: this.profileData.smsNotifications,
          marketingEmails: this.profileData.marketingEmails
        }));
        this.showSuccessMessage('Preferences saved locally!');
      } finally {
        this.isSavingPreferences = false;
      }
    },

    getInitials() {
      const first = this.profileData.firstName || 'U';
      const last = this.profileData.lastName || 'S';
      return `${first.charAt(0)}${last.charAt(0)}`.toUpperCase();
    },

    triggerFileUpload() {
      this.$refs.fileInput.click();
    },

    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        if (file.size > 2 * 1024 * 1024) {
          this.showErrorMessage('Image size must be less than 2MB');
          return;
        }

        if (!file.type.startsWith('image/')) {
          this.showErrorMessage('Please upload an image file');
          return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
          this.profileData.profilePicture = e.target.result;
          this.showSuccessMessage('Profile picture updated! Click "Save Changes" to save.');
        };
        reader.readAsDataURL(file);
      }
    },

    exportData() {
      const userSession = JSON.parse(localStorage.getItem('ramyeon_user_session') || '{}');
      const dataToExport = {
        profile: this.profileData,
        points: userSession.points || 0,
        vouchers: userSession.vouchers || [],
        exportDate: new Date().toISOString(),
        version: '2.0.0'
      };

      const dataStr = JSON.stringify(dataToExport, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);
      
      const link = document.createElement('a');
      link.href = url;
      link.download = `ramyeon-profile-${new Date().toISOString().split('T')[0]}.json`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);

      this.showSuccessMessage('Data exported successfully!');
    },

    confirmDeleteAccount() {
      this.showDeleteModal = true;
    },

    async deleteAccount() {
      localStorage.removeItem('ramyeon_user_session');
      localStorage.removeItem('ramyeon_remember_user');
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      
      this.showDeleteModal = false;
      this.$emit('setCurrentPage', 'Home');
      
      setTimeout(() => {
        alert('Account deleted successfully.');
      }, 500);
    },

    showSuccessMessage(text) {
      this.successMessage = text;
      this.errorMessage = '';
      setTimeout(() => {
        this.successMessage = '';
      }, 5000);
    },

    showErrorMessage(text) {
      this.errorMessage = text;
      this.successMessage = '';
      setTimeout(() => {
        this.errorMessage = '';
      }, 5000);
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

* {
  font-family: 'Poppins', sans-serif;
  box-sizing: border-box;
}

.settings-wrapper {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 2rem 1rem;
}

.dark-mode {
  background: #1a1a1a;
  color: #fff;
}

.settings-container {
  max-width: 800px;
  margin: 0 auto;
}

/* Header */
.settings-header {
  margin-bottom: 2rem;
}

.back-button {
  background: white;
  border: 2px solid #e0e0e0;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 1rem;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.back-button:hover {
  background: #f5f5f5;
  border-color: #ff4b4b;
}

.dark-mode .back-button {
  background: #2a2a2a;
  border-color: #444;
  color: #fff;
}

.header-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #333;
  margin: 0 0 0.5rem 0;
}

.dark-mode .header-title {
  color: #fff;
}

.header-subtitle {
  color: #666;
  font-size: 1.1rem;
  margin: 0;
}

.dark-mode .header-subtitle {
  color: #aaa;
}

/* Alerts */
.alert {
  padding: 1rem 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 600;
  border: 2px solid;
}

.alert-success {
  background: linear-gradient(135deg, #d1fae5, #a7f3d0);
  color: #065f46;
  border-color: #6ee7b7;
}

.alert-error {
  background: linear-gradient(135deg, #fee2e2, #fecaca);
  color: #991b1b;
  border-color: #fca5a5;
}

.alert-icon {
  font-size: 1.25rem;
}

/* Card */
.settings-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
  overflow: hidden;
}

.dark-mode .settings-card {
  background: #2a2a2a;
}

.card-header {
  padding: 1.5rem;
  border-bottom: 2px solid #f0f0f0;
  background: linear-gradient(135deg, rgba(255, 75, 75, 0.05), rgba(255, 92, 51, 0.05));
}

.dark-mode .card-header {
  border-bottom-color: #444;
  background: linear-gradient(135deg, rgba(255, 75, 75, 0.1), rgba(255, 92, 51, 0.1));
}

.card-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #333;
}

.dark-mode .card-title {
  color: #fff;
}

.title-icon {
  font-size: 1.75rem;
}

.card-body {
  padding: 1.5rem;
}

.card-body.center {
  text-align: center;
}

/* Avatar Section */
.avatar-section {
  display: inline-block;
}

.avatar-wrapper {
  position: relative;
  display: inline-block;
  cursor: pointer;
  margin-bottom: 1rem;
}

.avatar-container {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  position: relative;
  border: 4px solid #ff4b4b;
  box-shadow: 0 4px 12px rgba(255, 75, 75, 0.3);
  transition: all 0.3s ease;
}

.avatar-wrapper:hover .avatar-container {
  transform: scale(1.05);
  box-shadow: 0 6px 20px rgba(255, 75, 75, 0.4);
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #ff4b4b, #ff5c33);
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-initials {
  font-size: 2.5rem;
  font-weight: 700;
  color: white;
}

.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
  gap: 0.5rem;
}

.avatar-container:hover .avatar-overlay {
  opacity: 1;
}

.camera-icon {
  font-size: 2rem;
}

.upload-text {
  color: white;
  font-size: 0.875rem;
  font-weight: 600;
}

.avatar-badge {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #ff4b4b, #ff5c33);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.125rem;
  border: 3px solid white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.avatar-hint {
  color: #666;
  font-size: 0.9rem;
  margin: 0;
}

.dark-mode .avatar-hint {
  color: #aaa;
}

/* Form */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-label {
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}

.dark-mode .form-label {
  color: #fff;
}

.required {
  color: #ff4b4b;
}

.input-wrapper {
  position: relative;
}

.form-input {
  width: 100%;
  padding: 0.875rem 3rem 0.875rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
  color: #333;
}

.form-input:focus {
  outline: none;
  border-color: #ff4b4b;
  box-shadow: 0 0 0 3px rgba(255, 75, 75, 0.1);
}

.form-input.has-error {
  border-color: #ff4b4b;
  background: rgba(255, 75, 75, 0.05);
}

.dark-mode .form-input {
  background: #1f1f1f;
  color: #fff;
  border-color: #444;
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
  padding-right: 1rem;
}

.input-icon {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.25rem;
  pointer-events: none;
}

.form-textarea + .input-icon {
  top: 1rem;
  transform: none;
}

.password-toggle {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.25rem;
  padding: 0.25rem;
  transition: transform 0.2s ease;
}

.password-toggle:hover {
  transform: translateY(-50%) scale(1.1);
}

.error-text {
  color: #ff4b4b;
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

/* Password Strength */
.password-strength {
  margin-top: 0.75rem;
}

.strength-bars {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.strength-bar {
  flex: 1;
  height: 4px;
  background: #e0e0e0;
  border-radius: 2px;
  transition: all 0.3s ease;
}

.strength-bar.active.weak {
  background: #ff4b4b;
}

.strength-bar.active.medium {
  background: #ffa500;
}

.strength-bar.active.strong {
  background: #10b981;
}

.strength-bar.active.very-strong {
  background: #059669;
}

.strength-label {
  font-size: 0.875rem;
  font-weight: 600;
}

.strength-label.weak {
  color: #ff4b4b;
}

.strength-label.medium {
  color: #ffa500;
}

.strength-label.strong {
  color: #10b981;
}

.strength-label.very-strong {
  color: #059669;
}

/* Setting Row */
.setting-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem;
  border-radius: 8px;
  border: 2px solid #f0f0f0;
  margin-bottom: 1rem;
  transition: all 0.3s ease;
}

.setting-row:hover {
  border-color: #ff4b4b;
  background: rgba(255, 75, 75, 0.02);
}

.dark-mode .setting-row {
  border-color: #444;
  background: #1f1f1f;
}

.setting-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

.setting-icon {
  font-size: 2rem;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(255, 75, 75, 0.1), rgba(255, 92, 51, 0.1));
  border-radius: 10px;
  flex-shrink: 0;
}

.setting-label {
  font-weight: 600;
  font-size: 1.05rem;
  color: #333;
  margin-bottom: 0.25rem;
}

.dark-mode .setting-label {
  color: #fff;
}

.setting-desc {
  color: #666;
  font-size: 0.9rem;
}

.dark-mode .setting-desc {
  color: #aaa;
}

/* Toggle Switch */
.toggle {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
  flex-shrink: 0;
}

.toggle input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: 0.4s;
  border-radius: 34px;
  border: 2px solid #e0e0e0;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 24px;
  width: 24px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.4s;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.toggle input:checked + .toggle-slider {
  background: linear-gradient(135deg, #ff4b4b, #ff5c33);
  border-color: #ff4b4b;
}

.toggle input:focus + .toggle-slider {
  box-shadow: 0 0 4px #ff4b4b;
}

.toggle input:checked + .toggle-slider:before {
  transform: translateX(26px);
}

/* Buttons */
.form-actions {
  margin-top: 1.5rem;
  display: flex;
  gap: 1rem;
}

.btn-save,
.btn-primary,
.btn-secondary {
  padding: 1rem 2rem;
  border-radius: 8px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.btn-save,
.btn-primary {
  background: linear-gradient(135deg, #ff4b4b, #ff5c33);
  color: white;
}

.btn-save:hover:not(:disabled),
.btn-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #ff5c33, #ff6b43);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 75, 75, 0.3);
}

.btn-secondary {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
}

.btn-secondary:hover:not(:disabled) {
  background: linear-gradient(135deg, #8b5cf6, #a855f7);
  transform: translateY(-2px);
}

.btn-save:disabled,
.btn-primary:disabled,
.btn-secondary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Danger Card */
.danger-card .card-header {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.05), rgba(220, 38, 38, 0.05));
}

.danger-actions {
  display: grid;
  gap: 1rem;
}

.danger-btn {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  border: 2px solid;
}

.danger-btn.outline {
  background: white;
  border-color: #e0e0e0;
  color: #333;
}

.danger-btn.outline:hover {
  border-color: #ff4b4b;
  background: rgba(255, 75, 75, 0.05);
  transform: translateY(-2px);
}

.danger-btn.solid {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  border-color: #ef4444;
  color: white;
}

.danger-btn.solid:hover {
  background: linear-gradient(135deg, #dc2626, #b91c1c);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.dark-mode .danger-btn.outline {
  background: #1f1f1f;
  border-color: #444;
  color: #fff;
}

.btn-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.btn-label {
  font-size: 1.05rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.btn-desc {
  font-size: 0.9rem;
  opacity: 0.8;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal {
  background: white;
  border-radius: 12px;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.dark-mode .modal {
  background: #2a2a2a;
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 2px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header.danger {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(220, 38, 38, 0.1));
}

.dark-mode .modal-header {
  border-bottom-color: #444;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
}

.dark-mode .modal-header h3 {
  color: #fff;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
  transition: all 0.3s ease;
  width: 35px;
  height: 35px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.modal-close:hover {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  transform: rotate(90deg);
}

.modal-body {
  padding: 1.5rem;
}

.modal-body p {
  color: #333;
  margin-bottom: 1rem;
  line-height: 1.6;
}

.dark-mode .modal-body p {
  color: #ddd;
}

.warning-box {
  background: rgba(239, 68, 68, 0.1);
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #ef4444;
  margin-bottom: 1rem;
}

.deletion-list h4 {
  margin: 0 0 0.75rem 0;
  color: #333;
}

.dark-mode .deletion-list h4 {
  color: #fff;
}

.deletion-list ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.deletion-list li {
  padding: 0.5rem 0;
  color: #666;
  border-bottom: 1px solid #f0f0f0;
}

.dark-mode .deletion-list li {
  color: #aaa;
  border-bottom-color: #444;
}

.deletion-list li:last-child {
  border-bottom: none;
}

.deletion-list li::before {
  content: '✕';
  color: #ef4444;
  font-weight: bold;
  margin-right: 0.75rem;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid #f0f0f0;
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.dark-mode .modal-footer {
  border-top-color: #444;
}

.btn-danger {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-danger:hover {
  background: linear-gradient(135deg, #dc2626, #b91c1c);
  transform: translateY(-2px);
}

/* Transitions */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from {
  opacity: 0;
  transform: translateY(-20px);
}

.slide-down-leave-to {
  opacity: 0;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal,
.modal-leave-to .modal {
  transform: scale(0.9);
}

/* Responsive */
@media (max-width: 768px) {
  .settings-wrapper {
    padding: 1rem 0.5rem;
  }

  .header-title {
    font-size: 2rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .form-group {
    grid-column: 1 / -1 !important;
  }

  .setting-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .toggle {
    align-self: flex-end;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn-save,
  .btn-primary,
  .btn-secondary {
    width: 100%;
    justify-content: center;
  }

  .modal-footer {
    flex-direction: column;
  }

  .modal-footer button {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .header-title {
    font-size: 1.75rem;
  }

  .avatar-container {
    width: 100px;
    height: 100px;
  }

  .avatar-initials {
    font-size: 2rem;
  }
}
</style>
