<template>
  <div class="profile-container" :class="{ 'dark-mode': isDarkMode }">
    <div class="profile-content">
      <!-- Header -->
      <div class="profile-header">
        <div class="profile-avatar">
          ⚙️
        </div>
        <h1 class="profile-name">Profile Settings</h1>
        <p class="profile-email">Manage your personal information</p>
      </div>

      <!-- Profile Settings Content -->
      <div class="profile-main">
        <div v-if="successMessage" class="message success">
          {{ successMessage }}
        </div>
        
        <div v-if="errorMessage" class="message error">
          {{ errorMessage }}
        </div>

        <!-- Personal Information -->
        <div class="settings-section">
          <div class="settings-group">
            <h3 class="settings-group-title">Personal Information</h3>
            
            <form @submit.prevent="updateProfile">
              <div class="form-group">
                <label for="firstName" class="form-label">First Name</label>
                <input
                  type="text"
                  id="firstName"
                  v-model="profileData.firstName"
                  class="form-input"
                  required
                />
              </div>
              
              <div class="form-group">
                <label for="lastName" class="form-label">Last Name</label>
                <input
                  type="text"
                  id="lastName"
                  v-model="profileData.lastName"
                  class="form-input"
                  required
                />
              </div>
              
              <div class="form-group">
                <label for="email" class="form-label">Email Address</label>
                <input
                  type="email"
                  id="email"
                  v-model="profileData.email"
                  class="form-input"
                  required
                />
              </div>
              
              <div class="form-group">
                <label for="phone" class="form-label">Phone Number</label>
                <input
                  type="tel"
                  id="phone"
                  v-model="profileData.phone"
                  class="form-input"
                  required
                />
              </div>
              
              <div class="form-group">
                <label for="address" class="form-label">Address</label>
                <textarea
                  id="address"
                  v-model="profileData.address"
                  class="form-input"
                  rows="3"
                  placeholder="Enter your delivery address"
                ></textarea>
              </div>
              
              <div class="form-group">
                <label for="birthdate" class="form-label">Date of Birth</label>
                <input
                  type="date"
                  id="birthdate"
                  v-model="profileData.birthdate"
                  class="form-input"
                />
              </div>
              
              <button type="submit" class="action-btn primary-btn" :disabled="isLoading">
                <span v-if="isLoading" class="loading-spinner"></span>
                {{ isLoading ? 'Updating...' : 'Update Profile' }}
              </button>
            </form>
          </div>
        </div>

        <!-- Account Security -->
        <div class="settings-section">
          <div class="settings-group">
            <h3 class="settings-group-title">Account Security</h3>
            
            <form @submit.prevent="changePassword">
              <div class="form-group">
                <label for="currentPassword" class="form-label">Current Password</label>
                <div style="position: relative;">
                  <input
                    :type="showCurrentPassword ? 'text' : 'password'"
                    id="currentPassword"
                    v-model="passwordData.currentPassword"
                    class="form-input"
                    required
                  />
                  <button
                    type="button"
                    class="password-toggle"
                    @click="showCurrentPassword = !showCurrentPassword"
                  >
                    {{ showCurrentPassword ? '👁️' : '👁️‍🗨️' }}
                  </button>
                </div>
              </div>
              
              <div class="form-group">
                <label for="newPassword" class="form-label">New Password</label>
                <div style="position: relative;">
                  <input
                    :type="showNewPassword ? 'text' : 'password'"
                    id="newPassword"
                    v-model="passwordData.newPassword"
                    class="form-input"
                    required
                    minlength="8"
                  />
                  <button
                    type="button"
                    class="password-toggle"
                    @click="showNewPassword = !showNewPassword"
                  >
                    {{ showNewPassword ? '👁️' : '👁️‍🗨️' }}
                  </button>
                </div>
              </div>
              
              <div class="form-group">
                <label for="confirmPassword" class="form-label">Confirm New Password</label>
                <div style="position: relative;">
                  <input
                    :type="showConfirmPassword ? 'text' : 'password'"
                    id="confirmPassword"
                    v-model="passwordData.confirmPassword"
                    class="form-input"
                    required
                  />
                  <button
                    type="button"
                    class="password-toggle"
                    @click="showConfirmPassword = !showConfirmPassword"
                  >
                    {{ showConfirmPassword ? '👁️' : '👁️‍🗨️' }}
                  </button>
                </div>
              </div>
              
              <button type="submit" class="action-btn secondary-btn" :disabled="isPasswordLoading">
                <span v-if="isPasswordLoading" class="loading-spinner"></span>
                {{ isPasswordLoading ? 'Changing...' : 'Change Password' }}
              </button>
            </form>
          </div>
        </div>

        <!-- Preferences -->
        <div class="settings-section">
          <div class="settings-group">
            <h3 class="settings-group-title">Preferences</h3>
            
            <div class="setting-item">
              <div class="setting-info">
                <div class="setting-label">Email Notifications</div>
                <div class="setting-description">Receive promotional emails and order updates</div>
              </div>
              <div class="setting-control">
                <div 
                  class="toggle-switch" 
                  :class="{ active: profileData.emailNotifications }"
                  @click="profileData.emailNotifications = !profileData.emailNotifications"
                ></div>
              </div>
            </div>
            
            <div class="setting-item">
              <div class="setting-info">
                <div class="setting-label">SMS Notifications</div>
                <div class="setting-description">Get text messages for order status updates</div>
              </div>
              <div class="setting-control">
                <div 
                  class="toggle-switch" 
                  :class="{ active: profileData.smsNotifications }"
                  @click="profileData.smsNotifications = !profileData.smsNotifications"
                ></div>
              </div>
            </div>
            
            <div class="setting-item">
              <div class="setting-info">
                <div class="setting-label">Marketing Communications</div>
                <div class="setting-description">Receive special offers and promotions</div>
              </div>
              <div class="setting-control">
                <div 
                  class="toggle-switch" 
                  :class="{ active: profileData.marketingEmails }"
                  @click="profileData.marketingEmails = !profileData.marketingEmails"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Account Actions -->
        <div class="settings-section">
          <div class="settings-group">
            <h3 class="settings-group-title">Account Actions</h3>
            
            <div class="profile-actions">
              <button class="action-btn secondary-btn" @click="exportData">
                📥 Export My Data
              </button>
              <button class="action-btn secondary-btn" @click="$emit('setCurrentPage', 'Profile')">
                ← Back to Profile
              </button>
              <button class="action-btn" style="background: #dc3545; color: white;" @click="confirmDeleteAccount">
                🗑️ Delete Account
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Account Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal-overlay" @click="showDeleteModal = false">
      <div class="modal-container" @click.stop>
        <div class="modal-header">
          <h2>Delete Account</h2>
          <button class="close-btn" @click="showDeleteModal = false">✕</button>
        </div>
        <div class="modal-content">
          <p>Are you sure you want to delete your account? This action cannot be undone.</p>
          <p><strong>All your data, including points and vouchers, will be permanently lost.</strong></p>
          <div class="modal-actions">
            <button class="action-btn secondary-btn" @click="showDeleteModal = false">
              Cancel
            </button>
            <button class="action-btn" style="background: #dc3545; color: white;" @click="deleteAccount">
              Delete Account
            </button>
          </div>
        </div>
      </div>
    </div>
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
        emailNotifications: true,
        smsNotifications: true,
        marketingEmails: false
      },
      passwordData: {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      },
      showCurrentPassword: false,
      showNewPassword: false,
      showConfirmPassword: false,
      isLoading: false,
      isPasswordLoading: false,
      successMessage: '',
      errorMessage: '',
      showDeleteModal: false,
      isDarkMode: false
    }
  },
  mounted() {
    this.loadUserData();
    this.loadDarkModePreference();
  },
  methods: {
    loadUserData() {
      const userSession = localStorage.getItem('ramyeon_user_session');
      if (userSession) {
        const userData = JSON.parse(userSession);
        this.profileData = {
          firstName: userData.firstName || '',
          lastName: userData.lastName || '',
          email: userData.email || '',
          phone: userData.phone || '',
          address: userData.address || '',
          birthdate: userData.birthdate || '',
          emailNotifications: userData.emailNotifications !== false,
          smsNotifications: userData.smsNotifications !== false,
          marketingEmails: userData.marketingEmails || false
        };
      }
    },

    loadDarkModePreference() {
      const darkMode = localStorage.getItem('ramyeon_dark_mode');
      this.isDarkMode = darkMode === 'true';
    },

    async updateProfile() {
      this.isLoading = true;
      this.successMessage = '';
      this.errorMessage = '';

      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1500));

        // Update user session
        const userSession = JSON.parse(localStorage.getItem('ramyeon_user_session') || '{}');
        const updatedUser = {
          ...userSession,
          ...this.profileData,
          updatedAt: new Date().toISOString()
        };

        localStorage.setItem('ramyeon_user_session', JSON.stringify(updatedUser));

        // Update users array if it exists
        const users = JSON.parse(localStorage.getItem('ramyeon_users') || '[]');
        const userIndex = users.findIndex(u => u.email === this.profileData.email);
        if (userIndex !== -1) {
          users[userIndex] = { ...users[userIndex], ...this.profileData };
          localStorage.setItem('ramyeon_users', JSON.stringify(users));
        }

        this.successMessage = 'Profile updated successfully!';
        setTimeout(() => {
          this.successMessage = '';
        }, 3000);

      } catch (error) {
        this.errorMessage = 'Failed to update profile. Please try again.';
        setTimeout(() => {
          this.errorMessage = '';
        }, 3000);
      } finally {
        this.isLoading = false;
      }
    },

    async changePassword() {
      if (this.passwordData.newPassword !== this.passwordData.confirmPassword) {
        this.errorMessage = 'New passwords do not match.';
        setTimeout(() => {
          this.errorMessage = '';
        }, 3000);
        return;
      }

      if (this.passwordData.newPassword.length < 8) {
        this.errorMessage = 'New password must be at least 8 characters long.';
        setTimeout(() => {
          this.errorMessage = '';
        }, 3000);
        return;
      }

      this.isPasswordLoading = true;
      this.successMessage = '';
      this.errorMessage = '';

      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1500));

        // In a real app, you would verify the current password
        // For demo purposes, we'll assume it's correct
        
        // Update password in storage (in real app, this would be hashed)
        const userSession = JSON.parse(localStorage.getItem('ramyeon_user_session') || '{}');
        const users = JSON.parse(localStorage.getItem('ramyeon_users') || '[]');
        
        const userIndex = users.findIndex(u => u.email === userSession.email);
        if (userIndex !== -1) {
          users[userIndex].password = this.passwordData.newPassword;
          localStorage.setItem('ramyeon_users', JSON.stringify(users));
        }

        // Clear password fields
        this.passwordData = {
          currentPassword: '',
          newPassword: '',
          confirmPassword: ''
        };

        this.successMessage = 'Password changed successfully!';
        setTimeout(() => {
          this.successMessage = '';
        }, 3000);

      } catch (error) {
        this.errorMessage = 'Failed to change password. Please try again.';
        setTimeout(() => {
          this.errorMessage = '';
        }, 3000);
      } finally {
        this.isPasswordLoading = false;
      }
    },

    exportData() {
      const userSession = JSON.parse(localStorage.getItem('ramyeon_user_session') || '{}');
      const dataToExport = {
        profile: this.profileData,
        points: userSession.points || 0,
        vouchers: userSession.vouchers || [],
        exportDate: new Date().toISOString()
      };

      const dataStr = JSON.stringify(dataToExport, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);
      
      const link = document.createElement('a');
      link.href = url;
      link.download = `ramyeon-corner-data-${new Date().toISOString().split('T')[0]}.json`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);

      this.successMessage = 'Data exported successfully!';
      setTimeout(() => {
        this.successMessage = '';
      }, 3000);
    },

    confirmDeleteAccount() {
      this.showDeleteModal = true;
    },

    async deleteAccount() {
      try {
        // Clear all user data
        localStorage.removeItem('ramyeon_user_session');
        localStorage.removeItem('ramyeon_remember_user');
        
        // Remove from users array
        const users = JSON.parse(localStorage.getItem('ramyeon_users') || '[]');
        const filteredUsers = users.filter(u => u.email !== this.profileData.email);
        localStorage.setItem('ramyeon_users', JSON.stringify(filteredUsers));

        this.showDeleteModal = false;
        
        // Redirect to home page
        this.$emit('setCurrentPage', 'Home');
        
        // Show success message
        setTimeout(() => {
          alert('Account deleted successfully. We\'re sorry to see you go!');
        }, 500);

      } catch (error) {
        this.errorMessage = 'Failed to delete account. Please try again.';
        this.showDeleteModal = false;
        setTimeout(() => {
          this.errorMessage = '';
        }, 3000);
      }
    }
  }
}
</script>

