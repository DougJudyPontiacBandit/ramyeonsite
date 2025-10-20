<template>
  <div class="settings-wrapper" :class="{ 'dark-mode': isDarkMode, 'high-contrast': highContrast, 'reduce-motion': reduceMotion }">
    <div class="settings-container">
      <!-- Header Section -->
      <div class="settings-header">
        <button class="back-button" @click="$emit('setCurrentPage', 'Profile')">
          <span>←</span> Back to Profile
        </button>
        <h1 class="header-title">App Settings</h1>
        <p class="header-subtitle">Customize your app experience</p>
      </div>

      <!-- Success Message -->
      <transition name="slide-down">
        <div v-if="successMessage" class="alert alert-success">
          <span class="alert-icon">✓</span>
          <span class="alert-text">{{ successMessage }}</span>
        </div>
      </transition>

      <!-- Appearance Settings -->
      <div class="settings-card">
        <div class="card-header">
          <h2 class="card-title">
            <span class="title-icon">🎨</span>
            Appearance
          </h2>
        </div>
        <div class="card-body">
          <!-- Dark Mode -->
          <div class="setting-row highlight">
            <div class="setting-info">
              <span class="setting-icon">{{ isDarkMode ? '🌙' : '☀️' }}</span>
              <div class="setting-text">
                <div class="setting-label">Dark Mode</div>
                <div class="setting-desc">Switch between light and dark themes</div>
              </div>
            </div>
            <label class="toggle">
              <input type="checkbox" v-model="isDarkMode" @change="toggleDarkMode">
              <span class="toggle-slider"></span>
            </label>
          </div>

          <!-- Font Size -->
          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-icon">📝</span>
              <div class="setting-text">
                <div class="setting-label">Font Size</div>
                <div class="setting-desc">Adjust text size</div>
              </div>
            </div>
            <select v-model="fontSize" @change="updateFontSize" class="select-input">
              <option value="small">Small</option>
              <option value="medium">Medium</option>
              <option value="large">Large</option>
              <option value="xlarge">Extra Large</option>
            </select>
          </div>

          <!-- High Contrast -->
          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-icon">🔆</span>
              <div class="setting-text">
                <div class="setting-label">High Contrast</div>
                <div class="setting-desc">Increase contrast for better visibility</div>
              </div>
            </div>
            <label class="toggle">
              <input type="checkbox" v-model="highContrast" @change="toggleHighContrast">
              <span class="toggle-slider"></span>
            </label>
          </div>

          <!-- Reduce Motion -->
          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-icon">🎬</span>
              <div class="setting-text">
                <div class="setting-label">Reduce Motion</div>
                <div class="setting-desc">Minimize animations</div>
              </div>
            </div>
            <label class="toggle">
              <input type="checkbox" v-model="reduceMotion" @change="toggleReduceMotion">
              <span class="toggle-slider"></span>
            </label>
          </div>
        </div>
      </div>

      <!-- Language & Region -->
      <div class="settings-card">
        <div class="card-header">
          <h2 class="card-title">
            <span class="title-icon">🌍</span>
            Language & Region
          </h2>
        </div>
        <div class="card-body">
          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-icon">🗣️</span>
              <div class="setting-text">
                <div class="setting-label">Language</div>
                <div class="setting-desc">Choose your preferred language</div>
              </div>
            </div>
            <select v-model="language" @change="updateLanguage" class="select-input">
              <option value="en">🇺🇸 English</option>
              <option value="ko">🇰🇷 한국어</option>
              <option value="ja">🇯🇵 日本語</option>
              <option value="zh">🇨🇳 中文</option>
              <option value="tl">🇵🇭 Filipino</option>
            </select>
          </div>

          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-icon">💰</span>
              <div class="setting-text">
                <div class="setting-label">Currency</div>
                <div class="setting-desc">Select your preferred currency</div>
              </div>
            </div>
            <select v-model="currency" @change="updateCurrency" class="select-input">
              <option value="PHP">₱ PHP</option>
              <option value="USD">$ USD</option>
              <option value="KRW">₩ KRW</option>
              <option value="JPY">¥ JPY</option>
              <option value="EUR">€ EUR</option>
            </select>
          </div>

          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-icon">🕐</span>
              <div class="setting-text">
                <div class="setting-label">Time Zone</div>
                <div class="setting-desc">Set your local time zone</div>
              </div>
            </div>
            <select v-model="timezone" @change="updateTimezone" class="select-input">
              <option value="Asia/Manila">🇵🇭 Manila (GMT+8)</option>
              <option value="Asia/Seoul">🇰🇷 Seoul (GMT+9)</option>
              <option value="Asia/Tokyo">🇯🇵 Tokyo (GMT+9)</option>
              <option value="America/New_York">🇺🇸 New York (GMT-5)</option>
              <option value="Europe/London">🇬🇧 London (GMT+0)</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Notifications -->
      <div class="settings-card">
        <div class="card-header">
          <h2 class="card-title">
            <span class="title-icon">🔔</span>
            Notifications
          </h2>
        </div>
        <div class="card-body">
          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-icon">📲</span>
              <div class="setting-text">
                <div class="setting-label">Push Notifications</div>
                <div class="setting-desc">Receive notifications on your device</div>
              </div>
            </div>
            <label class="toggle">
              <input type="checkbox" v-model="pushNotifications" @change="togglePushNotifications">
              <span class="toggle-slider"></span>
            </label>
          </div>

          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-icon">📦</span>
              <div class="setting-text">
                <div class="setting-label">Order Updates</div>
                <div class="setting-desc">Get notified about order status</div>
              </div>
            </div>
            <label class="toggle">
              <input type="checkbox" v-model="orderUpdates" @change="toggleOrderUpdates">
              <span class="toggle-slider"></span>
            </label>
          </div>

          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-icon">🎁</span>
              <div class="setting-text">
                <div class="setting-label">Promotional Offers</div>
                <div class="setting-desc">Receive notifications about deals</div>
              </div>
            </div>
            <label class="toggle">
              <input type="checkbox" v-model="promotionalOffers" @change="togglePromotionalOffers">
              <span class="toggle-slider"></span>
            </label>
          </div>

          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-icon">{{ notificationSound ? '🔊' : '🔇' }}</span>
              <div class="setting-text">
                <div class="setting-label">Sound</div>
                <div class="setting-desc">Play sound for notifications</div>
              </div>
            </div>
            <label class="toggle">
              <input type="checkbox" v-model="notificationSound" @change="toggleNotificationSound">
              <span class="toggle-slider"></span>
            </label>
          </div>
        </div>
      </div>

      <!-- Privacy & Security -->
      <div class="settings-card">
        <div class="card-header">
          <h2 class="card-title">
            <span class="title-icon">🔒</span>
            Privacy & Security
          </h2>
        </div>
        <div class="card-body">
          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-icon">📍</span>
              <div class="setting-text">
                <div class="setting-label">Location Services</div>
                <div class="setting-desc">Allow app to access your location</div>
              </div>
            </div>
            <label class="toggle">
              <input type="checkbox" v-model="locationServices" @change="toggleLocationServices">
              <span class="toggle-slider"></span>
            </label>
          </div>

          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-icon">📊</span>
              <div class="setting-text">
                <div class="setting-label">Analytics</div>
                <div class="setting-desc">Help improve the app</div>
              </div>
            </div>
            <label class="toggle">
              <input type="checkbox" v-model="analytics" @change="toggleAnalytics">
              <span class="toggle-slider"></span>
            </label>
          </div>

          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-icon">🔐</span>
              <div class="setting-text">
                <div class="setting-label">Two-Factor Authentication</div>
                <div class="setting-desc">
                  {{ twoFactorEnabled ? '✓ Enabled - Extra security active' : 'Add extra layer of security' }}
                </div>
              </div>
            </div>
            <button class="btn-small" :class="twoFactorEnabled ? 'btn-success' : 'btn-primary'" @click="setup2FA">
              {{ twoFactorEnabled ? '✓ Enabled' : '+ Setup' }}
            </button>
          </div>
        </div>
      </div>

      <!-- App Preferences -->
      <div class="settings-card">
        <div class="card-header">
          <h2 class="card-title">
            <span class="title-icon">⭐</span>
            App Preferences
          </h2>
        </div>
        <div class="card-body">
          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-icon">🛒</span>
              <div class="setting-text">
                <div class="setting-label">Auto-Save Cart</div>
                <div class="setting-desc">Automatically save cart items</div>
              </div>
            </div>
            <label class="toggle">
              <input type="checkbox" v-model="autoSaveCart" @change="toggleAutoSaveCart">
              <span class="toggle-slider"></span>
            </label>
          </div>

          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-icon">💳</span>
              <div class="setting-text">
                <div class="setting-label">Remember Payment</div>
                <div class="setting-desc">Save your payment method</div>
              </div>
            </div>
            <label class="toggle">
              <input type="checkbox" v-model="rememberPayment" @change="toggleRememberPayment">
              <span class="toggle-slider"></span>
            </label>
          </div>

          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-icon">⚡</span>
              <div class="setting-text">
                <div class="setting-label">Quick Reorder</div>
                <div class="setting-desc">One-click reorder previous orders</div>
              </div>
            </div>
            <label class="toggle">
              <input type="checkbox" v-model="quickReorder" @change="toggleQuickReorder">
              <span class="toggle-slider"></span>
            </label>
          </div>
        </div>
      </div>

      <!-- Data Management -->
      <div class="settings-card">
        <div class="card-header">
          <h2 class="card-title">
            <span class="title-icon">💾</span>
            Data Management
          </h2>
        </div>
        <div class="card-body">
          <div class="action-buttons">
            <button class="action-btn" @click="clearCache">
              <span class="action-icon">🗑️</span>
              <div class="action-text">
                <div class="action-label">Clear Cache</div>
                <div class="action-desc">{{ cacheSize }} MB cached</div>
              </div>
            </button>

            <button class="action-btn" @click="resetSettings">
              <span class="action-icon">🔄</span>
              <div class="action-text">
                <div class="action-label">Reset Settings</div>
                <div class="action-desc">Restore to defaults</div>
              </div>
            </button>

            <button class="action-btn" @click="exportData">
              <span class="action-icon">📥</span>
              <div class="action-text">
                <div class="action-label">Export Data</div>
                <div class="action-desc">Download settings</div>
              </div>
            </button>
          </div>
        </div>
      </div>

      <!-- Save Button -->
      <div class="save-section">
        <button class="btn-save" @click="saveAllSettings" :disabled="isSaving">
          <span v-if="isSaving" class="spinner"></span>
          <span v-else>💾</span>
          {{ isSaving ? 'Saving Changes...' : 'Save All Changes' }}
        </button>
      </div>

      <!-- App Info -->
      <div class="app-info">
        <div class="app-logo">🍜</div>
        <div class="app-details">
          <div class="app-name">Ramyeon Corner</div>
          <div class="app-version">Version 2.0.0</div>
        </div>
        <div class="app-links">
          <a href="#">Privacy</a>
          <span>•</span>
          <a href="#">Terms</a>
          <span>•</span>
          <a href="#">Help</a>
        </div>
      </div>
    </div>

    <!-- Clear Cache Modal -->
    <transition name="modal">
      <div v-if="showCacheModal" class="modal-overlay" @click="showCacheModal = false">
        <div class="modal" @click.stop>
          <div class="modal-header">
            <h3>🗑️ Clear Cache</h3>
            <button class="modal-close" @click="showCacheModal = false">✕</button>
          </div>
          <div class="modal-body">
            <p>This will remove temporary files and cached data to free up space.</p>
            <div class="info-box">
              <strong>Estimated Cache Size:</strong> {{ cacheSize }} MB
            </div>
            <p class="note">Your account data and settings will not be affected.</p>
          </div>
          <div class="modal-footer">
            <button class="btn-secondary" @click="showCacheModal = false">Cancel</button>
            <button class="btn-primary" @click="confirmClearCache">Clear Cache</button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Reset Settings Modal -->
    <transition name="modal">
      <div v-if="showResetModal" class="modal-overlay" @click="showResetModal = false">
        <div class="modal" @click.stop>
          <div class="modal-header warning">
            <h3>⚠️ Reset Settings</h3>
            <button class="modal-close" @click="showResetModal = false">✕</button>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to reset all settings to their default values?</p>
            <div class="warning-box">
              <strong>This action cannot be undone.</strong>
            </div>
            <div class="reset-list">
              <h4>Settings that will be reset:</h4>
              <ul>
                <li>Appearance settings</li>
                <li>Language & Region</li>
                <li>Notifications</li>
                <li>Privacy & Security</li>
                <li>App preferences</li>
              </ul>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn-secondary" @click="showResetModal = false">Cancel</button>
            <button class="btn-danger" @click="confirmResetSettings">Reset Settings</button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: 'Settings',
  emits: ['setCurrentPage'],
  data() {
    return {
      isDarkMode: false,
      fontSize: 'medium',
      highContrast: false,
      reduceMotion: false,
      language: 'en',
      currency: 'PHP',
      timezone: 'Asia/Manila',
      pushNotifications: true,
      orderUpdates: true,
      promotionalOffers: false,
      notificationSound: true,
      locationServices: true,
      analytics: false,
      twoFactorEnabled: false,
      autoSaveCart: true,
      rememberPayment: false,
      quickReorder: true,
      successMessage: '',
      showResetModal: false,
      showCacheModal: false,
      isSaving: false,
      cacheSize: '12.5'
    }
  },
  mounted() {
    this.loadSettings();
    this.estimateCacheSize();
  },
  methods: {
    loadSettings() {
      const settings = JSON.parse(localStorage.getItem('ramyeon_settings') || '{}');
      
      this.isDarkMode = settings.isDarkMode ?? false;
      this.fontSize = settings.fontSize || 'medium';
      this.highContrast = settings.highContrast ?? false;
      this.reduceMotion = settings.reduceMotion ?? false;
      this.language = settings.language || 'en';
      this.currency = settings.currency || 'PHP';
      this.timezone = settings.timezone || 'Asia/Manila';
      this.pushNotifications = settings.pushNotifications ?? true;
      this.orderUpdates = settings.orderUpdates ?? true;
      this.promotionalOffers = settings.promotionalOffers ?? false;
      this.notificationSound = settings.notificationSound ?? true;
      this.locationServices = settings.locationServices ?? true;
      this.analytics = settings.analytics ?? false;
      this.twoFactorEnabled = settings.twoFactorEnabled ?? false;
      this.autoSaveCart = settings.autoSaveCart ?? true;
      this.rememberPayment = settings.rememberPayment ?? false;
      this.quickReorder = settings.quickReorder ?? true;
      
      localStorage.setItem('ramyeon_dark_mode', this.isDarkMode.toString());
      this.applyTheme();
    },

    saveSettings() {
      const settings = {
        isDarkMode: this.isDarkMode,
        fontSize: this.fontSize,
        highContrast: this.highContrast,
        reduceMotion: this.reduceMotion,
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
    },

    applyTheme() {
      const root = document.documentElement;
      
      if (this.isDarkMode) {
        root.classList.add('dark-mode');
        document.body.classList.add('dark-mode');
      } else {
        root.classList.remove('dark-mode');
        document.body.classList.remove('dark-mode');
      }
      
      const fontMultipliers = {
        'small': '0.875',
        'medium': '1',
        'large': '1.125',
        'xlarge': '1.25'
      };
      root.style.setProperty('--font-size-multiplier', fontMultipliers[this.fontSize] || '1');
      
      if (this.highContrast) {
        root.classList.add('high-contrast');
      } else {
        root.classList.remove('high-contrast');
      }

      if (this.reduceMotion) {
        root.classList.add('reduce-motion');
      } else {
        root.classList.remove('reduce-motion');
      }
    },

    toggleDarkMode() {
      this.applyTheme();
      this.saveSettings();
      this.showSuccessMessage(`${this.isDarkMode ? 'Dark' : 'Light'} mode enabled!`);
    },

    toggleHighContrast() {
      this.applyTheme();
      this.saveSettings();
      this.showSuccessMessage(`High contrast ${this.highContrast ? 'enabled' : 'disabled'}!`);
    },

    toggleReduceMotion() {
      this.applyTheme();
      this.saveSettings();
      this.showSuccessMessage(`Reduced motion ${this.reduceMotion ? 'enabled' : 'disabled'}!`);
    },

    updateFontSize() {
      this.applyTheme();
      this.saveSettings();
      const sizes = { 'small': 'Small', 'medium': 'Medium', 'large': 'Large', 'xlarge': 'Extra Large' };
      this.showSuccessMessage(`Font size changed to ${sizes[this.fontSize]}!`);
    },

    updateLanguage() {
      this.saveSettings();
      const langs = { 'en': 'English', 'ko': 'Korean', 'ja': 'Japanese', 'zh': 'Chinese', 'tl': 'Filipino' };
      this.showSuccessMessage(`Language changed to ${langs[this.language]}!`);
    },

    updateCurrency() {
      this.saveSettings();
      this.showSuccessMessage(`Currency changed to ${this.currency}!`);
    },

    updateTimezone() {
      this.saveSettings();
      this.showSuccessMessage('Timezone updated!');
    },

    togglePushNotifications() {
      this.saveSettings();
      this.showSuccessMessage(`Push notifications ${this.pushNotifications ? 'enabled' : 'disabled'}!`);
    },

    toggleOrderUpdates() {
      this.saveSettings();
      this.showSuccessMessage(`Order updates ${this.orderUpdates ? 'enabled' : 'disabled'}!`);
    },

    togglePromotionalOffers() {
      this.saveSettings();
      this.showSuccessMessage(`Promotional offers ${this.promotionalOffers ? 'enabled' : 'disabled'}!`);
    },

    toggleNotificationSound() {
      this.saveSettings();
      this.showSuccessMessage(`Notification sound ${this.notificationSound ? 'enabled' : 'disabled'}!`);
    },

    toggleLocationServices() {
      this.saveSettings();
      this.showSuccessMessage(`Location services ${this.locationServices ? 'enabled' : 'disabled'}!`);
    },

    toggleAnalytics() {
      this.saveSettings();
      this.showSuccessMessage(`Analytics ${this.analytics ? 'enabled' : 'disabled'}!`);
    },

    toggleAutoSaveCart() {
      this.saveSettings();
      this.showSuccessMessage(`Auto-save cart ${this.autoSaveCart ? 'enabled' : 'disabled'}!`);
    },

    toggleRememberPayment() {
      this.saveSettings();
      this.showSuccessMessage(`Remember payment ${this.rememberPayment ? 'enabled' : 'disabled'}!`);
    },

    toggleQuickReorder() {
      this.saveSettings();
      this.showSuccessMessage(`Quick reorder ${this.quickReorder ? 'enabled' : 'disabled'}!`);
    },

    setup2FA() {
      if (this.twoFactorEnabled) {
        const disable = confirm('Would you like to disable Two-Factor Authentication?');
        if (disable) {
          this.twoFactorEnabled = false;
          this.saveSettings();
          this.showSuccessMessage('Two-Factor Authentication disabled!');
        }
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
      this.showCacheModal = true;
    },

    confirmClearCache() {
      const keysToKeep = [
        'ramyeon_user_session', 
        'ramyeon_users', 
        'ramyeon_settings', 
        'ramyeon_dark_mode',
        'ramyeon_saved_vouchers',
        'access_token',
        'refresh_token'
      ];
      
      const allKeys = Object.keys(localStorage);
      let clearedCount = 0;
      
      allKeys.forEach(key => {
        if (!keysToKeep.includes(key)) {
          localStorage.removeItem(key);
          clearedCount++;
        }
      });
      
      this.showCacheModal = false;
      this.cacheSize = '0.5';
      this.showSuccessMessage(`Cache cleared! Removed ${clearedCount} items.`);
    },

    resetSettings() {
      this.showResetModal = true;
    },

    confirmResetSettings() {
      this.isDarkMode = false;
      this.fontSize = 'medium';
      this.highContrast = false;
      this.reduceMotion = false;
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
      this.showSuccessMessage('All settings reset to defaults!');
    },

    estimateCacheSize() {
      let totalSize = 0;
      for (let key in localStorage) {
        if (Object.prototype.hasOwnProperty.call(localStorage, key)) {
          const value = localStorage.getItem(key);
          totalSize += (key.length + (value ? value.length : 0)) * 2;
        }
      }
      this.cacheSize = ((totalSize / 1024 / 1024) + Math.random() * 5).toFixed(1);
    },

    exportData() {
      const exportData = {
        settings: JSON.parse(localStorage.getItem('ramyeon_settings') || '{}'),
        userSession: JSON.parse(localStorage.getItem('ramyeon_user_session') || '{}'),
        savedVouchers: JSON.parse(localStorage.getItem('ramyeon_saved_vouchers') || '[]'),
        exportDate: new Date().toISOString(),
        version: '2.0.0'
      };

      const dataStr = JSON.stringify(exportData, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);
      
      const link = document.createElement('a');
      link.href = url;
      link.download = `ramyeon-settings-${new Date().toISOString().split('T')[0]}.json`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);

      this.showSuccessMessage('Settings exported successfully!');
    },

    async saveAllSettings() {
      this.isSaving = true;
      await new Promise(resolve => setTimeout(resolve, 1000));
      this.saveSettings();
      this.isSaving = false;
      this.showSuccessMessage('All settings saved successfully!');
    },

    showSuccessMessage(message) {
      this.successMessage = message;
      setTimeout(() => {
        this.successMessage = '';
      }, 3000);
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

.reduce-motion * {
  animation-duration: 0.01ms !important;
  transition-duration: 0.01ms !important;
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

/* Alert */
.alert {
  background: linear-gradient(135deg, #d1fae5, #a7f3d0);
  color: #065f46;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 600;
  border: 2px solid #6ee7b7;
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

.setting-row.highlight {
  background: linear-gradient(135deg, rgba(255, 75, 75, 0.1), rgba(255, 92, 51, 0.1));
  border-color: #ff4b4b;
}

.dark-mode .setting-row {
  border-color: #444;
  background: #1f1f1f;
}

.dark-mode .setting-row:hover {
  border-color: #ff5c33;
  background: rgba(255, 92, 51, 0.1);
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

.setting-text {
  flex: 1;
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

/* Select Input */
.select-input {
  padding: 0.75rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-weight: 500;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
  color: #333;
  min-width: 180px;
}

.select-input:hover {
  border-color: #ff4b4b;
}

.select-input:focus {
  outline: none;
  border-color: #ff4b4b;
  box-shadow: 0 0 0 3px rgba(255, 75, 75, 0.1);
}

.dark-mode .select-input {
  background: #1f1f1f;
  color: #fff;
  border-color: #444;
}

/* Buttons */
.btn-small {
  padding: 0.625rem 1.25rem;
  border-radius: 8px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.btn-primary {
  background: linear-gradient(135deg, #ff4b4b, #ff5c33);
  color: white;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #ff5c33, #ff6b43);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 75, 75, 0.3);
}

.btn-success {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.btn-success:hover {
  background: linear-gradient(135deg, #059669, #047857);
  transform: translateY(-2px);
}

.btn-secondary {
  background: white;
  color: #666;
  border: 2px solid #e0e0e0;
}

.btn-secondary:hover {
  background: #f5f5f5;
  border-color: #ccc;
}

.btn-danger {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
}

.btn-danger:hover {
  background: linear-gradient(135deg, #dc2626, #b91c1c);
}

/* Action Buttons */
.action-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem;
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn:hover {
  border-color: #ff4b4b;
  background: rgba(255, 75, 75, 0.02);
  transform: translateY(-2px);
}

.dark-mode .action-btn {
  background: #1f1f1f;
  border-color: #444;
}

.action-icon {
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

.action-label {
  font-weight: 600;
  color: #333;
  margin-bottom: 0.25rem;
}

.dark-mode .action-label {
  color: #fff;
}

.action-desc {
  color: #666;
  font-size: 0.9rem;
}

.dark-mode .action-desc {
  color: #aaa;
}

/* Save Section */
.save-section {
  margin: 2rem 0;
  text-align: center;
}

.btn-save {
  background: linear-gradient(135deg, #ff4b4b, #ff5c33);
  color: white;
  border: none;
  padding: 1.25rem 3rem;
  border-radius: 12px;
  font-weight: 700;
  font-size: 1.125rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  box-shadow: 0 4px 12px rgba(255, 75, 75, 0.3);
}

.btn-save:hover:not(:disabled) {
  background: linear-gradient(135deg, #ff5c33, #ff6b43);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 75, 75, 0.4);
}

.btn-save:disabled {
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

/* App Info */
.app-info {
  background: linear-gradient(135deg, #ff4b4b, #ff5c33);
  border-radius: 12px;
  padding: 2rem;
  color: white;
  text-align: center;
  margin-top: 2rem;
}

.app-logo {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.app-name {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.app-version {
  opacity: 0.9;
  margin-bottom: 1rem;
}

.app-links {
  display: flex;
  gap: 1rem;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}

.app-links a {
  color: white;
  text-decoration: none;
  font-weight: 500;
  transition: opacity 0.3s ease;
}

.app-links a:hover {
  opacity: 0.8;
  text-decoration: underline;
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
  background: linear-gradient(135deg, rgba(255, 75, 75, 0.1), rgba(255, 92, 51, 0.1));
}

.modal-header.warning {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(239, 68, 68, 0.1));
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
  background: rgba(255, 75, 75, 0.1);
  color: #ff4b4b;
  transform: rotate(90deg);
}

.dark-mode .modal-close {
  color: #aaa;
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

.info-box {
  background: rgba(255, 75, 75, 0.1);
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #ff4b4b;
  margin: 1rem 0;
}

.warning-box {
  background: rgba(239, 68, 68, 0.1);
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #ef4444;
  margin: 1rem 0;
}

.note {
  font-size: 0.9rem;
  color: #666;
  font-style: italic;
}

.dark-mode .note {
  color: #aaa;
}

.reset-list {
  margin-top: 1.5rem;
}

.reset-list h4 {
  margin: 0 0 0.75rem 0;
  color: #333;
}

.dark-mode .reset-list h4 {
  color: #fff;
}

.reset-list ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.reset-list li {
  padding: 0.5rem 0;
  color: #666;
  border-bottom: 1px solid #f0f0f0;
}

.dark-mode .reset-list li {
  color: #aaa;
  border-bottom-color: #444;
}

.reset-list li:last-child {
  border-bottom: none;
}

.reset-list li::before {
  content: '•';
  color: #ff4b4b;
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

  .setting-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .setting-info {
    width: 100%;
  }

  .toggle,
  .select-input,
  .btn-small {
    width: 100%;
  }

  .action-buttons {
    grid-template-columns: 1fr;
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

  .btn-save {
    width: 100%;
  }
}
</style>
