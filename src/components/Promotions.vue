<template>
  <div class="promotions-page">
    <main class="main-content">
      <!-- Flash Sale Section -->
      <section class="flash-sale-section">
        <div class="flash-sale-card" :class="{ 'disabled': !isLoggedIn }" @click="handlePromotionClick('FLASH30', 'Flash Sale')">
          <div class="flash-sale-content">
            <div class="flash-sale-image">
              <img :src="ramyeonHero" alt="Ramyeon Bowl" />
            </div>
            <div class="flash-sale-text">
              <p class="flash-sale-duration">24 HOURS ONLY</p>
              <h2 class="flash-sale-title">FLASH SALE</h2>
              <div class="flash-sale-discount">30% OFF</div>
              <div class="flash-sale-code">
                <span>Use Code: </span>
                <span class="code-highlight">CORNER</span>
              </div>
              <div class="flash-sale-actions">
                <button class="order-btn" @click.stop="handlePromotionClick('FLASH30', 'Flash Sale')">Order Now</button>
                <button v-if="isLoggedIn" class="save-promotion-btn" @click.stop="savePromotion('FLASH30', 'Flash Sale', '30% OFF')" :disabled="isSaving">
                  <span v-if="!isSaving">💾 Save</span>
                  <span v-else>⏳ Saving...</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Top Food Items -->
      <section class="food-items-section">
        <div class="food-grid">
          <div
            v-for="(item, index) in topItems"
            :key="index"
            class="food-item-card"
            :class="{ 'disabled': !isLoggedIn }"
            @click="handlePromotionClick(item.code, item.name)"
          >
            <div class="food-image">
              <img :src="item.image" :alt="item.name" />
            </div>
            <div class="food-info">
              <h3 class="food-name">{{ item.name }}</h3>
              <p class="food-price">{{ item.price }}</p>
              <button v-if="isLoggedIn" class="save-item-btn" @click.stop="savePromotion(item.code, item.name, item.discount || 'Special Offer')" :disabled="isSaving">
                <span v-if="!isSaving">💾 Save</span>
                <span v-else>⏳</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Promotional Banner -->
      <section class="promo-banner">
        <div class="promo-banner-content">
          <div class="promo-text">
            <h3>ENJOY RAMYEON YOUR WAY!</h3>
            <p>Discover authentic Korean flavors with every bowl</p>
          </div>
          <div class="promo-icon">🍜</div>
        </div>
      </section>

      <!-- Bottom Food Items -->
      <section class="food-items-section">
        <div class="food-grid">
          <div
            v-for="(item, index) in bottomItems"
            :key="index"
            class="food-item-card"
            :class="{ 'disabled': !isLoggedIn }"
            @click="handlePromotionClick(item.code, item.name)"
          >
            <div class="food-image">
              <img :src="item.image" :alt="item.name" />
            </div>
            <div class="food-info">
              <h3 class="food-name">{{ item.name }}</h3>
              <p class="food-price">{{ item.price }}</p>
              <button v-if="isLoggedIn" class="save-item-btn" @click.stop="savePromotion(item.code, item.name, item.discount || 'Special Offer')" :disabled="isSaving">
                <span v-if="!isSaving">💾 Save</span>
                <span v-else>⏳</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Special Offers -->
      <section class="special-offers">
        <div class="offers-grid">
          <!-- Summer Offer -->
          <div class="summer-offer-card" :class="{ 'disabled': !isLoggedIn }" @click="handlePromotionClick('SUMMER40', 'Summer Special')">
            <div class="summer-offer-content">
              <div class="summer-offer-text">
                <h3>Special Summer Offer</h3>
                <div class="discount">40% OFF</div>
                <p>Ice cold different flavors to chill you in the summer!</p>
              </div>
              <div class="summer-offer-icon">🎁</div>
            </div>
            <button class="order-btn-red" @click.stop="handlePromotionClick('SUMMER40', 'Summer Special')">ORDER</button>
            <button v-if="isLoggedIn" class="save-offer-btn" @click.stop="savePromotion('SUMMER40', 'Summer Special', '40% OFF')" :disabled="isSaving">
              <span v-if="!isSaving">💾 Save</span>
              <span v-else>⏳</span>
            </button>
          </div>

          <!-- Vouchers -->
          <div class="vouchers-section">
            <div class="voucher-card" :class="{ 'disabled': !isLoggedIn }" @click="handlePromotionClick('STORE10', 'Store Voucher')">
              <div class="voucher-content">
                <div class="voucher-icon">🎁</div>
                <div class="voucher-text">
                  <div class="voucher-discount">₱ 10 OFF</div>
                  <div class="voucher-title">STORE VOUCHER</div>
                </div>
              </div>
              <button v-if="isLoggedIn" class="save-voucher-btn" @click.stop="savePromotion('STORE10', 'Store Voucher', '₱ 10 OFF')" :disabled="isSaving">
                <span v-if="!isSaving">💾 Save</span>
                <span v-else>⏳</span>
              </button>
            </div>
            <div class="voucher-card delivery-voucher" :class="{ 'disabled': !isLoggedIn }" @click="handlePromotionClick('DELIVERY20', 'Delivery Voucher')">
              <div class="voucher-content">
                <div class="voucher-icon">🚚</div>
                <div class="voucher-text">
                  <div class="voucher-discount">₱ 20 OFF</div>
                  <div class="voucher-title">DELIVERY VOUCHER</div>
                </div>
              </div>
              <button v-if="isLoggedIn" class="save-voucher-btn" @click.stop="savePromotion('DELIVERY20', 'Delivery Voucher', '₱ 20 OFF')" :disabled="isSaving">
                <span v-if="!isSaving">💾 Save</span>
                <span v-else>⏳</span>
              </button>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- Modal for QR Code -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <h3>{{ modalTitle }}</h3>
        <div v-if="isTextCode" class="text-code">
          <p>Your promo code:</p>
          <div class="code-display">{{ currentCode }}</div>
          <p class="code-instruction">Show this code to the cashier</p>
        </div>
        <div v-else class="qr-code">
          <canvas ref="qrCanvas"></canvas>
          <p class="qr-instruction">Scan this QR code to apply the promotion</p>
        </div>
        <button @click="closeModal" class="close-btn">Close</button>
      </div>
    </div>
  </div>
