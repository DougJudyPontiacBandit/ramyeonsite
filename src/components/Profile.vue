<template>
  <div class="profile-container" :class="{ 'dark-mode': isDarkMode }">
    <div class="profile-content">
      <!-- Profile Header -->
      <div class="profile-header">
        <div class="profile-avatar">
          👤
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
              <div class="points-value">{{ user.points }}</div>
              <div class="points-unit">pts</div>
            </div>
          </div>
          <button class="promotions-btn" @click="$emit('setCurrentPage', 'Promotions')">
            See Promotions
          </button>
        </div>

        <!-- Vouchers Section -->
        <div class="vouchers-section">
          <div class="section-header">
            <h2 class="section-title">Get vouchers</h2>
            <a href="#" class="see-all-btn" @click.prevent="showAllVouchers">See all</a>
          </div>
          
          <div class="vouchers-grid">
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
      isDarkMode: false
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
  },
  methods: {
    loadUserData() {
      // Load user data from localStorage
      const userSession = localStorage.getItem('ramyeon_user_session');
      if (userSession) {
        const userData = JSON.parse(userSession);
        this.user = {
          ...userData,
          pointsQRCode: userData.pointsQRCode || this.generatePointsQRCode()
        };
      } else {
        // Default user data if no session
        this.user = {
          firstName: 'Guest',
          lastName: 'User',
          email: 'guest@ramyeoncorner.com',
          points: 3280,
          vouchers: [
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
          pointsQRCode: this.generatePointsQRCode()
        };
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
      
      // Update localStorage
      this.updateUserSession();
    },

    handleSaveVoucher(voucher) {
      // Handle voucher saving
      console.log('Saving voucher:', voucher);
      this.showMessage('Voucher saved for later!', 'info');
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
/* Additional component-specific styles */
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

/* Enhanced voucher card hover effects */
.voucher-card {
  position: relative;
  overflow: hidden;
}

.voucher-card::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.voucher-card:hover::after {
  left: 100%;
}

/* Points circle enhanced animation */
.points-circle {
  position: relative;
  overflow: hidden;
}

.points-circle::after {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(45deg, #ff4757, #ff3742, #ff4757, #ff3742);
  border-radius: 50%;
  z-index: -1;
  animation: borderRotate 3s linear infinite;
}

@keyframes borderRotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* Responsive enhancements */
@media (max-width: 480px) {
  .voucher-icon {
    width: 40px;
    height: 40px;
    font-size: 1.2rem;
  }
  
  .voucher-title {
    font-size: 1.1rem;
  }
  
  .voucher-subtitle {
    font-size: 0.8rem;
  }
  
  .voucher-discount {
    font-size: 0.8rem;
    padding: 6px 12px;
  }
}
</style>
