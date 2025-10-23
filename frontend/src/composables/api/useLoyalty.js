import { ref, computed } from 'vue'
import { loyaltyAPI } from '@/services/api'

/**
 * Composable for managing loyalty points
 * Handles balance, history, tiers, earning, and redemption
 */
export function useLoyalty() {
  // ================================================================
  // REACTIVE STATE
  // ================================================================
  
  const loyaltyBalance = ref(0)
  const loyaltyHistory = ref([])
  const loyaltyTiers = ref([])
  const currentTier = ref(null)
  const isLoading = ref(false)
  const error = ref(null)
  
  // Cache for performance
  const loyaltyCache = ref(new Map())
  const historyCache = ref(null)
  const lastFetchTime = ref(0)
  const CACHE_DURATION = 5 * 60 * 1000 // 5 minutes

  // ================================================================
  // COMPUTED PROPERTIES
  // ================================================================
  
  const hasLoyaltyPoints = computed(() => loyaltyBalance.value > 0)
  const canRedeemPoints = computed(() => loyaltyBalance.value >= 40) // Minimum 40 points
  const maxRedemptionAmount = computed(() => Math.min(loyaltyBalance.value / 4, 20)) // Max ₱20
  const pointsValue = computed(() => loyaltyBalance.value / 4) // 4 points = ₱1

  // ================================================================
  // CORE METHODS
  // ================================================================

  /**
   * Get customer loyalty points balance
   * @param {string} userId - Customer ID
   * @returns {Promise<Object>} Balance result
   */
  const getLoyaltyBalance = async (userId) => {
    try {
      isLoading.value = true
      error.value = null
      
      console.log('💎 Fetching loyalty balance for user:', userId)
      
      // Check cache first
      if (loyaltyCache.value.has(`balance_${userId}`)) {
        const cached = loyaltyCache.value.get(`balance_${userId}`)
        if (Date.now() - cached.timestamp < CACHE_DURATION) {
          loyaltyBalance.value = cached.data
          console.log('💎 Using cached loyalty balance:', loyaltyBalance.value)
          return { success: true, data: { balance: loyaltyBalance.value } }
        }
      }
      
      // Fetch from API
      const result = await loyaltyAPI.getBalance(userId)
      
      if (result.success) {
        loyaltyBalance.value = result.data?.balance || result.balance || 0
        lastFetchTime.value = Date.now()
        
        // Cache the result
        loyaltyCache.value.set(`balance_${userId}`, {
          data: loyaltyBalance.value,
          timestamp: Date.now()
        })
        
        console.log(`✅ Loyalty balance: ${loyaltyBalance.value} points`)
        return { success: true, data: { balance: loyaltyBalance.value } }
      } else {
        throw new Error(result.error || 'Failed to fetch loyalty balance')
      }
    } catch (err) {
      console.error('❌ Error fetching loyalty balance:', err)
      error.value = err.message
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Get customer loyalty points history
   * @param {string} userId - Customer ID
   * @param {Object} filters - Filter options
   * @returns {Promise<Object>} History result
   */
  const getLoyaltyHistory = async (userId, filters = {}) => {
    try {
      isLoading.value = true
      error.value = null
      
      console.log('📜 Fetching loyalty history for user:', userId)
      
      // Check cache first
      const cacheKey = `history_${userId}_${JSON.stringify(filters)}`
      if (historyCache.value && historyCache.value.key === cacheKey) {
        const cached = historyCache.value
        if (Date.now() - cached.timestamp < CACHE_DURATION) {
          loyaltyHistory.value = cached.data
          console.log('📜 Using cached loyalty history:', loyaltyHistory.value.length, 'transactions')
          return { success: true, data: loyaltyHistory.value }
        }
      }
      
      // Fetch from API
      const result = await loyaltyAPI.getHistory(userId, filters)
      
      if (result.success) {
        loyaltyHistory.value = result.data?.results || result.data?.history || result.history || []
        historyCache.value = {
          data: loyaltyHistory.value,
          key: cacheKey,
          timestamp: Date.now()
        }
        
        console.log(`✅ Fetched ${loyaltyHistory.value.length} loyalty transactions`)
        return { success: true, data: loyaltyHistory.value }
      } else {
        throw new Error(result.error || 'Failed to fetch loyalty history')
      }
    } catch (err) {
      console.error('❌ Error fetching loyalty history:', err)
      error.value = err.message
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Get loyalty tiers
   * @returns {Promise<Object>} Tiers result
   */
  const getLoyaltyTiers = async () => {
    try {
      isLoading.value = true
      error.value = null
      
      console.log('👑 Fetching loyalty tiers')
      
      const result = await loyaltyAPI.getTiers()
      
      if (result.success) {
        loyaltyTiers.value = result.data?.tiers || result.tiers || []
        console.log(`✅ Fetched ${loyaltyTiers.value.length} loyalty tiers`)
        return { success: true, data: loyaltyTiers.value }
      } else {
        throw new Error(result.error || 'Failed to fetch loyalty tiers')
      }
    } catch (err) {
      console.error('❌ Error fetching loyalty tiers:', err)
      error.value = err.message
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Get current loyalty tier for customer
   * @param {string} userId - Customer ID
   * @returns {Promise<Object>} Current tier result
   */
  const getCurrentTier = async (userId) => {
    try {
      isLoading.value = true
      error.value = null
      
      console.log('👑 Fetching current loyalty tier for user:', userId)
      
      // Check cache first
      if (loyaltyCache.value.has(`tier_${userId}`)) {
        const cached = loyaltyCache.value.get(`tier_${userId}`)
        if (Date.now() - cached.timestamp < CACHE_DURATION) {
          currentTier.value = cached.data
          console.log('👑 Using cached loyalty tier:', currentTier.value?.name)
          return { success: true, data: currentTier.value }
        }
      }
      
      // Fetch from API
      const result = await loyaltyAPI.getCurrentTier(userId)
      
      if (result.success) {
        currentTier.value = result.data || result.tier
        lastFetchTime.value = Date.now()
        
        // Cache the result
        loyaltyCache.value.set(`tier_${userId}`, {
          data: result.data,
          timestamp: Date.now()
        })
        
        console.log(`✅ Current tier: ${currentTier.value.name}`)
        return { success: true, data: result.data }
      } else {
        throw new Error(result.error || 'Failed to fetch current tier')
      }
    } catch (err) {
      console.error('❌ Error fetching current tier:', err)
      error.value = err.message
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }

  // ================================================================
  // POINTS CALCULATION METHODS
  // ================================================================

  /**
   * Calculate loyalty points earned from order
   * @param {number} subtotalAfterDiscount - Subtotal after discounts
   * @returns {Promise<Object>} Points calculation result
   */
  const calculatePointsEarned = async (subtotalAfterDiscount) => {
    try {
      console.log('🧮 Calculating loyalty points earned for subtotal:', subtotalAfterDiscount)
      
      const result = await loyaltyAPI.calculatePointsEarned(subtotalAfterDiscount)
      
      if (result.success) {
        const points = result.points_earned || result.data?.points_earned || 0
        console.log(`✅ Points earned: ${points}`)
        return { success: true, data: { points_earned: points } }
      } else {
        throw new Error(result.error || 'Failed to calculate points earned')
      }
    } catch (err) {
      console.error('❌ Error calculating points earned:', err)
      return { success: false, error: err.message }
    }
  }

  /**
   * Calculate discount from loyalty points
   * @param {number} pointsToRedeem - Points to redeem
   * @returns {Object} Discount calculation
   */
  const calculatePointsDiscount = (pointsToRedeem) => {
    try {
      // 4 points = ₱1 discount
      const discountAmount = pointsToRedeem / 4
      const maxDiscount = 20 // Maximum ₱20 discount
      const actualDiscount = Math.min(discountAmount, maxDiscount)
      
      return {
        points_used: pointsToRedeem,
        discount_amount: Math.round(actualDiscount * 100) / 100,
        max_discount: maxDiscount,
        points_remaining: loyaltyBalance.value - pointsToRedeem
      }
    } catch (err) {
      console.error('❌ Error calculating points discount:', err)
      return { points_used: 0, discount_amount: 0, max_discount: 20, points_remaining: loyaltyBalance.value }
    }
  }

  /**
   * Validate points redemption
   * @param {string} customerId - Customer ID
   * @param {number} pointsToRedeem - Points to redeem
   * @param {number} subtotal - Order subtotal
   * @returns {Promise<Object>} Validation result
   */
  const validatePointsRedemption = async (customerId, pointsToRedeem, subtotal) => {
    try {
      console.log('🔍 Validating points redemption:', { customerId, pointsToRedeem, subtotal })
      
      const result = await loyaltyAPI.validateRedemption(pointsToRedeem, subtotal, customerId)
      
      if (result.success) {
        console.log('✅ Points redemption validation successful')
        return { success: true, data: result.data }
      } else {
        throw new Error(result.error || 'Points redemption validation failed')
      }
    } catch (err) {
      console.error('❌ Error validating points redemption:', err)
      return { success: false, error: err.message }
    }
  }

  /**
   * Redeem loyalty points
   * @param {string} customerId - Customer ID
   * @param {number} pointsToRedeem - Points to redeem
   * @param {number} subtotal - Order subtotal
   * @returns {Promise<Object>} Redemption result
   */
  const redeemPoints = async (customerId, pointsToRedeem, subtotal) => {
    try {
      console.log('💎 Redeeming loyalty points:', { customerId, pointsToRedeem, subtotal })
      
      // Validate first
      const validation = await validatePointsRedemption(customerId, pointsToRedeem, subtotal)
      if (!validation.success) {
        throw new Error(validation.error)
      }

      // Update local balance
      loyaltyBalance.value = Math.max(0, loyaltyBalance.value - pointsToRedeem)
      
      console.log('✅ Points redeemed successfully')
      return { success: true, data: { new_balance: loyaltyBalance.value } }
    } catch (err) {
      console.error('❌ Error redeeming points:', err)
      return { success: false, error: err.message }
    }
  }

  /**
   * Award loyalty points
   * @param {string} customerId - Customer ID
   * @param {number} pointsToAward - Points to award
   * @param {string} reason - Reason for awarding points
   * @returns {Promise<Object>} Award result
   */
  const awardPoints = async (customerId, pointsToAward, reason = 'Order completion') => {
    try {
      console.log('🎁 Awarding loyalty points:', { customerId, pointsToAward, reason })
      
      // Update local balance
      loyaltyBalance.value += pointsToAward
      
      // Add to history
      const newTransaction = {
        id: Date.now().toString(),
        type: 'earned',
        points: pointsToAward,
        reason: reason,
        timestamp: new Date().toISOString(),
        balance_after: loyaltyBalance.value
      }
      
      loyaltyHistory.value.unshift(newTransaction)
      
      console.log('✅ Points awarded successfully')
      return { success: true, data: { new_balance: loyaltyBalance.value, transaction: newTransaction } }
    } catch (err) {
      console.error('❌ Error awarding points:', err)
      return { success: false, error: err.message }
    }
  }

  // ================================================================
  // UTILITY METHODS
  // ================================================================

  /**
   * Clear all loyalty data
   */
  const clearLoyaltyData = () => {
    loyaltyBalance.value = 0
    loyaltyHistory.value = []
    loyaltyTiers.value = []
    currentTier.value = null
    error.value = null
    loyaltyCache.value.clear()
    historyCache.value = null
    lastFetchTime.value = 0
  }

  /**
   * Refresh loyalty data
   * @param {string} userId - Customer ID
   * @returns {Promise<Object>} Refresh result
   */
  const refreshLoyaltyData = async (userId) => {
    clearLoyaltyData()
    const balanceResult = await getLoyaltyBalance(userId)
    const historyResult = await getLoyaltyHistory(userId)
    const tierResult = await getCurrentTier(userId)
    
    return {
      success: balanceResult.success && historyResult.success && tierResult.success,
      data: {
        balance: balanceResult.data,
        history: historyResult.data,
        tier: tierResult.data
      }
    }
  }

  /**
   * Check if loyalty data is cached and valid
   * @returns {boolean} Cache validity
   */
  const isCacheValid = () => {
    return Date.now() - lastFetchTime.value < CACHE_DURATION
  }

  // ================================================================
  // RETURN COMPOSABLE INTERFACE
  // ================================================================

  return {
    // State
    loyaltyBalance,
    loyaltyHistory,
    loyaltyTiers,
    currentTier,
    isLoading,
    error,
    
    // Computed
    hasLoyaltyPoints,
    canRedeemPoints,
    maxRedemptionAmount,
    pointsValue,
    
    // Methods
    getLoyaltyBalance,
    getLoyaltyHistory,
    getLoyaltyTiers,
    getCurrentTier,
    calculatePointsEarned,
    calculatePointsDiscount,
    validatePointsRedemption,
    redeemPoints,
    awardPoints,
    clearLoyaltyData,
    refreshLoyaltyData,
    isCacheValid
  }
}
