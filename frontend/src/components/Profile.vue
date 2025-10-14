<template>
  <div class="profile-container" :class="{ 'dark-mode': isDarkMode }">
    <div class="profile-content">
      <!-- Profile Header -->
      <div class="profile-header">
        <div class="profile-avatar" @mouseenter="avatarHover = true" @mouseleave="avatarHover = false">
          {{ avatarHover ? '✨' : '👤' }}
        </div>
        <h1 class="profile-name">{{ user.firstName }} {{ user.lastName }}</h1>
        <p class="profile-email">{{ user.email }}</p>
      </div>

      <!-- Profile Main Content -->
      <div class="profile-main">
        <!-- Points Section -->
        <div class="points-section">
          <div class="points-badge">
            <div class="points-circle">
              <div class="points-label">Total Points</div>
              <div class="points-value" :key="user.points">{{ user.points }}</div>
              <div class="points-unit">pts</div>
            </div>
          </div>
          <button class="promotions-btn" @click="$emit('setCurrentPage', 'Promotions')">
            <span>🎁</span> See Promotions
          </button>
        </div>

        <!-- Vouchers Section -->
        <div class="vouchers-section">
          <div class="section-header">
            <h2 class="section-title">{{ user.vouchers.length > 0 ? 'My Vouchers' : 'No Vouchers Yet' }}</h2>
            <a v-if="user.vouchers.length > 2" href="#" class="see-all-btn" @click.prevent="showAllVouchers">
              {{ showAllVouchersFlag ? 'Show Less' : 'See All' }}
            </a>
          </div>
          
          <div v-if="user.vouchers.length > 0" class="vouchers-grid">
            <div 
              v-for="voucher in displayedVouchers" 
              :key="voucher.id"
              class="voucher-card"
              @click="openVoucherModal(voucher)"
            >
              <div class="voucher-icon">
                {{ getVoucherIcon(voucher.title) }}
              </div>
              <h3 class="voucher-title">{{ voucher.title }}</h3>
              <p class="voucher-subtitle">{{ voucher.subtitle }}</p>
              <span class="voucher-discount">{{ voucher.discount }}</span>
            </div>
          </div>
          
          <div v-else class="empty-vouchers">
            <div class="empty-icon">🎫</div>
            <p class="empty-text">Save vouchers from promotions to use them later!</p>
            <button class="promotions-btn" @click="$emit('setCurrentPage', 'Promotions')">
              Browse Promotions
            </button>
          </div>
        </div>

        <!-- QR Code Section -->
        <div class="qr-section">
          <h3 class="qr-title">Scan for Points</h3>
          <QRCode
            :code="user.pointsQRCode || generatePointsQRCode()"
            title=""
            subtitle=""
            :instructions="'Show this QR code when making a purchase to earn points'"
            size="medium"
          />
        </div>

        <!-- Settings Section -->
        <div class="settings-section">
          <h3 class="settings-title">Account & App Settings</h3>
          <p class="settings-description">Manage your profile information and app preferences</p>
          <div class="settings-buttons">
            <button class="settings-btn profile-settings-btn" @click="$emit('setCurrentPage', 'ProfileSettings')">
              👤 Profile Settings
            </button>
            <button class="settings-btn app-settings-btn" @click="$emit('setCurrentPage', 'Settings')">
              ⚙️ App Settings
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Voucher Modal -->
    <VoucherModal 
      :voucher="selectedVoucher"
      :isVisible="showVoucherModal"
      @close="closeVoucherModal"
      @useVoucher="handleUseVoucher"
      @saveVoucher="handleSaveVoucher"
      @removeVoucher="handleRemoveVoucher"
    />
  </div>
</template>

<script>
import QRCode from './QRCode.vue'
import VoucherModal from './VoucherModal.vue'

