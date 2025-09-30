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

        <!-- Address Book Section -->
        <div class="address-book-section">
          <h3 class="address-book-title">Address Book</h3>
          <p class="address-book-description">Manage your delivery addresses</p>
          
          <!-- Add New Address Button -->
          <button class="add-address-btn" @click="showAddAddress = true">
            + Add New Address
          </button>
          
          <!-- Address List -->
          <div class="address-list">
            <div 
              v-for="(address, index) in user.addresses" 
              :key="index"
              class="address-item"
              :class="{ 'default': address.isDefault }"
            >
              <div class="address-info">
                <h4 class="address-name">{{ address.name }}</h4>
                <p class="address-details">{{ address.street }}, {{ address.city }}, {{ address.province }}</p>
                <p class="address-postal">{{ address.postalCode }}</p>
                <div class="address-actions">
                  <button class="edit-btn" @click="editAddress(index)">Edit</button>
                  <button class="delete-btn" @click="deleteAddress(index)">Delete</button>
                  <button 
                    v-if="!address.isDefault" 
                    class="set-default-btn" 
                    @click="setDefaultAddress(index)"
                  >
                    Set as Default
                  </button>
                </div>
              </div>
              <div class="address-default" v-if="address.isDefault">
                <span class="default-badge">Default</span>
              </div>
            </div>
          </div>
          
          <!-- Add/Edit Address Modal -->
          <div class="address-modal" v-if="showAddAddress || editingAddress !== null">
            <div class="modal-content">
              <h3 class="modal-title">{{ editingAddress !== null ? 'Edit Address' : 'Add New Address' }}</h3>
              <form @submit.prevent="saveAddress">
                <div class="form-group">
                  <label for="addressName">Address Name</label>
                  <input 
                    type="text" 
                    id="addressName" 
                    v-model="currentAddress.name" 
                    placeholder="e.g., Home, Work"
                    required
                  />
                </div>
                <div class="form-group">
                  <label for="street">Street Address</label>
                  <input 
                    type="text" 
                    id="street" 
                    v-model="currentAddress.street" 
                    placeholder="Street name and number"
                    required
                  />
                </div>
                <div class="form-row">
                  <div class="form-group">
                    <label for="city">City</label>
                    <input 
                      type="text" 
                      id="city" 
                      v-model="currentAddress.city" 
                      placeholder="City"
                      required
                    />
                  </div>
                  <div class="form-group">
                    <label for="province">Province</label>
                    <input 
                      type="text" 
                      id="province" 
                      v-model="currentAddress.province" 
                      placeholder="Province"
                      required
                    />
                  </div>
                </div>
                <div class="form-group">
                  <label for="postalCode">Postal Code</label>
                  <input 
                    type="text" 
                    id="postalCode" 
                    v-model="currentAddress.postalCode" 
                    placeholder="Postal code"
                    required
                  />
                </div>
                <div class="form-group">
                  <label class="checkbox-label">
                    <input 
                      type="checkbox" 
                      v-model="currentAddress.isDefault"
                    />
                    Set as default delivery address
                  </label>
                </div>
                <div class="modal-actions">
                  <button type="button" class="cancel-btn" @click="cancelAddressEdit">Cancel</button>
                  <button type="submit" class="save-btn">Save Address</button>
                </div>
              </form>
            </div>
          </div>
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
        vouchers: [],
        addresses: [
          {
            name: 'Home',
            street: '123 Main St',
            city: 'Bislig',
            province: 'Surigao del Sur',
            postalCode: '8311',
            isDefault: true
          }
        ]
      },
      showVoucherModal: false,
      selectedVoucher: {},
      showAllVouchersFlag: false,
      isDarkMode: false,
      showAddAddress: false,
      editingAddress: null,
      currentAddress: {
        name: '',
        street: '',
        city: '',
        province: '',
        postalCode: '',
        isDefault: false
      }
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
    },

    editAddress(index) {
      this.editingAddress = index;
      this.currentAddress = { ...this.user.addresses[index] };
    },

    deleteAddress(index) {
      if (confirm('Are you sure you want to delete this address?')) {
        this.user.addresses.splice(index, 1);
        this.updateUserSession();
        this.showMessage('Address deleted successfully!', 'success');
      }
    },

    setDefaultAddress(index) {
      // Remove default from all addresses
      this.user.addresses.forEach(addr => addr.isDefault = false);
      // Set default for selected address
      this.user.addresses[index].isDefault = true;
      this.updateUserSession();
      this.showMessage('Default address updated!', 'success');
    },

    saveAddress() {
      if (this.editingAddress !== null) {
        // Update existing address
        this.user.addresses[this.editingAddress] = { ...this.currentAddress };
        this.showMessage('Address updated successfully!', 'success');
      } else {
        // Add new address
        this.user.addresses.push({ ...this.currentAddress });
        this.showMessage('Address added successfully!', 'success');
      }
      this.cancelAddressEdit();
      this.updateUserSession();
    },

    cancelAddressEdit() {
      this.showAddAddress = false;
      this.editingAddress = null;
      this.currentAddress = {
        name: '',
        street: '',
        city: '',
        province: '',
        postalCode: '',
        isDefault: false
      };
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

/* Address Book Styles */
.address-book-section {
  background: white;
  border-radius: 20px;
  padding: 25px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.address-book-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
}

.address-book-description {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 20px;
}

.add-address-btn {
  padding: 12px 20px;
  background: #ff4757;
  color: white;
  border: none;
  border-radius: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 20px;
}

.add-address-btn:hover {
  background: #ff3742;
  transform: translateY(-2px);
}

.address-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.address-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border: 2px solid #eee;
  border-radius: 15px;
  transition: all 0.3s ease;
  position: relative;
}

.address-item.default {
  border-color: #ff4757;
  background: rgba(255, 71, 87, 0.05);
}

.address-info {
  flex: 1;
}

.address-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
}

.address-details {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 5px;
}

.address-postal {
  color: #999;
  font-size: 0.8rem;
}

.address-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.edit-btn, .delete-btn, .set-default-btn {
  padding: 8px 12px;
  border: none;
  border-radius: 10px;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.edit-btn {
  background: #17a2b8;
  color: white;
}

.edit-btn:hover {
  background: #138496;
}

.delete-btn {
  background: #dc3545;
  color: white;
}

.delete-btn:hover {
  background: #c82333;
}

.set-default-btn {
  background: #28a745;
  color: white;
}

.set-default-btn:hover {
  background: #218838;
}

.address-default {
  display: flex;
  align-items: center;
}

.default-badge {
  background: #ff4757;
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.address-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 20px;
  padding: 30px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.form-group {
  margin-bottom: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.form-group label {
  display: block;
  font-weight: 500;
  color: #333;
  margin-bottom: 8px;
}

.form-group input {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid #eee;
  border-radius: 10px;
  font-size: 1rem;
  font-family: 'Poppins', sans-serif;
  transition: all 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #ff4757;
  box-shadow: 0 0 0 3px rgba(255, 71, 87, 0.1);
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 30px;
}

.cancel-btn, .save-btn {
  padding: 12px 20px;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn {
  background: #6c757d;
  color: white;
}

.cancel-btn:hover {
  background: #5a6268;
}

.save-btn {
  background: #28a745;
  color: white;
}

.save-btn:hover {
  background: #218838;
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
  
  .address-actions {
    flex-direction: column;
    gap: 5px;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .modal-content {
    padding: 20px;
  }
}
</style>
