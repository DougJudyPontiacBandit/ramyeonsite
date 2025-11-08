<template>
  <div class="promotions-page">
    <!-- Loading State -->
    <div v-if="isLoading" class="loading-container">
      <div class="loading-spinner-big"></div>
      <p>Loading promotions...</p>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="error-container">
      <div class="error-icon">⚠️</div>
      <h3>Failed to Load Promotions</h3>
      <p>{{ error || 'An error occurred while loading promotions' }}</p>
      <button @click="fetchActivePromotions" class="retry-btn">Retry</button>
    </div>
    
    <!-- No Promotions State -->
    <div v-else-if="!isLoading && (!activePromotions || activePromotions.length === 0)" class="empty-promotions">
      <div class="empty-icon">🎁</div>
      <h3>No Active Promotions</h3>
      <p>Check back later for exciting deals and offers!</p>
    </div>
    
    <!-- Active Promotions Headlines -->
    <main v-else-if="activePromotions && activePromotions.length > 0" class="main-content">
      <div 
        v-for="promotion in activePromotions" 
        :key="promotion.promotion_id || promotion.id || promotion._id"
        class="promotion-headline"
        :class="{ 'disabled': !isLoggedIn }"
        @click="handlePromotionClick(promotion)"
      >
        <div class="promotion-image-container">
          <img 
            :src="getPromotionImage(promotion)" 
            :alt="promotion.name || promotion.promotion_name || 'Promotion'"
            class="promotion-image"
            @error="handleImageError"
          />
        </div>
        <div class="headline-content">
          <div class="headline-text">
            <h2 class="headline-title">{{ promotion.name || promotion.promotion_name || 'Special Promotion' }}</h2>
            <p class="headline-description" v-if="promotion.description || promotion.promotion_description">
              {{ promotion.description || promotion.promotion_description }}
            </p>
            <div class="headline-discount">
              <span v-if="promotion.type === 'percentage' || promotion.discount_type === 'percentage'">
                {{ promotion.discount_value || 0 }}% OFF
              </span>
              <span v-else-if="promotion.type === 'fixed_amount' || promotion.discount_type === 'fixed'">
                ₱{{ promotion.discount_value || 0 }} OFF
              </span>
              <span v-else>{{ getPromotionDisplay(promotion) }}</span>
            </div>
            <div class="headline-code" v-if="promotion.promotion_code || promotion.code">
              <span>Code: </span>
              <span class="code-value">{{ promotion.promotion_code || promotion.code }}</span>
            </div>
          </div>
          <div class="headline-actions">
            <button 
              v-if="isLoggedIn" 
              class="order-btn" 
              @click.stop="handlePromotionClick(promotion)"
            >
              <span class="btn-icon">🛒</span>
              <span>Order Now</span>
            </button>
            <button 
              v-if="isLoggedIn" 
              class="save-btn" 
              @click.stop="savePromotion(promotion)"
              :disabled="isSaving(promotion.promotion_id || promotion.id || promotion._id)"
            >
              <span v-if="!isSaving(promotion.promotion_id || promotion.id || promotion._id)" class="btn-icon">💾</span>
              <span v-else class="loading-spinner-small"></span>
              <span>{{ isSaving(promotion.promotion_id || promotion.id || promotion._id) ? 'Saving...' : 'Save' }}</span>
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { usePromotions } from '../composables/api/usePromotions.js'