export default {
  name: 'Profile',
  components: {
    QRCode,
    VoucherModal
  },
  emits: ['setCurrentPage'],
  data() {
    return {
      user: {
        firstName: 'John',
        lastName: 'Doe',
        email: 'john.doe@example.com',
        points: 3280,
        vouchers: []
      },
      showVoucherModal: false,
      selectedVoucher: {},
      showAllVouchersFlag: false,
      isDarkMode: false,
      avatarHover: false
    }
  },
  computed: {
    displayedVouchers() {
      if (this.showAllVouchersFlag) {
        return this.user.vouchers;
      }
      return this.user.vouchers.slice(0, 2);
    }
  },
  mounted() {
    this.loadUserData();
    this.loadDarkModePreference();
    this.fetchCurrentUser();
    this.loadSavedVouchers();
  },
  methods: {
    loadUserData() {
      // Load user data from localStorage
      const userSession = localStorage.getItem('ramyeon_user_session');
      if (userSession) {
        const userData = JSON.parse(userSession);
        this.user = {
          ...userData,
          vouchers: [],
          pointsQRCode: userData.pointsQRCode || this.generatePointsQRCode()
        };
      } else {
        // Default user data if no session
        this.user = {
          firstName: 'Guest',
          lastName: 'User',
          email: 'guest@ramyeoncorner.com',
          points: 3280,
          vouchers: [],
          pointsQRCode: this.generatePointsQRCode()
        };
      }
    },

    loadSavedVouchers() {
      // Load saved vouchers from localStorage
      const savedVouchers = JSON.parse(localStorage.getItem('ramyeon_saved_vouchers') || '[]');
      this.user.vouchers = savedVouchers;
    },

    async fetchCurrentUser() {
      try {
        const { authAPI } = await import('../services/api.js')
        const user = await authAPI.getProfile()
        const first = user.first_name || user.firstName || (user.user_data?.full_name?.split(' ')[0])
        const last = user.last_name || user.lastName || (user.user_data?.full_name?.split(' ').slice(1).join(' ') || '')
        this.user = {
          ...this.user,
          firstName: first || this.user.firstName,
          lastName: last || this.user.lastName,
          email: user.email || this.user.email
        }
      } catch (e) {
        // ignore if not logged in
      }
    },

    loadDarkModePreference() {
      const darkMode = localStorage.getItem('ramyeon_dark_mode');
      this.isDarkMode = darkMode === 'true';
    },

    generatePointsQRCode() {
      return `POINTS-${this.user.email || 'guest'}-${Date.now()}`;
    },

    getVoucherIcon(title) {
      const icons = {
        'Shin Ramyun': '🍜',
        'Fish Cake': '🍢',
        'Welcome Bonus': '🎉',
        'Social Signup Bonus': '🎁',
        'Tteokbokki': '🌶️',
        'Kimchi': '🥬',
        'default': '🎫'
      };
      return icons[title] || icons.default;
    },

    openVoucherModal(voucher) {
      this.selectedVoucher = voucher;
      this.showVoucherModal = true;
    },

    closeVoucherModal() {
      this.showVoucherModal = false;
      this.selectedVoucher = {};
    },

    handleUseVoucher(voucher) {
      // Handle voucher usage
      console.log('Using voucher:', voucher);
      
      // Show success message
      this.showMessage('Voucher applied successfully!', 'success');
      
      // Remove voucher from user's vouchers (simulate usage)
      this.user.vouchers = this.user.vouchers.filter(v => v.id !== voucher.id);
      
      // Update localStorage - remove from saved vouchers
      const savedVouchers = JSON.parse(localStorage.getItem('ramyeon_saved_vouchers') || '[]');
      const updatedVouchers = savedVouchers.filter(v => v.id !== voucher.id);
      localStorage.setItem('ramyeon_saved_vouchers', JSON.stringify(updatedVouchers));
    },

    handleSaveVoucher(voucher) {
      // Handle voucher saving
      console.log('Saving voucher:', voucher);
      this.showMessage('Voucher saved for later!', 'info');
      
      // Reload vouchers to reflect any changes
      this.loadSavedVouchers();
    },

    handleRemoveVoucher(voucher) {
      // Handle voucher removal
      console.log('Removing voucher:', voucher);
      
      // Remove from UI
      this.user.vouchers = this.user.vouchers.filter(v => v.id !== voucher.id);
      
      // Show success message
      this.showMessage('Voucher removed!', 'info');
    },

    showAllVouchers() {
      this.showAllVouchersFlag = !this.showAllVouchersFlag;
    },

    updateUserSession() {
      const userSession = {
        ...this.user,
        loginTime: new Date().toISOString()
      };
      localStorage.setItem('ramyeon_user_session', JSON.stringify(userSession));
    },

    showMessage(text, type) {
      // Create and show a temporary message
      const messageDiv = document.createElement('div');
      messageDiv.className = `message ${type}`;
      messageDiv.textContent = text;
      messageDiv.style.position = 'fixed';
      messageDiv.style.top = '20px';
      messageDiv.style.right = '20px';
      messageDiv.style.zIndex = '9999';
      messageDiv.style.borderRadius = '8px';
      messageDiv.style.padding = '15px 20px';
      messageDiv.style.fontWeight = '500';
      messageDiv.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
      messageDiv.style.animation = 'slideInRight 0.3s ease-out';

      // Set colors based on type
      if (type === 'success') {
        messageDiv.style.background = '#d4edda';
        messageDiv.style.color = '#155724';
        messageDiv.style.border = '1px solid #c3e6cb';
      } else if (type === 'error') {
        messageDiv.style.background = '#f8d7da';
        messageDiv.style.color = '#721c24';
        messageDiv.style.border = '1px solid #f5c6cb';
      } else if (type === 'info') {
        messageDiv.style.background = '#cce7ff';
        messageDiv.style.color = '#004085';
        messageDiv.style.border = '1px solid #b3d7ff';
      }

      document.body.appendChild(messageDiv);

      // Remove message after 3 seconds
      setTimeout(() => {
        if (messageDiv.parentNode) {
          messageDiv.style.animation = 'slideOutRight 0.3s ease-in';
          setTimeout(() => {
            document.body.removeChild(messageDiv);
          }, 300);
        }
      }, 3000);
    }
  },

  // Watch for dark mode changes from settings
  watch: {
    '$root.isDarkMode'(newVal) {
      this.isDarkMode = newVal;
    }
  }
}
</script>

