<template>
  <div class="profile-container" :class="{ 'dark-mode': isDarkMode }">
    <div class="profile-content">
      <!-- Header -->
      <div class="profile-header">
        <div class="profile-avatar">
          🔧
        </div>
        <h1 class="profile-name">Settings</h1>
        <p class="profile-email">Customize your app experience</p>
      </div>

      <!-- Settings Content -->
      <div class="profile-main">
        <div v-if="successMessage" class="message success">
          {{ successMessage }}
        </div>

        <!-- Appearance Settings -->
        <div class="settings-section">
          <div class="settings-group">
            <h3 class="settings-group-title">Appearance</h3>
            
            <div class="setting-item">
              <div class="setting-info">
                <div class="setting-label">Dark Mode</div>
                <div class="setting-description">Switch between light and dark themes</div>
              </div>
              <div class="setting-control">
                <div 
                  class="toggle-switch" 
                  :class="{ active: isDarkMode }"
                  @click="toggleDarkMode"
                ></div>
              </div>
            </div>
            
            <div class="setting-item">
              <div class="setting-info">
                <div class="setting-label">Font Size</div>
                <div class="setting-description">Adjust text size for better readability</div>
              </div>
              <div class="setting-control">
                <select v-model="fontSize" @change="updateFontSize" class="form-select">
                  <option value="small">Small</option>
                  <option value="medium">Medium</option>
                  <option value="large">Large</option>
                </select>
              </div>
            </div>
            
            <div class="setting-item">
              <div class="setting-info">
                <div class="setting-label">High Contrast</div>
                <div class="setting-description">Increase contrast for better visibility</div>
              </div>
              <div class="setting-control">
                <div 
                  class="toggle-switch" 
                  :class="{ active: highContrast }"
                  @click="toggleHighContrast"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Language & Region -->
        <div class="settings-section">
          <div class="settings-group">
            <h3 class="settings-group-title">Language & Region</h3>
            
            <div class="setting-item">
              <div class="setting-info">
                <div class="setting-label">Language</div>
                <div class="setting-description">Choose your preferred language</div>
              </div>
              <div class="setting-control">
                <select v-model="language" @change="updateLanguage" class="form-select">
                  <option value="en">English</option>
                  <option value="ko">한국어 (Korean)</option>
                  <option value="ja">日本語 (Japanese)</option>
                  <option value="zh">中文 (Chinese)</option>
                  <option value="tl">Filipino</option>
                </select>
              </div>
            </div>
            
            <div class="setting-item">
              <div class="setting-info">
                <div class="setting-label">Currency</div>
                <div class="setting-description">Select your preferred currency</div>
              </div>
              <div class="setting-control">
                <select v-model="currency" @change="updateCurrency" class="form-select">
                  <option value="PHP">₱ Philippine Peso (PHP)</option>
                  <option value="USD">$ US Dollar (USD)</option>
                  <option value="KRW">₩ Korean Won (KRW)</option>
                  <option value="JPY">¥ Japanese Yen (JPY)</option>
                  <option value="EUR">€ Euro (EUR)</option>
                </select>
              </div>
            </div>
            
            <div class="setting-item">
              <div class="setting-info">
                <div class="setting-label">Time Zone</div>
                <div class="setting-description">Set your local time zone</div>
              </div>
              <div class="setting-control">
                <select v-model="timezone" @change="updateTimezone" class="form-select">
                  <option value="Asia/Manila">Philippines (GMT+8)</option>
                  <option value="Asia/Seoul">Seoul (GMT+9)</option>
                  <option value="Asia/Tokyo">Tokyo (GMT+9)</option>
                  <option value="America/New_York">New York (GMT-5)</option>
                  <option value="Europe/London">London (GMT+0)</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <!-- Notifications -->
        <div class="settings-section">
          <div class="settings-group">
            <h3 class="settings-group-title">Notifications</h3>
            
            <div class="setting-item">
              <div class="setting-info">
                <div class="setting-label">Push Notifications</div>
                <div class="setting-description">Receive notifications on your device</div>
              </div>
              <div class="setting-control">
                <div 
                  class="toggle-switch" 
                  :class="{ active: pushNotifications }"
                  @click="togglePushNotifications"
                ></div>
              </div>
            </div>
            
            <div class="setting-item">
              <div class="setting-info">
                <div class="setting-label">Order Updates</div>
                <div class="setting-description">Get notified about order status changes</div>
              </div>
              <div class="setting-control">
                <div 
                  class="toggle-switch" 
                  :class="{ active: orderUpdates }"
                  @click="toggleOrderUpdates"
                ></div>
              </div>
            </div>
            
            <div class="setting-item">
              <div class="setting-info">
                <div class="setting-label">Promotional Offers</div>
                <div class="setting-description">Receive notifications about deals and promotions</div>
              </div>
              <div class="setting-control">
                <div 
                  class="toggle-switch" 
                  :class="{ active: promotionalOffers }"
                  @click="togglePromotionalOffers"
                ></div>
              </div>
            </div>
            
            <div class="setting-item">
              <div class="setting-info">
                <div class="setting-label">Sound</div>
                <div class="setting-description">Play sound for notifications</div>
              </div>
              <div class="setting-control">
                <div 
                  class="toggle-switch" 
                  :class="{ active: notificationSound }"
                  @click="toggleNotificationSound"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Privacy & Security -->
        <div class="settings-section">
          <div class="settings-group">
            <h3 class="settings-group-title">Privacy & Security</h3>
            
            <div class="setting-item">
              <div class="setting-info">
                <div class="setting-label">Location Services</div>
                <div class="setting-description">Allow app to access your location for delivery</div>
              </div>
              <div class="setting-control">
                <div 
                  class="toggle-switch" 
                  :class="{ active: locationServices }"
                  @click="toggleLocationServices"
                ></div>
              </div>
            </div>
            
            <div class="setting-item">
              <div class="setting-info">
                <div class="setting-label">Analytics</div>
                <div class="setting-description">Help improve the app by sharing usage data</div>
              </div>
              <div class="setting-control">
                <div 
                  class="toggle-switch" 
                  :class="{ active: analytics }"
                  @click="toggleAnalytics"
                ></div>
              </div>
            </div>
            
            <div class="setting-item">
              <div class="setting-info">
                <div class="setting-label">Two-Factor Authentication</div>
                <div class="setting-description">Add an extra layer of security to your account</div>
              </div>
              <div class="setting-control">
                <button class="action-btn secondary-btn" @click="setup2FA">
                  {{ twoFactorEnabled ? 'Manage' : 'Setup' }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- App Preferences -->
        <div class="settings-section">
          <div class="settings-group">
            <h3 class="settings-group-title">App Preferences</h3>
            
            <div class="setting-item">
              <div class="setting-info">
                <div class="setting-label">Auto-Save Cart</div>
                <div class="setting-description">Automatically save items in your cart</div>
              </div>
              <div class="setting-control">
                <div 
                  class="toggle-switch" 
                  :class="{ active: autoSaveCart }"
                  @click="toggleAutoSaveCart"
                ></div>
              </div>
            </div>
            
            <div class="setting-item">
              <div class="setting-info">
                <div class="setting-label">Remember Payment Method</div>
                <div class="setting-description">Save your preferred payment method</div>
              </div>
              <div class="setting-control">
                <div 
                  class="toggle-switch" 
                  :class="{ active: rememberPayment }"
                  @click="toggleRememberPayment"
                ></div>
              </div>
            </div>
            
            <div class="setting-item">
              <div class="setting-info">
                <div class="setting-label">Quick Reorder</div>
                <div class="setting-description">Enable one-click reordering of previous orders</div>
              </div>
              <div class="setting-control">
                <div 
                  class="toggle-switch" 
                  :class="{ active: quickReorder }"
                  @click="toggleQuickReorder"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Data Management -->
        <div class="settings-section">
          <div class="settings-group">
            <h3 class="settings-group-title">Data Management</h3>
            
            <div class="data-management-grid">
              <div class="data-card">
                <div class="data-card-icon">🗑️</div>
                <div class="data-card-content">
                  <h4 class="data-card-title">Clear Cache</h4>
                  <p class="data-card-description">Remove temporary files and cached data</p>
                  <button class="data-card-btn" @click="clearCache">Clear Cache</button>
                </div>
              </div>
              
              <div class="data-card">
                <div class="data-card-icon">🔄</div>
                <div class="data-card-content">
                  <h4 class="data-card-title">Reset Settings</h4>
                  <p class="data-card-description">Restore all settings to default values</p>
                  <button class="data-card-btn danger" @click="resetSettings">Reset Settings</button>
                </div>
              </div>
              
              <div class="data-card">
                <div class="data-card-icon">📊</div>
                <div class="data-card-content">
                  <h4 class="data-card-title">Export Data</h4>
                  <p class="data-card-description">Download your settings and preferences</p>
                  <button class="data-card-btn" @click="exportData">Export Data</button>
                </div>
              </div>
            </div>
            
            <div class="settings-navigation">
              <button class="navigation-btn back-btn" @click="$emit('setCurrentPage', 'Profile')">
                <span class="btn-icon">←</span>
                <span class="btn-text">Back to Profile</span>
              </button>
              <button class="navigation-btn save-btn" @click="saveAllSettings">
                <span class="btn-icon">💾</span>
                <span class="btn-text">Save All Changes</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Reset Confirmation Modal -->
    <div v-if="showResetModal" class="modal-overlay" @click="showResetModal = false">
      <div class="modal-container" @click.stop>
        <div class="modal-header">
          <h2>Reset Settings</h2>
          <button class="close-btn" @click="showResetModal = false">✕</button>
        </div>
        <div class="modal-content">
          <p>Are you sure you want to reset all settings to their default values?</p>
          <p><strong>This action cannot be undone.</strong></p>
          <div class="modal-actions">
            <button class="action-btn secondary-btn" @click="showResetModal = false">
              Cancel
            </button>
            <button class="action-btn primary-btn" @click="confirmResetSettings">
              Reset Settings
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Settings',
  emits: ['setCurrentPage'],
  data() {
    return {
      // Appearance
      isDarkMode: false,
      fontSize: 'medium',
      highContrast: false,
      
      // Language & Region
      language: 'en',
      currency: 'PHP',
      timezone: 'Asia/Manila',
      
      // Notifications
      pushNotifications: true,
      orderUpdates: true,
      promotionalOffers: false,
      notificationSound: true,
      
      // Privacy & Security
      locationServices: true,
      analytics: false,
      twoFactorEnabled: false,
      
      // App Preferences
      autoSaveCart: true,
      rememberPayment: false,
      quickReorder: true,
      
      // UI State
      successMessage: '',
      showResetModal: false
    }
  },
  mounted() {
    this.loadSettings();
  },
  methods: {
    loadSettings() {
      // Load settings from localStorage
      const settings = JSON.parse(localStorage.getItem('ramyeon_settings') || '{}');
      
      // Apply loaded settings
      this.isDarkMode = settings.isDarkMode || false;
      this.fontSize = settings.fontSize || 'medium';
      this.highContrast = settings.highContrast || false;
      this.language = settings.language || 'en';
      this.currency = settings.currency || 'PHP';
      this.timezone = settings.timezone || 'Asia/Manila';
      this.pushNotifications = settings.pushNotifications !== false;
      this.orderUpdates = settings.orderUpdates !== false;
      this.promotionalOffers = settings.promotionalOffers || false;
      this.notificationSound = settings.notificationSound !== false;
      this.locationServices = settings.locationServices !== false;
      this.analytics = settings.analytics || false;
      this.twoFactorEnabled = settings.twoFactorEnabled || false;
      this.autoSaveCart = settings.autoSaveCart !== false;
      this.rememberPayment = settings.rememberPayment || false;
      this.quickReorder = settings.quickReorder !== false;
      
      // Apply dark mode to localStorage for other components
      localStorage.setItem('ramyeon_dark_mode', this.isDarkMode.toString());
      
      // Apply theme to document
      this.applyTheme();
    },

    saveSettings() {
      const settings = {
        isDarkMode: this.isDarkMode,
        fontSize: this.fontSize,
        highContrast: this.highContrast,
        language: this.language,
        currency: this.currency,
        timezone: this.timezone,
        pushNotifications: this.pushNotifications,
        orderUpdates: this.orderUpdates,
        promotionalOffers: this.promotionalOffers,
        notificationSound: this.notificationSound,
        locationServices: this.locationServices,
        analytics: this.analytics,
        twoFactorEnabled: this.twoFactorEnabled,
        autoSaveCart: this.autoSaveCart,
        rememberPayment: this.rememberPayment,
        quickReorder: this.quickReorder,
        updatedAt: new Date().toISOString()
      };
      
      localStorage.setItem('ramyeon_settings', JSON.stringify(settings));
      localStorage.setItem('ramyeon_dark_mode', this.isDarkMode.toString());
      
      this.showSuccessMessage('Settings saved successfully!');
    },

    applyTheme() {
      const root = document.documentElement;
      
      if (this.isDarkMode) {
        root.classList.add('dark-mode');
      } else {
        root.classList.remove('dark-mode');
      }
      
      // Apply font size
      root.style.setProperty('--font-size-multiplier', 
        this.fontSize === 'small' ? '0.9' : 
        this.fontSize === 'large' ? '1.1' : '1'
      );
      
      // Apply high contrast
      if (this.highContrast) {
        root.classList.add('high-contrast');
      } else {
        root.classList.remove('high-contrast');
      }
    },

    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      this.applyTheme();
      this.saveSettings();
    },

    toggleHighContrast() {
      this.highContrast = !this.highContrast;
      this.applyTheme();
      this.saveSettings();
    },

    updateFontSize() {
      this.applyTheme();
      this.saveSettings();
    },

    updateLanguage() {
      // In a real app, this would trigger language change
      this.saveSettings();
      this.showSuccessMessage(`Language changed to ${this.getLanguageName(this.language)}`);
    },

    updateCurrency() {
      this.saveSettings();
      this.showSuccessMessage(`Currency changed to ${this.currency}`);
    },

    updateTimezone() {
      this.saveSettings();
      this.showSuccessMessage('Timezone updated successfully!');
    },

    getLanguageName(code) {
      const languages = {
        'en': 'English',
        'ko': 'Korean',
        'ja': 'Japanese',
        'zh': 'Chinese',
        'tl': 'Filipino'
      };
      return languages[code] || code;
    },

    // Toggle methods for all switches
    togglePushNotifications() {
      this.pushNotifications = !this.pushNotifications;
      this.saveSettings();
    },

    toggleOrderUpdates() {
      this.orderUpdates = !this.orderUpdates;
      this.saveSettings();
    },

    togglePromotionalOffers() {
      this.promotionalOffers = !this.promotionalOffers;
      this.saveSettings();
    },

    toggleNotificationSound() {
      this.notificationSound = !this.notificationSound;
      this.saveSettings();
    },

    toggleLocationServices() {
      this.locationServices = !this.locationServices;
      this.saveSettings();
    },

    toggleAnalytics() {
      this.analytics = !this.analytics;
      this.saveSettings();
    },

    toggleAutoSaveCart() {
      this.autoSaveCart = !this.autoSaveCart;
      this.saveSettings();
    },

    toggleRememberPayment() {
      this.rememberPayment = !this.rememberPayment;
      this.saveSettings();
    },

    toggleQuickReorder() {
      this.quickReorder = !this.quickReorder;
      this.saveSettings();
    },

    setup2FA() {
      // In a real app, this would open 2FA setup flow
      if (this.twoFactorEnabled) {
        alert('Two-Factor Authentication is currently enabled. You can manage your settings here.');
      } else {
        const enable = confirm('Would you like to enable Two-Factor Authentication for added security?');
        if (enable) {
          this.twoFactorEnabled = true;
          this.saveSettings();
          this.showSuccessMessage('Two-Factor Authentication enabled!');
        }
      }
    },

    clearCache() {
      // Clear app cache (excluding user data and settings)
      const keysToKeep = ['ramyeon_user_session', 'ramyeon_users', 'ramyeon_settings', 'ramyeon_dark_mode'];
      const allKeys = Object.keys(localStorage);
      
      allKeys.forEach(key => {
        if (!keysToKeep.includes(key)) {
          localStorage.removeItem(key);
        }
      });
      
      this.showSuccessMessage('Cache cleared successfully!');
    },

    resetSettings() {
      this.showResetModal = true;
    },

    confirmResetSettings() {
      // Reset all settings to defaults
      this.isDarkMode = false;
      this.fontSize = 'medium';
      this.highContrast = false;
      this.language = 'en';
      this.currency = 'PHP';
      this.timezone = 'Asia/Manila';
      this.pushNotifications = true;
      this.orderUpdates = true;
      this.promotionalOffers = false;
      this.notificationSound = true;
      this.locationServices = true;
      this.analytics = false;
      this.twoFactorEnabled = false;
      this.autoSaveCart = true;
      this.rememberPayment = false;
      this.quickReorder = true;
      
      this.applyTheme();
      this.saveSettings();
      this.showResetModal = false;
      this.showSuccessMessage('Settings reset to defaults!');
    },

    showSuccessMessage(message) {
      this.successMessage = message;
      setTimeout(() => {
        this.successMessage = '';
      }, 3000);
    },

    exportData() {
      // Export user settings and preferences
      const exportData = {
        settings: JSON.parse(localStorage.getItem('ramyeon_settings') || '{}'),
        userSession: JSON.parse(localStorage.getItem('ramyeon_user_session') || '{}'),
        savedVouchers: JSON.parse(localStorage.getItem('ramyeon_saved_vouchers') || '[]'),
        exportDate: new Date().toISOString(),
        version: '1.0.0'
      };

      // Create and download file
      const dataStr = JSON.stringify(exportData, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);
      
      const link = document.createElement('a');
      link.href = url;
      link.download = `ramyeon-data-export-${new Date().toISOString().split('T')[0]}.json`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);

      this.showSuccessMessage('Data exported successfully!');
    },

    saveAllSettings() {
      // Save all current settings
      this.saveSettings();
      this.showSuccessMessage('All settings saved successfully!');
    }
  }
}
</script>