export default {
  name: 'Promotions',
  emits: ['setCurrentPage'],
  props: {
    isLoggedIn: Boolean
  },
  setup() {
    const promotions = usePromotions();
    return {
      ...promotions
    };
  },
  data() {
    return {
      savingPromotions: {},
      fallbackImages: {
        'ramyeon': require('@/assets/food/ramyeon-hero.jpg'),
        'ramen': require('@/assets/food/ramyeon-hero.jpg'),
        'kimchi': require('@/assets/food/kimchi.jpg'),
        'bulgogi': require('@/assets/food/bulgogi.jpg'),
        'corndog': require('@/assets/food/corn-dog.jpg'),
        'corn-dog': require('@/assets/food/corn-dog.jpg'),
        'fishcake': require('@/assets/food/fish-cake.jpg'),
        'fish-cake': require('@/assets/food/fish-cake.jpg'),
        'tteokbokki': require('@/assets/food/tteokbokki.jpg'),
        'drinks': require('@/assets/food/ramyeon-hero.jpg'),
        'drink': require('@/assets/food/ramyeon-hero.jpg'),
        'default': require('@/assets/food/ramyeon-hero.jpg')
      }
    }
  },
  async mounted() {
    await this.fetchActivePromotions();
  },
  methods: {
    async fetchActivePromotions() {
      try {
        console.log('🎯 Fetching active promotions from database...')
        const result = await this.getActivePromotions()
        
        if (result && result.success) {
          console.log('✅ Loaded', this.activePromotions?.length || 0, 'active promotions')
          console.log('Promotions:', this.activePromotions)
        } else if (result && result.error) {
          console.error('❌ Error from API:', result.error)
          this.showErrorMessage(result.error || 'Could not load promotions. Please try again later.')
        }
      } catch (error) {
        console.error('❌ Error fetching promotions:', error)
        const errorMessage = error?.message || error?.error || 'Could not load promotions. Please try again later.'
        this.showErrorMessage(errorMessage)
      }
    },
    
    getPromotionDisplay(promotion) {
      if (promotion.type === 'buy_x_get_y' || promotion.discount_type === 'buy_x_get_y') {
        const config = promotion.discount_config || promotion.config || {}
        return `Buy ${config.buy_quantity || 2} Get ${config.get_quantity || 1} Free`
      }
      return 'Special Offer'
    },
    
    handlePromotionClick(promotion) {
      if (!this.isLoggedIn) {
        this.showErrorMessage('Please log in to access promotions!')
        return
      }
      // Log promotion for debugging
      console.log('🎯 Promotion clicked:', promotion?.name || promotion?.promotion_name)
      // Navigate to menu or cart
      this.$emit('setCurrentPage', 'Menu')
    },
    
    isSaving(promotionId) {
      return this.savingPromotions[promotionId] === true
    },
    
    getPromotionImage(promotion) {
      // Check if promotion has an image URL
      if (promotion.image_url) {
        return promotion.image_url
      }
      if (promotion.image) {
        return promotion.image
      }
      
      // Try to match promotion name to an image
      const nameLower = (promotion.name || promotion.promotion_name || '').toLowerCase()
      
      // Check for keywords in the name
      for (const [key, image] of Object.entries(this.fallbackImages)) {
        if (nameLower.includes(key)) {
          return image
        }
      }
      
      // Check target_type or description for hints
      const description = (promotion.description || promotion.promotion_description || '').toLowerCase()
      for (const [key, image] of Object.entries(this.fallbackImages)) {
        if (description.includes(key)) {
          return image
        }
      }
      
      // Default image
      return this.fallbackImages.default
    },
    
    handleImageError(event) {
      // Fallback to default image if image fails to load
      event.target.src = this.fallbackImages.default
    },
    
    async savePromotion(promotion) {
      if (!this.isLoggedIn) {
        this.showErrorMessage('Please log in to save promotions!')
        return
      }

      if (this.savingPromotions[promotion.promotion_id]) {
        return
      }

      this.savingPromotions[promotion.promotion_id] = true

      try {
        const savedVouchers = JSON.parse(localStorage.getItem('ramyeon_saved_vouchers') || '[]')
        const exists = savedVouchers.find(v => v.promotion_id === promotion.promotion_id)
        
        if (exists) {
          this.showErrorMessage('This promotion is already saved!')
          return
        }

        const discountText = (promotion.type === 'percentage' || promotion.discount_type === 'percentage')
          ? `${promotion.discount_value || 0}% OFF`
          : (promotion.type === 'fixed_amount' || promotion.discount_type === 'fixed')
          ? `₱${promotion.discount_value || 0} OFF`
          : this.getPromotionDisplay(promotion)

        const promotionVoucher = {
          id: Date.now(),
          promotion_id: promotion.promotion_id || promotion.id || promotion._id,
          title: promotion.name || promotion.promotion_name || 'Special Promotion',
          subtitle: promotion.description || promotion.promotion_description || 'Promotion Offer',
          discount: discountText,
          code: promotion.promotion_code || promotion.code || promotion.promotion_id || promotion.id,
          type: 'promotion',
          promotionData: {
            type: promotion.type || promotion.discount_type,
            discount_value: promotion.discount_value || 0,
            target_type: promotion.target_type,
            target_ids: promotion.target_ids,
            start_date: promotion.start_date,
            end_date: promotion.end_date,
            usage_limit: promotion.usage_limit,
            current_usage: promotion.current_usage
          },
          qrCode: `${promotion.promotion_id || promotion.id || promotion._id}-QR-${Date.now()}`,
          savedAt: new Date().toISOString()
        }

        savedVouchers.push(promotionVoucher)
        localStorage.setItem('ramyeon_saved_vouchers', JSON.stringify(savedVouchers))

        console.log('✅ Promotion saved:', promotionVoucher)
        this.showSuccessMessage('Promotion saved! Redirecting to profile...')

        setTimeout(() => {
          this.$emit('setCurrentPage', 'Profile')
        }, 1000)

      } catch (error) {
        console.error('Error saving promotion:', error)
        this.showErrorMessage('Failed to save promotion. Please try again.')
      } finally {
        this.savingPromotions[promotion.promotion_id] = false
      }
    },

    showSuccessMessage(message) {
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
.promotions-page {
  background: linear-gradient(135deg, #faf8f5 0%, #fff5f0 50%, #faf8f5 100%);
  background-size: 400% 400%;
  animation: gradientShift 15s ease infinite;
  font-family: 'Poppins', 'Arial', sans-serif;
  padding: 40px 20px 20px 20px;
  min-height: auto;
  margin-bottom: 0;
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 30px;
  padding-bottom: 0;
  margin-bottom: 0;
}

/* Promotion Headline Style */
.promotion-headline {
  background: linear-gradient(135deg, #ff6f61, #ff4a3d);
  border-radius: 20px;
  padding: 0;
  box-shadow: 0 10px 30px rgba(255, 111, 97, 0.3);
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: stretch;
  min-height: 300px;
}

.promotion-image-container {
  position: relative;
  width: 40%;
  min-width: 300px;
  overflow: hidden;
  flex-shrink: 0;
}

.promotion-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.image-overlay {
  display: none;
}

.promotion-headline::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transition: left 0.8s ease;
  z-index: 2;
}

.promotion-headline:hover::before {
  left: 100%;
}

.promotion-headline:hover .promotion-image {
  transform: scale(1.1);
}

.promotion-headline:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(255, 111, 97, 0.4);
}

.promotion-headline.disabled {
  opacity: 0.6;
  cursor: not-allowed;
  filter: grayscale(50%);
}

.promotion-headline.disabled:hover {
  transform: none;
}

.headline-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 30px;
  position: relative;
  z-index: 1;
  padding: 40px;
  flex: 1;
}

.headline-text {
  flex: 1;
  color: white;
}

.headline-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin: 0 0 15px 0;
  text-transform: uppercase;
  letter-spacing: 1px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.headline-description {
  font-size: 1.1rem;
  margin: 0 0 20px 0;
  opacity: 0.95;
  line-height: 1.6;
}

.headline-discount {
  font-size: 3rem;
  font-weight: 900;
  margin: 20px 0;
  text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.3);
  letter-spacing: 2px;
}

.headline-code {
  font-size: 1.1rem;
  margin-top: 15px;
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  display: inline-block;
  backdrop-filter: blur(10px);
}

.code-value {
  font-weight: 700;
  font-size: 1.2rem;
  letter-spacing: 2px;
}

.headline-actions {
  display: flex;
  flex-direction: column;
  gap: 15px;
  min-width: 180px;
}

.order-btn,
.save-btn {
  background: white;
  color: #ff6f61;
  border: 2px solid rgba(255, 255, 255, 0.3);
  padding: 15px 30px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 4px 15px rgba(255, 255, 255, 0.3);
}

.order-btn:hover,
.save-btn:hover {
  background: rgba(255, 255, 255, 0.95);
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(255, 255, 255, 0.5);
}

.save-btn {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border-color: rgba(255, 255, 255, 0.4);
}

.save-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-icon {
  font-size: 1.2rem;
}

.loading-spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Loading, Error, Empty States */
.loading-container,
.error-container,
.empty-promotions {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  padding: 40px 20px;
  text-align: center;
}

.loading-spinner-big {
  width: 60px;
  height: 60px;
  border: 4px solid rgba(255, 111, 97, 0.2);
  border-top-color: #ff6f61;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

.loading-container p {
  font-size: 1.2rem;
  color: #666;
  font-weight: 600;
}

.error-container,
.empty-promotions {
  background: white;
  border-radius: 20px;
  padding: 60px 40px;
  max-width: 500px;
  margin: 40px auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.error-icon,
.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.error-container h3,
.empty-promotions h3 {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 15px;
  font-weight: 700;
}

.error-container p,
.empty-promotions p {
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 30px;
  line-height: 1.6;
}

.retry-btn {
  background: linear-gradient(135deg, #ff6f61, #ff4a3d);
  color: white;
  border: none;
  padding: 15px 40px;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.retry-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(255, 111, 97, 0.4);
}

/* Responsive Design */
@media (max-width: 968px) {
  .promotion-headline {
    flex-direction: column;
    min-height: auto;
  }

  .promotion-image-container {
    width: 100%;
    min-width: 100%;
    height: 250px;
  }
}

@media (max-width: 768px) {
  .promotions-page {
    padding: 20px 15px;
  }

  .promotion-headline {
    min-height: auto;
  }

  .headline-content {
    flex-direction: column;
    text-align: center;
    padding: 30px 20px;
  }

  .headline-title {
    font-size: 2rem;
  }

  .headline-discount {
    font-size: 2.5rem;
  }

  .headline-actions {
    width: 100%;
    flex-direction: row;
  }

  .order-btn,
  .save-btn {
    flex: 1;
  }
}

@media (max-width: 480px) {
  .headline-title {
    font-size: 1.5rem;
  }

  .headline-discount {
    font-size: 2rem;
  }

  .headline-description {
    font-size: 1rem;
  }
}
</style>