<style src="./Profile.css" scoped></style>

<style scoped>
/* Additional futuristic animations */
@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(100px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideOutRight {
  from {
    opacity: 1;
    transform: translateX(0);
  }
  to {
    opacity: 0;
    transform: translateX(100px);
  }
}

/* Message notifications with neon effect */
.message {
  padding: 18px 25px;
  border-radius: 15px;
  font-weight: 600;
  backdrop-filter: blur(20px);
  border: 1px solid;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.message.success {
  background: rgba(40, 167, 69, 0.2);
  color: #00ff88;
  border-color: rgba(0, 255, 136, 0.4);
  text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
}

.message.error {
  background: rgba(220, 53, 69, 0.2);
  color: #ff4757;
  border-color: rgba(255, 71, 87, 0.4);
  text-shadow: 0 0 10px rgba(255, 71, 87, 0.5);
}

.message.info {
  background: rgba(102, 126, 234, 0.2);
  color: #667eea;
  border-color: rgba(102, 126, 234, 0.4);
  text-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
}

/* Glowing text effect for hover */
.promotions-btn span {
  display: inline-block;
  margin-right: 8px;
  animation: iconSpin 3s linear infinite;
}

@keyframes iconSpin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Responsive enhancements */
@media (max-width: 480px) {
  .voucher-icon {
    width: 60px;
    height: 60px;
    font-size: 1.8rem;
  }
  
  .voucher-title {
    font-size: 1.2rem;
  }
  
  .voucher-subtitle {
    font-size: 0.85rem;
  }
  
  .voucher-discount {
    font-size: 0.9rem;
    padding: 8px 16px;
  }
  
  .empty-icon {
    font-size: 4rem;
  }
}
</style>