<style src="./Profile.css" scoped></style>

<style scoped>
/* Additional styles for Settings component */
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
  background: linear-gradient(135deg, #ff4757, #ff3742);
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

/* High contrast mode */
:global(.high-contrast) {
  --primary-color: #000000;
  --secondary-color: #ffffff;
  --accent-color: #ff0000;
}

:global(.high-contrast) .profile-content {
  border: 3px solid #000000;
}

:global(.high-contrast) .toggle-switch {
  border: 2px solid #000000;
}

:global(.high-contrast) .form-select,
:global(.high-contrast) .form-input {
  border: 2px solid #000000;
}

/* Data Management Grid */
.data-management-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.data-card {
  background: white;
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
  border: 2px solid #f0f0f0;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.data-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(135deg, #ff4757, #ff3742);
}

.data-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
  border-color: #ff4757;
}

.data-card-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ff4757, #ff3742);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  margin-bottom: 20px;
  box-shadow: 0 8px 20px rgba(255, 71, 87, 0.3);
}

.data-card-content {
  text-align: center;
}

.data-card-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #333;
  margin: 0 0 10px 0;
}

.data-card-description {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.5;
  margin: 0 0 20px 0;
}

.data-card-btn {
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  color: #495057;
  border: 2px solid #dee2e6;
  padding: 12px 25px;
  border-radius: 25px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  width: 100%;
}