<style src="./Profile.css" scoped></style>

<style scoped>
/* Additional styles for ProfileSettings */
.password-toggle {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: #666;
  font-size: 1.1rem;
  padding: 5px;
}

.password-toggle:hover {
  color: #ff4757;
}

.loading-spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid #ffffff;
  border-radius: 50%;
  border-top-color: transparent;
  animation: spin 1s ease-in-out infinite;
  margin-right: 8px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 20px;
}

.modal-container {
  background: white;
  border-radius: 15px;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px;
  border-bottom: 2px solid #f0f0f0;
  background: linear-gradient(135deg, #dc3545, #c82333);
  color: white;
  border-radius: 15px 15px 0 0;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
}

.close-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  font-size: 1.2rem;
  width: 35px;
  height: 35px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.modal-content {
  padding: 25px;
}

.modal-content p {
  margin-bottom: 15px;
  line-height: 1.6;
  color: #333;
}

.modal-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  margin-top: 25px;
}

.dark-mode .modal-container {
  background: #2d2d2d;
}

.dark-mode .modal-content p {
  color: #f5f5f5;
}

.dark-mode .password-toggle {
  color: #b8b8b8;
}

.dark-mode .password-toggle:hover {
  color: #ff4757;
}

/* Responsive design */
@media (max-width: 768px) {
  .modal-container {
    margin: 20px;
  }
  
  .modal-actions {
    flex-direction: column;
  }
  
  .modal-actions .action-btn {
    width: 100%;
  }
}
</style>
