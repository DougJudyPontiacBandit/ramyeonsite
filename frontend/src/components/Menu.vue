<template>
  <div class="menu-page">
    <h1>Menu</h1>
    
    <!-- Loading State -->
    <div v-if="loading || isLoading" class="loading-state">
      <p>Loading menu...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
      <button @click="fetchData">Retry</button>
    </div>

    <!-- Menu Content -->
    <div v-else>
      <div class="categories">
        <button
          :class="{ active: selectedCategory === 'All' }"
          @click="selectCategory('All', null)"
        >
          All
        </button>
        <button
          v-for="category in categories"
          :key="category._id"
          :class="{ active: selectedCategory === category._id }"
          @click="selectCategory(category._id, category.category_name)"
        >
          {{ category.category_name }}
        </button>
      </div>

      <div v-if="loadingProducts || isProductsLoading" class="loading-products">
        <p>Loading products...</p>
      </div>

      <div v-else-if="displayProducts.length === 0" class="no-products">
        <p>No products available in this category.</p>
      </div>

      <div v-else class="products-grid">
        <div
          class="product-card"
          v-for="product in displayProducts"
          :key="product.id || product._id"
        >
          <img 
            :src="product.image_url || product.image || require('../assets/Home/BigRamen.png')" 
            :alt="product.product_name || product.name"
            @error="handleImageError"
          />
          <div class="product-info">
            <h3>{{ product.product_name || product.name }}</h3>
            <p>{{ product.description || 'No description available' }}</p>
            <div class="price">₱{{ (product.selling_price || product.price).toFixed(2) }}</div>
          </div>
          <button class="add-btn" @click="addToCart(product)">+</button>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="pagination.total_pages > 1" class="pagination">
        <button 
          @click="goToPage(pagination.current_page - 1)" 
          :disabled="pagination.current_page === 1"
        >
          Previous
        </button>
        <span>Page {{ pagination.current_page }} of {{ pagination.total_pages }}</span>
        <button 
          @click="goToPage(pagination.current_page + 1)" 
          :disabled="pagination.current_page === pagination.total_pages"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import './Menu.css';
import { useProducts } from '../composables/api/useProducts.js';
import { useCategories } from '../composables/api/useCategories.js';

export default {
  name: "MenuPage",
  props: {
    onAddToCart: {
      type: Function,
      required: true,
    },
  },
  setup() {
    // Initialize composables
    const products = useProducts();
    const categories = useCategories();
    
    return {
      // Expose composable methods and state
      ...products,
      ...categories
    };
  },
  data() {
    return {
      // Keep local state for UI-specific data
      selectedCategory: 'All',
      selectedCategoryName: null,
      loading: true,
      loadingProducts: false,
      error: null,
      pagination: {
        current_page: 1,
        total_pages: 1,
        total_items: 0,
        items_per_page: 20
      }
    };
  },
  computed: {
    // Ensure products are reactive from composable
    displayProducts() {
      console.log('🔄 Display products computed:', this.products?.length || 0);
      return this.products || [];
    }
  },
  async mounted() {
    await this.fetchData();
  },
  methods: {
    async fetchData() {
      this.loading = true;
      this.error = null;
      
      try {
        // Fetch categories using composable
        await this.getCategories();
        console.log('📂 Categories loaded:', this.categories);
        
        // Fetch all products initially using composable
        await this.fetchProducts();
        
        this.loading = false;
      } catch (err) {
        console.error('Error fetching menu data:', err);
        this.error = err.message || 'Failed to load menu. Please try again.';
        this.loading = false;
      }
    },

    async fetchProducts(page = 1) {
      this.loadingProducts = true;
      
      try {
        let response;
        
        if (this.selectedCategory === 'All') {
          // Fetch all products using composable
          response = await this.getProducts({
            page: page,
            limit: this.pagination.items_per_page
          });
        } else {
          // Fetch products by category using composable
          console.log('🔍 Fetching products for category:', this.selectedCategory);
          response = await this.getProducts({
            category: this.selectedCategory,
            page: page,
            limit: this.pagination.items_per_page
          });
        }
        
        if (response.success && response.data) {
          // Products are already in the composable state
          console.log('📦 Products updated in composable:', response.data.length);
          
          // Update pagination if available
          if (response.data.pagination) {
            this.pagination = {
              current_page: response.data.pagination.current_page,
              total_pages: response.data.pagination.total_pages,
              total_items: response.data.pagination.total_items,
              items_per_page: response.data.pagination.items_per_page
            };
          }
        } else {
          console.warn('⚠️ No products data received:', response);
        }
        
        this.loadingProducts = false;
      } catch (err) {
        console.error('Error fetching products:', err);
        this.loadingProducts = false;
      }
    },

    async selectCategory(categoryId, categoryName) {
      console.log('🎯 Selecting category:', categoryId, categoryName);
      console.log('🎯 Available categories:', this.categories);
      this.selectedCategory = categoryId;
      this.selectedCategoryName = categoryName;
      this.pagination.current_page = 1; // Reset to first page
      await this.fetchProducts(1);
    },

    async goToPage(page) {
      if (page >= 1 && page <= this.pagination.total_pages) {
        await this.fetchProducts(page);
        // Scroll to top of products
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    },

    addToCart(product) {
      // Normalize product data for cart
      const cartProduct = {
        id: product.product_id || product._id || product.id,
        product_id: product.product_id || product._id || product.id,
        name: product.product_name || product.name,
        price: parseFloat(product.selling_price || product.price),
        description: product.description || 'No description available',
        image: product.image_url || product.image,
        category: product.category_name || product.category,
        subcategory: product.subcategory_name || product.subcategory,
        stock: product.stock_quantity || product.stock || 0
      };
      
      this.onAddToCart(cartProduct);
    },

    handleImageError(event) {
      // Fallback image when product image fails to load
      event.target.src = require('../assets/Home/BigRamen.png');
    }
  },
};
</script>