</template>

<script>
import QRCode from 'qrcode'

export default {
  name: 'Promotions',
  emits: ['setCurrentPage'],
  props: {
    isLoggedIn: Boolean
  },
  data() {
    return {
      showModal: false,
      modalTitle: '',
      currentCode: '',
      isTextCode: false,
      isSaving: false,
      ramyeonHero: require('@/assets/food/ramyeon-hero.jpg'),
      topItems: [
        {
          name: "SHIN RAMYEON",
          price: "₱100.00",
          image: require('@/assets/food/kimchi.jpg'),
          code: "SHIN15",
          discount: "15% OFF"
        },
        {
          name: "NEO GURI",
          price: "₱120.00",
          image: require('@/assets/food/bulgogi.jpg'),
          code: "NEO20",
          discount: "20% OFF"
        },
        {
          name: "CORN DOG",
          price: "₱85.00",
          image: require('@/assets/food/corn-dog.jpg'),
          code: "CORN10",
          discount: "10% OFF"
        },
      ],
      bottomItems: [
        {
          name: "KIMCHI",
          price: "₱80.00",
          image: require('@/assets/food/kimchi.jpg'),
          code: "KIMCHI12",
          discount: "12% OFF"
        },
        {
          name: "FISH CAKE",
          price: "₱90.00",
          image: require('@/assets/food/fish-cake.jpg'),
          code: "FISH18",
          discount: "18% OFF"
        },
        {
          name: "TTEOKBOKKI",
          price: "₱110.00",
          image: require('@/assets/food/tteokbokki.jpg'),
          code: "TTEOK25",
          discount: "25% OFF"
        },
      ]
    }
  },
  methods: {
    goBack() {
      this.$emit('setCurrentPage', 'Home')
    },
    handlePromotionClick(code, title) {
      if (!this.isLoggedIn) {
        this.showErrorMessage('Please log in to access promotions!')
        return
      }
      this.showPromoCode(code, title)
    },
    async showPromoCode(code, title) {
      this.currentCode = code
      this.modalTitle = title
      this.isTextCode = false
      this.showModal = true

      // Generate QR code
      await this.$nextTick()
      if (this.$refs.qrCanvas) {
        try {
          await QRCode.toCanvas(this.$refs.qrCanvas, code, {
            width: 200,
            margin: 2,
            color: {
              dark: '#000000',
              light: '#FFFFFF'
            }
          })
        } catch (error) {
          console.error('Error generating QR code:', error)
        }
      }
    },
    showTextCode(code, title) {
      this.currentCode = code
      this.modalTitle = title
      this.isTextCode = true
      this.showModal = true
    },
    closeModal() {
      this.showModal = false
      this.currentCode = ''
      this.modalTitle = ''
      this.isTextCode = false
    },

    async savePromotion(code, title, discount) {
      if (!this.isLoggedIn) {
        this.showErrorMessage('Please log in to save promotions!')
        return
      }

      this.isSaving = true

      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1500))

        // Create promotion voucher object
        const promotionVoucher = {
          id: Date.now(), // Generate unique ID
          title: title,
          subtitle: 'Promotion Offer',
          discount: discount,
          code: code,
          qrCode: `${code}-QR-${Date.now()}`,
          savedAt: new Date().toISOString(),
          type: 'promotion'
        }

        // Save to localStorage
        const savedVouchers = JSON.parse(localStorage.getItem('ramyeon_saved_vouchers') || '[]')

        // Check if already saved
        const exists = savedVouchers.find(v => v.code === code)
        if (!exists) {
          savedVouchers.push(promotionVoucher)
          localStorage.setItem('ramyeon_saved_vouchers', JSON.stringify(savedVouchers))
        }

        // Show success message
        this.showSuccessMessage('Promotion saved! Redirecting to profile...')

        // Redirect to profile after short delay
        setTimeout(() => {
          this.$emit('setCurrentPage', 'Profile')
        }, 1000)

      } catch (error) {
        console.error('Error saving promotion:', error)
        this.showErrorMessage('Failed to save promotion. Please try again.')
      } finally {
        this.isSaving = false
      }
    },

    showSuccessMessage(message) {
      // Create success notification
      const notification = document.createElement('div')
      notification.innerHTML = `
        <div style="
          position: fixed;
          top: 20px;
          right: 20px;
          background: linear-gradient(135deg, #28a745, #20c997);
          color: white;
          padding: 15px 25px;
          border-radius: 12px;
          box-shadow: 0 8px 25px rgba(40, 167, 69, 0.3);
          z-index: 9999;
          font-family: 'Poppins', sans-serif;
          font-weight: 600;
          animation: slideInRight 0.3s ease-out;
          display: flex;
          align-items: center;
          gap: 10px;
        ">
          <span style="font-size: 1.2rem;">✅</span>
          ${message}
        </div>
        <style>
          @keyframes slideInRight {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
          }
        </style>
      `

      document.body.appendChild(notification)

      // Remove after 3 seconds
      setTimeout(() => {
        if (notification.parentNode) {
          notification.style.animation = 'slideInRight 0.3s ease-in reverse'
          setTimeout(() => {
            document.body.removeChild(notification)
          }, 300)
        }
      }, 3000)
    },

    showErrorMessage(message) {
      // Create error notification
      const notification = document.createElement('div')
      notification.innerHTML = `
        <div style="
          position: fixed;
          top: 20px;
          right: 20px;
          background: linear-gradient(135deg, #dc3545, #c82333);
          color: white;
          padding: 15px 25px;
          border-radius: 12px;
          box-shadow: 0 8px 25px rgba(220, 53, 69, 0.3);
          z-index: 9999;
          font-family: 'Poppins', sans-serif;
          font-weight: 600;
          animation: slideInRight 0.3s ease-out;
          display: flex;
          align-items: center;
          gap: 10px;
        ">
          <span style="font-size: 1.2rem;">❌</span>
          ${message}
        </div>
        <style>
          @keyframes slideInRight {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
          }
        </style>
      `

      document.body.appendChild(notification)

      // Remove after 3 seconds
      setTimeout(() => {
        if (notification.parentNode) {
          notification.style.animation = 'slideInRight 0.3s ease-in reverse'
          setTimeout(() => {
            document.body.removeChild(notification)
          }, 300)
        }
      }, 3000)
    }
  }
}
</script>

<style scoped>
@import './Promotions.css';

/* Additional styles for save buttons */
.save-promotion-btn, .save-item-btn, .save-offer-btn, .save-voucher-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  margin-top: 8px;
}

.save-promotion-btn:hover, .save-item-btn:hover, .save-offer-btn:hover, .save-voucher-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

.save-promotion-btn:disabled, .save-item-btn:disabled, .save-offer-btn:disabled, .save-voucher-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* Disabled state for promotions */
.food-item-card.disabled, .flash-sale-card.disabled, .summer-offer-card.disabled, .voucher-card.disabled {
  opacity: 0.6;
  cursor: not-allowed;
  filter: grayscale(50%);
}

.food-item-card.disabled:hover, .flash-sale-card.disabled:hover, .summer-offer-card.disabled:hover, .voucher-card.disabled:hover {
  transform: none;
}

/* Position save buttons */
.food-info {
  position: relative;
}

.save-item-btn {
  position: absolute;
  top: 10px;
  right: 10px;
}

.save-offer-btn {
  margin-top: 10px;
  width: 100%;
}

.save-voucher-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 6px 12px;
  font-size: 12px;
}
</style>