.data-card-btn:hover {
  background: linear-gradient(135deg, #e9ecef, #dee2e6);
  border-color: #adb5bd;
  transform: translateY(-2px);
}

.data-card-btn.danger {
  background: linear-gradient(135deg, #dc3545, #c82333);
  color: white;
  border-color: #dc3545;
}

.data-card-btn.danger:hover {
  background: linear-gradient(135deg, #c82333, #a71e2a);
  border-color: #a71e2a;
}

/* Settings Navigation */
.settings-navigation {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-top: 30px;
  padding-top: 30px;
  border-top: 2px solid #f0f0f0;
}

.navigation-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px 30px;
  border: none;
  border-radius: 15px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  min-width: 180px;
  justify-content: center;
}

.navigation-btn .btn-icon {
  font-size: 1.2rem;
}

.back-btn {
  background: #f8f9fa;
  color: #6c757d;
  border: 2px solid #e9ecef;
}

.back-btn:hover {
  background: #e9ecef;
  border-color: #dee2e6;
  transform: translateY(-2px);
}

.save-btn {
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
  border: 2px solid #28a745;
}

.save-btn:hover {
  background: linear-gradient(135deg, #20c997, #17a2b8);
  border-color: #20c997;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(40, 167, 69, 0.3);
}

/* Dark Mode Styles for New Components */
.dark-mode .data-card {
  background: #3a3a3a;
  border-color: #4a4a4a;
}

.dark-mode .data-card-title {
  color: #f5f5f5;
}

.dark-mode .data-card-description {
  color: #b8b8b8;
}

.dark-mode .data-card-btn {
  background: #4a4a4a;
  color: #f5f5f5;
  border-color: #5a5a5a;
}

.dark-mode .data-card-btn:hover {
  background: #5a5a5a;
  border-color: #6a6a6a;
}

.dark-mode .settings-navigation {
  border-top-color: #4a4a4a;
}

.dark-mode .back-btn {
  background: #4a4a4a;
  color: #b8b8b8;
  border-color: #5a5a5a;
}

.dark-mode .back-btn:hover {
  background: #5a5a5a;
  border-color: #6a6a6a;
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
  
  .data-management-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .settings-navigation {
    flex-direction: column;
    gap: 15px;
  }
  
  .navigation-btn {
    min-width: auto;
    width: 100%;
  }
}

@media (max-width: 480px) {
  .data-card {
    padding: 20px;
  }
  
  .data-card-icon {
    width: 50px;
    height: 50px;
    font-size: 1.5rem;
  }
  
  .data-card-title {
    font-size: 1.1rem;
  }
  
  .data-card-description {
    font-size: 0.9rem;
  }
}
</style>
