// useCategories Composable
// Provides comprehensive category management with filtering, search, and hierarchy
import { ref, computed } from 'vue'
import { categoriesAPI } from '@/services/api.js'

/**
 * useCategories Composable
 * Manages category data, hierarchy, filtering, and search functionality
 * Used across multiple components: Menu, Home, Cart, Promotions
 */
export function useCategories() {
  // ================================================================
  // REACTIVE STATE
  // ================================================================
  
  // Category data
  const categories = ref([])
  const categoryHierarchy = ref([])
  const currentCategory = ref(null)
  const subcategories = ref([])
  const searchResults = ref([])
  
  // Loading states
  const isLoading = ref(false)
  const isSearching = ref(false)
  const isHierarchyLoading = ref(false)
  
  // Error handling
  const error = ref(null)
  const searchError = ref(null)
  const hierarchyError = ref(null)
  
  // Cache management
  const categoriesCache = ref(null)
  const hierarchyCache = ref(null)
  const lastFetchTime = ref(null)
  
  // ================================================================
  // COMPUTED PROPERTIES
  // ================================================================
  
  // Main categories (top level)
  const mainCategories = computed(() => {
    return categories.value.filter(category => !category.parent_id || category.parent_id === null)
  })
  
  // Categories with subcategories
  const categoriesWithSubcategories = computed(() => {
    return categories.value.filter(category => {
      return subcategories.value.some(sub => sub.parent_id === category._id)
    })
  })
  
  // Active categories (with products)
  const activeCategories = computed(() => {
    return categories.value.filter(category => category.is_active !== false)
  })
  
  // Featured categories
  const featuredCategories = computed(() => {
    return categories.value.filter(category => category.is_featured === true)
  })
  
  // Category breadcrumb path
  const categoryBreadcrumb = computed(() => {
    if (!currentCategory.value) return []
    
    const breadcrumb = []
    let category = currentCategory.value
    
    while (category) {
      breadcrumb.unshift(category)
      category = categories.value.find(cat => cat._id === category.parent_id)
    }
    
    return breadcrumb
  })
  
  // ================================================================
  // CORE CATEGORY METHODS
  // ================================================================
  
  /**
   * Get all categories
   * @param {Object} filters - Filter options (active, featured, etc.)
   * @returns {Promise<Object>} Categories data
   */
  const getCategories = async (filters = {}) => {
    try {
      isLoading.value = true
      error.value = null
      
      console.log('📂 Fetching categories with filters:', filters)
      
      // Check cache first
      if (categoriesCache.value && Date.now() - categoriesCache.value.timestamp < 300000) {
        console.log('✅ Using cached categories data')
        categories.value = categoriesCache.value.data
        isLoading.value = false
        return { success: true, data: categoriesCache.value.data }
      }
      
      // Fetch from API
      const result = await categoriesAPI.getAll()
      
      if (result.categories) {
        categories.value = result.categories
        lastFetchTime.value = Date.now()
        
        // Cache the result
        categoriesCache.value = {
          data: categories.value,
          timestamp: Date.now()
        }
        
        console.log(`✅ Fetched ${categories.value.length} categories`)
        return { success: true, data: categories.value }
      } else {
        throw new Error(result.message || 'Failed to fetch categories')
      }
    } catch (err) {
      console.error('❌ Error fetching categories:', err)
      error.value = err.message
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }
  
  /**
   * Get single category by ID
   * @param {string} categoryId - Category ID
   * @returns {Promise<Object>} Category data
   */
  const getCategory = async (categoryId) => {
    try {
      isLoading.value = true
      error.value = null
      
      console.log('📂 Fetching category:', categoryId)
      
      // Check if category is already in our list
      const existingCategory = categories.value.find(cat => cat._id === categoryId)
      if (existingCategory) {
        currentCategory.value = existingCategory
        isLoading.value = false
        return { success: true, data: existingCategory }
      }
      
      // Fetch from API
      const result = await categoriesAPI.getById(categoryId)
      
      if (result.success) {
        currentCategory.value = result.data
        console.log('✅ Category fetched successfully')
        return { success: true, data: result.data }
      } else {
        throw new Error(result.error || 'Failed to fetch category')
      }
    } catch (err) {
      console.error('❌ Error fetching category:', err)
      error.value = err.message
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }
  
  /**
   * Get category hierarchy (tree structure)
   * @returns {Promise<Object>} Category hierarchy data
   */
  const getCategoryHierarchy = async () => {
    try {
      isHierarchyLoading.value = true
      hierarchyError.value = null
      
      console.log('🌳 Fetching category hierarchy')
      
      // Check cache first
      if (hierarchyCache.value && Date.now() - hierarchyCache.value.timestamp < 300000) {
        console.log('✅ Using cached hierarchy data')
        categoryHierarchy.value = hierarchyCache.value.data
        isHierarchyLoading.value = false
        return { success: true, data: hierarchyCache.value.data }
      }
      
      // Fetch from API
      const result = await categoriesAPI.getAll()
      
      if (result.success) {
        categoryHierarchy.value = result.data
        hierarchyCache.value = {
          data: result.data,
          timestamp: Date.now()
        }
        
        console.log('✅ Category hierarchy fetched successfully')
        return { success: true, data: result.data }
      } else {
        throw new Error(result.error || 'Failed to fetch category hierarchy')
      }
    } catch (err) {
      console.error('❌ Error fetching category hierarchy:', err)
      hierarchyError.value = err.message
      return { success: false, error: err.message }
    } finally {
      isHierarchyLoading.value = false
    }
  }
  
  /**
   * Get subcategories for a parent category
   * @param {string} parentId - Parent category ID
   * @returns {Promise<Object>} Subcategories data
   */
  const getSubcategories = async (parentId) => {
    try {
      isLoading.value = true
      error.value = null
      
      console.log('📂 Fetching subcategories for parent:', parentId)
      
      // Check if we already have subcategories in our list
      const existingSubcategories = categories.value.filter(cat => cat.parent_id === parentId)
      if (existingSubcategories.length > 0) {
        subcategories.value = existingSubcategories
        isLoading.value = false
        return { success: true, data: existingSubcategories }
      }
      
      // Fetch from API
      const result = await categoriesAPI.getSubcategories(parentId)
      
      if (result.success) {
        subcategories.value = result.data.results || result.data
        console.log(`✅ Fetched ${subcategories.value.length} subcategories`)
        return { success: true, data: subcategories.value }
      } else {
        throw new Error(result.error || 'Failed to fetch subcategories')
      }
    } catch (err) {
      console.error('❌ Error fetching subcategories:', err)
      error.value = err.message
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }
  
  /**
   * Search categories by query
   * @param {string} query - Search query
   * @returns {Promise<Object>} Search results
   */
  const searchCategories = async (query) => {
    try {
      isSearching.value = true
      searchError.value = null
      
      if (!query || query.trim().length < 2) {
        searchResults.value = []
        return { success: true, data: [] }
      }
      
      console.log('🔍 Searching categories:', query)
      
      const result = await categoriesAPI.getAll()
      
      if (result.success) {
        searchResults.value = result.data.results || result.data
        console.log(`✅ Found ${searchResults.value.length} categories`)
        return { success: true, data: searchResults.value }
      } else {
        throw new Error(result.error || 'Category search failed')
      }
    } catch (err) {
      console.error('❌ Category search error:', err)
      searchError.value = err.message
      return { success: false, error: err.message }
    } finally {
      isSearching.value = false
    }
  }
  
  /**
   * Get featured categories
   * @returns {Promise<Object>} Featured categories data
   */
  const getFeaturedCategories = async () => {
    try {
      isLoading.value = true
      error.value = null
      
      console.log('⭐ Fetching featured categories')
      
      const result = await categoriesAPI.getAll()
      
      if (result.success) {
        const featured = result.data.results || result.data
        console.log(`✅ Fetched ${featured.length} featured categories`)
        return { success: true, data: featured }
      } else {
        throw new Error(result.error || 'Failed to fetch featured categories')
      }
    } catch (err) {
      console.error('❌ Error fetching featured categories:', err)
      error.value = err.message
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }
  
  // ================================================================
  // CATEGORY NAVIGATION METHODS
  // ================================================================
  
  /**
   * Set current category
   * @param {string|Object} category - Category ID or category object
   */
  const setCurrentCategory = (category) => {
    if (typeof category === 'string') {
      currentCategory.value = categories.value.find(cat => cat._id === category)
    } else {
      currentCategory.value = category
    }
    
    console.log('📂 Current category set to:', currentCategory.value?.name)
  }
  
  /**
   * Clear current category
   */
  const clearCurrentCategory = () => {
    currentCategory.value = null
    console.log('📂 Current category cleared')
  }
  
  /**
   * Navigate to parent category
   * @returns {Object|null} Parent category or null
   */
  const navigateToParent = () => {
    if (!currentCategory.value || !currentCategory.value.parent_id) {
      return null
    }
    
    const parentCategory = categories.value.find(cat => cat._id === currentCategory.value.parent_id)
    if (parentCategory) {
      setCurrentCategory(parentCategory)
      return parentCategory
    }
    
    return null
  }
  
  /**
   * Navigate to root categories
   */
  const navigateToRoot = () => {
    clearCurrentCategory()
    console.log('📂 Navigated to root categories')
  }
  
  // ================================================================
  // UTILITY METHODS
  // ================================================================
  
  /**
   * Clear all errors
   */
  const clearError = () => {
    error.value = null
    searchError.value = null
    hierarchyError.value = null
  }
  
  /**
   * Clear search results
   */
  const clearSearch = () => {
    searchResults.value = []
    searchError.value = null
  }
  
  /**
   * Refresh categories data
   */
  const refreshCategories = async () => {
    console.log('🔄 Refreshing categories data')
    categoriesCache.value = null
    hierarchyCache.value = null
    lastFetchTime.value = null
    return await getCategories()
  }
  
  /**
   * Clear all cache
   */
  const clearCache = () => {
    console.log('🗑️ Clearing categories cache')
    categoriesCache.value = null
    hierarchyCache.value = null
    lastFetchTime.value = null
  }
  
  /**
   * Get category by ID from current categories list
   * @param {string} categoryId - Category ID
   * @returns {Object|null} Category object or null
   */
  const findCategoryById = (categoryId) => {
    return categories.value.find(category => category._id === categoryId || category.id === categoryId) || null
  }
  
  /**
   * Get categories by parent ID
   * @param {string} parentId - Parent category ID
   * @returns {Array} Categories with specified parent
   */
  const getCategoriesByParent = (parentId) => {
    return categories.value.filter(category => category.parent_id === parentId)
  }
  
  /**
   * Check if category has subcategories
   * @param {string} categoryId - Category ID
   * @returns {boolean} True if has subcategories
   */
  const hasSubcategories = (categoryId) => {
    return categories.value.some(category => category.parent_id === categoryId)
  }
  
  /**
   * Get category path (breadcrumb)
   * @param {string} categoryId - Category ID
   * @returns {Array} Array of category objects forming the path
   */
  const getCategoryPath = (categoryId) => {
    const path = []
    let category = categories.value.find(cat => cat._id === categoryId)
    
    while (category) {
      path.unshift(category)
      category = categories.value.find(cat => cat._id === category.parent_id)
    }
    
    return path
  }
  
  /**
   * Get all descendant categories
   * @param {string} categoryId - Parent category ID
   * @returns {Array} All descendant categories
   */
  const getDescendantCategories = (categoryId) => {
    const descendants = []
    const directChildren = categories.value.filter(cat => cat.parent_id === categoryId)
    
    directChildren.forEach(child => {
      descendants.push(child)
      descendants.push(...getDescendantCategories(child._id))
    })
    
    return descendants
  }
  
  // ================================================================
  // RETURN COMPOSABLE
  // ================================================================
  
  return {
    // State
    categories,
    categoryHierarchy,
    currentCategory,
    subcategories,
    searchResults,
    isLoading,
    isSearching,
    isHierarchyLoading,
    error,
    searchError,
    hierarchyError,
    
    // Computed
    mainCategories,
    categoriesWithSubcategories,
    activeCategories,
    featuredCategories,
    categoryBreadcrumb,
    
    // Core methods
    getCategories,
    getCategory,
    getCategoryHierarchy,
    getSubcategories,
    searchCategories,
    getFeaturedCategories,
    
    // Navigation methods
    setCurrentCategory,
    clearCurrentCategory,
    navigateToParent,
    navigateToRoot,
    
    // Utility methods
    clearError,
    clearSearch,
    refreshCategories,
    clearCache,
    findCategoryById,
    getCategoriesByParent,
    hasSubcategories,
    getCategoryPath,
    getDescendantCategories
  }
}
